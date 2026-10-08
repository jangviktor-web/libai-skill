# -*- coding: utf-8 -*-
"""题名层面比对：本集题名 vs 权威题名，含逆向候选验证"""
import re, json, difflib
BASE = "/sandbox/workspace/libai/"
SEGMENTS = {"卷四": (2530, 3208), "卷十二": (8273, 8887), "卷十四": (9356, 10124), "卷二十": (13625, 14239)}
PUNCT = "，。、；：？！“”‘’（）《》〈〉「」『』,.!?;:\"'()[]　 \u3000\u00a0—－-·…"
rev = json.load(open(BASE + "scripts/reverse_map.json"))
def norm(s): return "".join(ch for ch in s if ch not in PUNCT)

cur = open(BASE + "modules/01_libai-shi-quanji.md", encoding="utf-8").read().split("\n")
brk = open(BASE + "modules/01_libai-shi-quanji.broken-backup.md", encoding="utf-8").read().split("\n")
qts = []
c = None
for raw in open(BASE + "refs/quan_tang_shi.txt", encoding="utf-8", errors="replace"):
    s = raw.strip()
    m = re.match(r"^卷\d+_(\d+)\s*【(.*?)】(.*)$", s)
    if m:
        if m.group(3).strip().startswith("李白"):
            c = m.group(2); qts.append(c)
        else: c = None
titles = set()
for t in qts:
    titles.add(norm(re.split(r"[　\s]", t)[-1]))
    titles.add(norm(t))

out = []
for i, raw in enumerate(cur, 1):
    if not any(a <= i <= b for a, b in SEGMENTS.values()): continue
    s = raw.strip().strip("\u3000").strip()
    if not s or "。" in s or s.startswith("(") or s.startswith("（"): continue
    if re.fullmatch(r"卷[一二三四五六七八九十]+", s): continue
    if re.fullmatch(r"(乐府|古近体诗|古风)[\u4e00-\u9fa5]*首", s): continue
    nt = norm(re.sub(r"[（(].*?[)）]", "", s))
    if nt in titles or not nt or nt == "其一":
        continue
    # 找最接近的权威题名
    best = max(titles, key=lambda t: difflib.SequenceMatcher(None, nt, t).ratio())
    r = difflib.SequenceMatcher(None, nt, best).ratio()
    if r < 0.5 or nt == best: continue
    # 逐字差异 + 逆向候选
    brow = brk[i - 1]
    bp = [k for k, ch in enumerate(brow) if ch not in PUNCT]
    diffs = []
    sm = difflib.SequenceMatcher(None, nt, best)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for d in range(i2 - i1, -1, -1): pass
            continue
        for d in range(max(i2 - i1, j2 - j1) + 1):
            A = nt[i1 + d] if i1 + d < i2 else ""
            B = best[j1 + d] if j1 + d < j2 else ""
            if A == B: continue
            G = brow[bp[i1 + d]] if i1 + d < len(bp) else "?"
            diffs.append((A, B, G, "".join(sorted(rev.get(G, [])))))
        # 同时给所有候选字
    out.append((i, s, best, round(r, 2), diffs))

with open(BASE + "scripts/title_diff.txt", "w", encoding="utf-8") as f:
    for i, s, best, r, diffs in out:
        f.write("L%-6d 本集《%s》\n        权威《%s》 r=%.2f\n" % (i, s, best, r))
        for A, B, G, cand in diffs:
            f.write("        A=%s B=%s G=%s CAND=%s %s\n" % (A or "-", B or "-", G or "-", cand or "-",
                    "候选命中" if (B in cand and B) else "候选外"))
print("titles diff:", len(out))
