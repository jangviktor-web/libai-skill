# -*- coding: utf-8 -*-
"""生成 4 段全量比对决策报告：破损字 G / 逆向候选 CAND(G) / 当前字 A / 权威字 B"""
import re, json, difflib

BASE = "/sandbox/workspace/libai/"
SEGMENTS = {"卷四": (2530, 3208), "卷十二": (8273, 8887), "卷十四": (9356, 10124), "卷二十": (13625, 14239)}
PUNCT = "，。、；：？！“”‘’（）《》〈〉「」『』,.!?;:\"'()[]　 \u3000\u00a0—－-·…"
rev = json.load(open(BASE + "scripts/reverse_map.json"))

def norm(s):
    return "".join(ch for ch in s if ch not in PUNCT)
def norm_pos(s):
    """返回 list: 规范化后第k个字符在原文中的下标"""
    return [i for i, ch in enumerate(s) if ch not in PUNCT]
def strip_notes(s):
    return re.sub(r"[（(][^（()）]*[)）]", "", s)

cur_lines = open(BASE + "modules/01_libai-shi-quanji.md", encoding="utf-8").read().split("\n")
brk_lines = open(BASE + "modules/01_libai-shi-quanji.broken-backup.md", encoding="utf-8").read().split("\n")

# 解析 module（分组诗）
groups = []
cur_parent = cur_sub = None
for i, raw in enumerate(cur_lines, 1):
    s = raw.strip().strip("\u3000").strip()
    if not s: continue
    if re.fullmatch(r"卷[一二三四五六七八九十]+", s) or re.fullmatch(r"(乐府|古近体诗|古风)[\u4e00-\u9fa5]*首", s):
        cur_parent = cur_sub = None; continue
    if "。" in s:
        if cur_sub is not None: cur_sub[2].append((i, strip_notes(s)))
        continue
    if s.startswith("(") or s.startswith("（"): continue
    if re.fullmatch(r"其[一二三四五六七八九十]+", s) and cur_parent is not None:
        cur_sub = (s, i, []); cur_parent[2].append(cur_sub); continue
    cur_parent = [s, i, []]; cur_sub = ("", i, []); cur_parent[2].append(cur_sub); groups.append(cur_parent)

def seg_of(n):
    for k, (a, b) in SEGMENTS.items():
        if a <= n <= b: return k
    return None

# 权威源
qts = []
c = None
for raw in open(BASE + "refs/quan_tang_shi.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    m = re.match(r"^卷\d+_(\d+)\s*【(.*?)】(.*)$", s)
    if m:
        if m.group(3).strip().startswith("李白"):
            c = {"title": m.group(2), "short": re.split(r"[　\s]", m.group(2))[-1], "text": ""}
            qts.append(c)
        else: c = None
        continue
    if c is not None and s and not s.startswith("《"): c["text"] += s
for c in qts: c["n"] = norm(c["text"])
tb = [norm(l.strip()) for l in open(BASE + "refs/li_taibai_ji.txt", encoding="utf-8", errors="replace") if len(l.strip()) >= 10]

out = []
for g in groups:
    seg = seg_of(g[1])
    if not seg: continue
    subs = [s for s in g[2] if s[2]]
    if not subs: continue
    my = ""; pos = []
    for sub in subs:
        for ln, txt in sub[2]:
            n = norm(txt); my += n
            pos += [(ln, j) for j in range(len(n))]
    if len(my) < 8: continue
    tc = g[0].split(" (")[0].split("（")[0].strip()
    ref = refname = None
    for cc in qts:
        if cc["short"] == tc or norm(cc["title"]) == norm(tc):
            ref, refname = cc["n"], "全唐诗"; break
    if ref is None:
        for cc in qts:
            if my[:10] and my[:10] in cc["n"]:
                ref, refname = cc["n"], "全唐诗"; break
    if ref is None:
        for t in tb:
            if my[:12] and my[:12] in t:
                ref, refname = t, "王琦本"; break
    if ref is None:
        out.append((seg, g[1], g[0], "NO-REF", [])); continue
    # 王琦本同诗对齐映射
    tbmap = {}
    tbtext = None
    for t in tb:
        if my[:12] and my[:12] in t:
            tbtext = t; break
    if tbtext is not None:
        sm2 = difflib.SequenceMatcher(None, my, tbtext, autojunk=False)
        for tag, i1, i2, j1, j2 in sm2.get_opcodes():
            if tag in ("equal", "replace"):
                for d in range(min(i2 - i1, j2 - j1)):
                    tbmap[i1 + d] = j1 + d
    def tbch(ip):
        j = tbmap.get(ip)
        return tbtext[j] if (tbtext is not None and j is not None) else "·"
    sm = difflib.SequenceMatcher(None, my, ref, autojunk=False)
    ent = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        if tag in ("insert", "delete") and abs((i2 - i1) - (j2 - j1)) > 2:
            ent.append(("ALIGN?", pos[i1][0] if i1 < len(pos) else g[1], my[i1:i2], ref[j1:j2], "", "", "", tbch(i1), "", i1)); continue
        if tag == "replace" and (i2 - i1) > 6:
            ent.append(("BIGR", pos[i1][0], my[i1:i2], ref[j1:j2], "", "", "", tbch(i1), "", i1)); continue
        k = max(i2 - i1, j2 - j1)
        for d in range(k):
            ip, jp = i1 + d, j1 + d
            A = my[ip] if ip < i2 else ""
            B = ref[jp] if jp < j2 else ""
            if A == B: continue
            if ip < len(pos):
                ln, off = pos[ip]
                raw = cur_lines[ln - 1]
                G = "?"
                brow = brk_lines[ln - 1]
                bp = norm_pos(brow)
                if off < len(bp):
                    G = brow[bp[off]]
                cand = "".join(sorted(rev.get(G, [])))
            else:
                ln, off, raw, G, cand = None, None, "", "", ""
            ent.append((tag, ln, A, B, cand, G, raw.strip(), tbch(ip), "A∈C" if A in cand else "A∉C", ip))
    if ent:
        out.append((seg, g[1], g[0], refname, ent))

with open(BASE + "scripts/decision_report.txt", "w", encoding="utf-8") as f:
    tot = 0
    for seg, tl, title, rn, ent in out:
        f.write("\n[%s] L%d 《%s》 源:%s\n" % (seg, tl, title, rn))
        for tag, ln, A, B, cand, G, raw, C, ac, ip in ent:
            tot += 1
            ver = "候选命中" if (B in cand) else ("候选外" if cand else "无候选")
            f.write("  L%-6s %-5s A=%-3s B=%-3s C=%-3s G=%-3s CAND=%-8s %-6s %s\n" % (str(ln), tag, A or "-", B or "-", C or "-", G or "-", cand or "-", ac, ver))
            if tag in ("ALIGN?", "BIGR"):
                f.write("        RAW=%s | REF=%s\n" % (raw[:60], B[:60]))
    print("entries", tot)
