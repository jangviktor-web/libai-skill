# -*- coding: utf-8 -*-
"""按卷统计本集实际诗题数，与目录声明首数比对，定位缺口"""
import re

lines = open('/sandbox/workspace/libai/modules/01_libai-shi-quanji.md', encoding='utf-8').read().split('\n')

# 1) 目录声明
head = '\n'.join(lines[:40])
decl = re.findall(r'卷([一二三四五六七八九十]+)（([^）]+)）', head)
print('目录声明卷数:', len(decl))
for c, name in decl:
    print('  卷' + c, name)

# 2) 正文卷标题
juan = []
for i, l in enumerate(lines):
    s = l.strip()
    if re.fullmatch(r'卷[一二三四五六七八九十]+', s):
        juan.append((i, s))
print('\n正文卷标题数:', len(juan))
print('正文卷标题:', [s for _, s in juan])

# 3) 每卷诗题数
def is_title(l):
    s = l.strip()
    if not s or not l.startswith('\u3000'):
        return False
    if s.endswith('。') or s.endswith(')') or s.endswith('）'):
        return False
    if s.startswith('(') or s.startswith('（'):
        return False
    if '一作' in s or '一\u3000作' in s:
        return False
    if len(s) > 22:
        return False
    if s.startswith('卷'):
        return False
    return True

print('\n--- 各卷实际诗题数 ---')
bounds = [p for p, _ in juan] + [len(lines)]
for k in range(len(juan)):
    a, b = bounds[k], bounds[k + 1]
    cnt = sum(1 for l in lines[a:b] if is_title(l))
    print(f'  卷{juan[k][1][1:]:4s} 实际 {cnt:4d} 题')
