# -*- coding: utf-8 -*-
"""重写 02_buyi.md：只保留本集确未收的篇目"""
import re

s = open('/sandbox/workspace/libai/modules/02_buyi.md', encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=## )', s)

keep_keys = ['折荷有赠', '别匡山', '菩萨蛮', '忆秦娥', '桂殿秋']
kept = []
for b in blocks:
    m = re.match(r'## (.+)', b)
    if not m:
        continue
    t = m.group(1).strip()
    if t.startswith('【') or t.startswith('附'):
        continue
    if '春夜宴' in t:
        continue  # 序文，另处理
    if any(k in t for k in keep_keys):
        kept.append(b.rstrip())

hdr = '''# 《李白诗全集》补遗（本集确未收篇目 · 网补）

> 说明：用户上传本集经**编码修复后已为完整诗本（25 卷 · 1010 首）**，名篇齐备（《梦游天姥吟留别》《望庐山瀑布》《黄鹤楼送孟浩然之广陵》《清平调》《南陵别儿童入京》等均已在集内）。
> 下列篇目经核验**确不在本集**，据《李太白集》《全唐诗》等权威源补录，供检索引用。均为本集所无者，非重复。
> ⚠️ 引用时以本文件为「补遗」，与正典 `modules/01_libai-shi-quanji.md` 区分。

'''

out = hdr + '\n'.join(kept) + '\n'
open('/sandbox/workspace/libai/modules/02_buyi.md', 'w', encoding='utf-8').write(out)
print('保留篇数:', len(kept), '->', keep_keys)
print('行数:', out.count('\n') + 1)
print(out[:900])
