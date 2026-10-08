# -*- coding: utf-8 -*-
"""对 modules/01_libai-shi-quanji.md 的 4 个复原段与权威源做字符级比对，输出候选讹字。"""
import re, difflib, sys, unicodedata

BASE = "/sandbox/workspace/libai/"
MOD = BASE + "modules/01_libai-shi-quanji.md"

SEGMENTS = {"卷四": (2530, 3208), "卷十二": (8273, 8887), "卷十四": (9356, 10124), "卷二十": (13625, 14239)}

PUNCT = "，。、；：？！“”‘’（）《》〈〉「」『』,.!?;:\"'()[]　 \u3000\u00a0—－-·…"

def norm(s):
    """去标点/空白，保留汉字"""
    out = []
    for ch in s:
        if ch in PUNCT:
            continue
        out.append(ch)
    return "".join(out)

def strip_notes(s):
    """去掉 ( X一作Y ) / ( 一作... ) 之类校记"""
    s = re.sub(r"[（(][^（()）]*[)）]", "", s)
    return s

# ---------- 解析 module ----------
lines = open(MOD, encoding="utf-8").read().split("\n")
poems = []  # (lineno_of_title, title, [(lineno, text)])
cur = None
for i, raw in enumerate(lines, 1):
    s = raw.strip().strip("\u3000").strip()
    if not s:
        continue
    if re.fullmatch(r"卷[一二三四五六七八九十]+", s) or re.fullmatch(r"(乐府|古近体诗|古风)[\u4e00-\u9fa5]*首", s):
        cur = None
        continue
    if s.startswith("(") or s.startswith("（"):
        if cur:
            cur[2].append((i, s))
        continue
    if "。" in s:
        if cur:
            cur[2].append((i, s))
        continue
    cur = (i, s, [])
    poems.append(cur)

def seg_of(lineno):
    for k, (a, b) in SEGMENTS.items():
        if a <= lineno <= b:
            return k
    return None

# ---------- 解析 全唐诗（李白） ----------
qts = {}
cur = None
for raw in open(BASE + "refs/quan_tang_shi.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    m = re.match(r"^卷\d+_(\d+)\s*【(.*?)】(.*)$", s)
    if m:
        author = m.group(3).strip()
        if author.startswith("李白"):
            t = m.group(2)
            for sep in ("　", " "):
                pass
            short = re.split(r"[　\s]", t)[-1]
            cur = {"title": t, "short": short, "text": ""}
            qts.setdefault(norm(short), []).append(cur)
        else:
            cur = None
        continue
    if cur is not None and s and not s.startswith("《"):
        cur["text"] += s

# ---------- 解析 李太白全集（王琦本） ----------
tb = []
for raw in open(BASE + "refs/li_taibai_ji.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    if not s:
        continue
    t = norm(s)
    if len(t) >= 8:
        tb.append(t)

def find_tb(text):
    key = norm(text)
    if len(key) < 6:
        return None
    k = key[:14]
    for t in tb:
        if k in t:
            return t
    k2 = key[:8]
    for t in tb:
        if k2 in t:
            return t
    return None

out = []
for (tl, title, body) in poems:
    seg = seg_of(tl)
    if not seg:
        continue
    content = [ (ln, strip_notes(txt)) for ln, txt in body if "。" in txt ]
    if not content:
        continue
    my = norm("".join(t for _, t in content))
    if len(my) < 6:
        continue
    # 找权威
    src = None
    cands = qts.get(norm(title.split(" (")[0].split("（")[0].strip()))
    if cands:
        src = cands[0]
    if src is None:
        # 用首句匹配
        head = my[:10]
        for d in qts.values():
            for c in d:
                if head and head in norm(c["text"]):
                    src = c
                    break
            if src: break
    refname, reftext = None, None
    if src and my[:8] in norm(src["text"]):
        refname, reftext = "全唐诗:" + src["short"], norm(src["text"])
    else:
        t = find_tb(my)
        if t:
            refname, reftext = "王琦本", t
    if reftext is None:
        out.append((seg, tl, title, "NO-MATCH", "", ""))
        continue
    sm = difflib.SequenceMatcher(None, my, reftext, autojunk=False)
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace":
            ops.append(("R", my[i1:i2], reftext[j1:j2], my[max(0,i1-6):i1], my[i2:i2+6]))
        elif tag == "insert":
            ops.append(("I", "", reftext[j1:j2], my[max(0,i1-6):i1], my[i1:i1+6]))
        elif tag == "delete":
            ops.append(("D", my[i1:i2], "", my[max(0,i1-6):i1], my[i2:i2+6]))
    if ops:
        out.append((seg, tl, title, refname, my, ops))

with open(BASE + "scripts/diff_report.txt", "w", encoding="utf-8") as f:
    for seg, tl, title, refname, my, ops in out:
        if refname == "NO-MATCH":
            f.write("[%s] L%d %s  ==> 未匹配到权威源\n" % (seg, tl, title))
            continue
        f.write("\n[%s] L%d %s  (源:%s)\n" % (seg, tl, title, refname))
        for tag, a, b, pre, post in ops:
            f.write("    %s  「%s」→「%s」   上下文:%s[%s→%s]%s\n" % (tag, a, b, pre, a or b, b or a, post))
print("done", len(out))
