# -*- coding: utf-8 -*-
s = open('/sandbox/workspace/libai/modules/01_libai-shi-quanji.md', encoding='utf-8').read()
lines = s.split('\n')
bad = []
for i, l in enumerate(lines):
    for ch in l:
        o = ord(ch)
        if o == 0xFFFD or 0xE000 <= o <= 0xF8FF or o in (0xFFFE, 0xFFFF):
            bad.append(i + 1); break
print('替换符/私用区 异常行数:', len(bad), bad[:30])

print('--- 卷二十一附近（14240-14285）---')
print('\n'.join(lines[14239:14285]))

print('--- 卷四附近（查卷四行号）---')
for i, l in enumerate(lines[:3300]):
    if l.strip() in ('卷四', '卷四（乐府四十四首）') or l.strip().startswith('卷四'):
        print('卷四行号:', i + 1, repr(l)); break

import collections
c = collections.Counter()
for l in lines:
    for ch in l:
        o = ord(ch)
        if o > 0x2FFF and not (0x4E00 <= o <= 0x9FFF) and not (0x3000 <= o <= 0x303F) and not (0xFF00 <= o <= 0xFFEF):
            c[ch] += 1
print('非常见字符 Top:', c.most_common(20))
