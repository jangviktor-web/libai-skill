# -*- coding: utf-8 -*-
"""按篇题抽取含关键词的诗句，供「维度11·唐代文士文化语境」取证使用。"""
import re, sys, json

SRC = "/sandbox/workspace/libai/modules/01_libai-shi-quanji.md"
lines = open(SRC, encoding="utf-8").read().split("\n")

JUAN = re.compile(r"^卷[一二三四五六七八九十]+")
def is_title(s):
    if not s.startswith("　　"):
        return False
    body = s.strip()
    if not body or body.startswith("(") or body.startswith("（"):
        return False
    if "。" in body:
        return False
    if len(body) > 22:
        return False
    return True

titles = [""] * len(lines)
cur_juan, cur_title, parent = "", "", ""
SUB = re.compile(r"^其[一二三四五六七八九十百]+$")
for i, s in enumerate(lines):
    if JUAN.match(s.strip()):
        cur_juan = s.strip()
    if is_title(s):
        t = s.strip()
        if SUB.match(t):
            cur_title = f"{parent}·{t}"
        else:
            parent = t
            cur_title = t
    titles[i] = f"{cur_juan}/{cur_title}"

KEYWORDS = sys.argv[1].split(",")
out = {}
for k in KEYWORDS:
    hits = []
    for i, s in enumerate(lines):
        if k in s and s.startswith("　　"):
            hits.append((titles[i], s.strip()))
    out[k] = hits

for k, hits in out.items():
    print(f"=====[{k}] {len(hits)} 行 =====")
    seen = set()
    for t, s in hits:
        print(f"  {t} :: {s}")
    print()
