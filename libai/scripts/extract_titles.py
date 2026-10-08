# -*- coding: utf-8 -*-
"""提取本集所有诗题，用于与权威全集做差集"""
lines = open('/sandbox/workspace/libai/modules/01_libai-shi-quanji.md', encoding='utf-8').read().split('\n')

titles = []
for l in lines:
    s = l.strip()
    if not s:
        continue
    # 诗题：行以全角空格缩进，且不以句末「。」结尾
    if not (l.startswith('\u3000\u3000') or l.startswith('\u3000')):
        continue
    if s.endswith('。') or s.endswith(')') or s.endswith('）'):
        continue
    if s.startswith('(') or s.startswith('（'):
        continue
    if '一作' in s or '一　作' in s:
        continue
    if len(s) > 22:
        continue
    # 排除卷次/体裁行
    if s.startswith('卷') and len(s) <= 6:
        continue
    if s in ('古风五十九首', '乐府', '补遗'):
        continue
    titles.append(s)

# 去重保序
seen = set()
uniq = []
for t in titles:
    if t not in seen:
        seen.add(t)
        uniq.append(t)

print('候选诗题(去重):', len(uniq))
print('---全部---')
for i, t in enumerate(uniq, 1):
    print(f'{i}\t{t}')
