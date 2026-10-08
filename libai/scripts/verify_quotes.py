# -*- coding: utf-8 -*-
import re, io

src = io.open("/sandbox/workspace/libai/modules/01_libai-shi-quanji.md", encoding="utf-8", errors="ignore").read()
doc = io.open("/sandbox/workspace/libai/references/11-cultural-context.md", encoding="utf-8").read()

frags = set()
for m in re.finditer(r'"([^"\n]{2,60})"', doc):
    s = m.group(1)
    if re.search(r'[\u4e00-\u9fff]', s) and not re.search(r'[A-Za-z]{3}', s):
        frags.add(s)

miss = []
for f in sorted(frags):
    ok = False
    for part in re.split(r'[／/]|\s{2,}', f):
        p = part.strip()
        if not p or p in ("系", "按"):
            ok = True
            continue
        if p in src:
            ok = True
    if not ok:
        miss.append(f)

print("quoted frags:", len(frags), "missing:", len(miss))
for m in miss:
    print("  x", m)
