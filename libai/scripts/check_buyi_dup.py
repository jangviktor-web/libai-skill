# -*- coding: utf-8 -*-
"""核验 02_buyi.md 中的篇目在本集(修复版)中是否已存在"""
import re

buyi = open('/sandbox/workspace/libai/modules/02_buyi.md', encoding='utf-8').read()
main = open('/sandbox/workspace/libai/modules/01_libai-shi-quanji.md', encoding='utf-8').read()
lines_main = main.split('\n')

titles = [t.strip() for t in re.findall(r'^## (.+)$', buyi, re.M)]
titles = [t for t in titles if not t.startswith('【') and not t.startswith('附')]

dup, new = [], []
for t in titles:
    base = re.sub(r'^(.+?)(其一|其二|其三|二首|三首|四首|五首|六首|七首|八首|十首|十七首|十九首|十二首|二十一首).*$', r'\1', t)
    hit = (t in main) or (base in main)
    (dup if hit else new).append(t)

print(f'02_buyi 诗题 {len(titles)} | 本集已有(重复) {len(dup)} | 本集仍无(真缺) {len(new)}')
print('\n=== 重复（应从 02_buyi 移除）===')
for d in dup: print('  ', d)
print('\n=== 真缺（保留在 02_buyi）===')
for n in new: print('  ', n)
