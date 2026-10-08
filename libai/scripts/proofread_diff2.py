# -*- coding: utf-8 -*-
"""v2: 4 段复原区与权威源字符级比对。组诗合并比对，偏移映射回行号。"""
import re, difflib

BASE = "/sandbox/workspace/libai/"
MOD = BASE + "modules/01_libai-shi-quanji.md"
SEGMENTS = {"卷四": (2530, 3208), "卷十二": (8273, 8887), "卷十四": (9356, 10124), "卷二十": (13625, 14239)}
PUNCT = "，。、；：？！“”‘’（）《》〈〉「」『』,.!?;:\"'()[]　 \u3000\u00a0—－-·…"

def norm(s):
    return "".join(ch for ch in s if ch not in PUNCT)

def strip_notes(s):
    return re.sub(r"[（(][^（()）]*[)）]", "", s)

lines = open(MOD, encoding="utf-8").read().split("\n")

# ---- 解析 module，构造 groups ----
groups = []            # [ [parent_title, parent_lineno, [(subtitle, lineno, [rawlines])] ] ]
cur_parent = None
cur_sub = None
for i, raw in enumerate(lines, 1):
    s = raw.strip().strip("\u3000").strip()
    if not s:
        continue
    if re.fullmatch(r"卷[一二三四五六七八九十]+", s) or re.fullmatch(r"(乐府|古近体诗|古风)[\u4e00-\u9fa5]*首", s):
        cur_parent = None; cur_sub = None
        continue
    if "。" in s:
        if cur_sub is not None:
            cur_sub[2].append((i, strip_notes(s)))
        continue
    if s.startswith("(") or s.startswith("（"):
        continue
    if re.fullmatch(r"其[一二三四五六七八九十]+", s) and cur_parent is not None:
        cur_sub = (s, i, [])
        cur_parent[2].append(cur_sub)
        continue
    # 新诗题
    cur_parent = [s, i, []]
    cur_sub = ("", i, [])
    cur_parent[2].append(cur_sub)
    groups.append(cur_parent)

def seg_of(lineno):
    for k, (a, b) in SEGMENTS.items():
        if a <= lineno <= b:
            return k
    return None

# ---- 权威源 ----
qts = []
cur = None
for raw in open(BASE + "refs/quan_tang_shi.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    m = re.match(r"^卷\d+_(\d+)\s*【(.*?)】(.*)$", s)
    if m:
        if m.group(3).strip().startswith("李白"):
            t = m.group(2)
            cur = {"title": t, "short": re.split(r"[　\s]", t)[-1], "text": ""}
            qts.append(cur)
        else:
            cur = None
        continue
    if cur is not None and s and not s.startswith("《"):
        cur["text"] += s
for c in qts:
    c["n"] = norm(c["text"])

tb = []
for raw in open(BASE + "refs/li_taibai_ji.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    if len(s) >= 10:
        tb.append(norm(s))

def find_tb(key):
    if len(key) < 6: return None
    for t in tb:
        if key[:12] in t: return t
    return None

# ---- 比对 ----
report = []
for g in groups:
    seg = seg_of(g[1])
    if not seg:
        continue
    subs = [s for s in g[2] if s[2]]
    if not subs:
        continue
    my = ""
    pos = []          # char index -> (lineno, raw line)
    for sub in subs:
        for ln, txt in sub[2]:
            n = norm(txt)
            my += n
            pos += [(ln, txt)] * len(n)
    if len(my) < 8:
        continue
    title_clean = g[0].split(" (")[0].split("（")[0].strip()
    ref, refname = None, None
    for c in qts:
        if c["short"] == title_clean or norm(c["title"]) == norm(title_clean) or title_clean == c["short"]:
            ref, refname = c["n"], "全唐诗"
            break
    if ref is None:
        for c in qts:
            if my[:10] and my[:10] in c["n"]:
                ref, refname = c["n"], "全唐诗"
                break
    if ref is None:
        t = find_tb(my)
        if t:
            ref, refname = t, "王琦本"
    if ref is None:
        report.append((g[1], seg, g[0], "NO-MATCH", []))
        continue
    sm = difflib.SequenceMatcher(None, my, ref, autojunk=False)
    ops = []
    big = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag in ("insert", "delete") and abs((i2 - i1) - (j2 - j1)) > 3:
            big += 1
        if tag == "replace" and (i2 - i1) > 5:
            big += 1
            continue
        ln = pos[i1][0] if i1 < len(pos) else (pos[-1][0] if pos else g[1])
        rawline = pos[i1][1] if i1 < len(pos) else ""
        ops.append((tag, ln, my[i1:i2], ref[j1:j2],
                    my[max(0, i1 - 7):i1], my[i2:i2 + 7], rawline))
    if ops or big:
        report.append((g[1], seg, g[0], refname + (" [对齐异常%d]" % big if big else ""), ops))

with open(BASE + "scripts/diff_report2.txt", "w", encoding="utf-8") as f:
    for tl, seg, title, refname, ops in report:
        f.write("\n[%s] L%d 《%s》 源:%s\n" % (seg, tl, title, refname))
        for tag, ln, a, b, pre, post, rawline in ops:
            f.write("   L%-6d %-6s 「%s」→「%s」  …%s[%s]%s…   |原文行: %s\n"
                    % (ln, tag, a, b, pre, (a + "/" + b) if a and b else (a or b), post, rawline.strip()))
print("pairs:", len(report))
