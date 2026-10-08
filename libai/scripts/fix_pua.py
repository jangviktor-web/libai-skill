# -*- coding: utf-8 -*-
"""将 modules 中的私用区(PUA)字符替换为古籍缺字符 □，并统计"""
p = '/sandbox/workspace/libai/modules/01_libai-shi-quanji.md'
s = open(p, encoding='utf-8').read()
out = []
cnt = 0
lines_hit = set()
cur_line = 1
for ch in s:
    if ch == '\n':
        cur_line += 1
    o = ord(ch)
    if 0xE000 <= o <= 0xF8FF:
        out.append('□')
        cnt += 1
        lines_hit.add(cur_line)
    else:
        out.append(ch)
open(p, 'w', encoding='utf-8').write(''.join(out))
print('替换 PUA 字符数:', cnt, '涉及行数:', len(lines_hit))
print('样例行:', sorted(lines_hit)[:15])
