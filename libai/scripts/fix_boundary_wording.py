# -*- coding: utf-8 -*-
"""幂等最终修复：(1) 边界表述；(2) 并发写入残留：字面 \\xNN 转义串还原、补回被吞的「升格」。"""
import os, re

B = "/sandbox/workspace/libai"
ALL = ["references/02-creation-heuristics.md", "references/07-literary-lineage.md",
       "cases/00_index.md", "cases/01_gufeng-yuefu.md", "cases/02_jinti-jueju.md"]

WORD = {
 "references/02-creation-heuristics.md": [
  ("下表基于源文件全文（159246 字符，含诗题、异文校记、少量目录与乱码章节，属**相对序位证据**）：",
   "下表基于源文件全文（**修复前**文本 159246 字符，含诗题、异文校记、少量目录；原卷四／卷十二／卷十四／卷二十的整段编码损坏**已修复**，本集现为完整诗本 1010 首，本表频次属修复前统计、未重算），属**相对序位证据**："),
  ("乐府（句式长短不齐、多换韵；卷四源文件有乱码，取证慎用）",
   "乐府（句式长短不齐、多换韵；原卷四编码损坏已修复，本卷可正常检索引用）"),
  ("（《李白诗全集》二十五卷，UTF-8，18340 行）", "（《李白诗全集》二十五卷，UTF-8，修复后 18350 行）"),
  ("自我形象的\"\"装置", "自我形象的\"升格\"装置"),
  ("9. **发露／含蓄按体裁分工**：歌行直说，绝句留白（§8.3）。\n9. **发露／含蓄按体裁分工**：歌行直说，绝句留白（§8.3）。",
   "9. **发露／含蓄按体裁分工**：歌行直说，绝句留白（§8.3）。"),
 ],
 "references/07-literary-lineage.md": [
  ("> - 卷次标注以源文件可见的\"卷N\"标记为准；源文件缺失卷首标记者（卷四、卷十二、卷十四、卷二十等），标\"卷次待考\"。",
   "> - 卷次标注以源文件可见的\"卷N\"标记为准。原因编码损坏而卷首不全的卷四、卷十二、卷十四、卷二十**现已修复**，二十五卷卷首标记齐全，全部引诗均可标卷次（可用 `grep -n \"^卷十三$\" modules/01_libai-shi-quanji.md` 一类命令复核）。"),
  ("（《寄崔侍御》·卷次待考）", "（《寄崔侍御》·卷十三）"),
  ("（《赠僧行融》·卷次待考）", "（《赠僧行融》·卷十一）"),
  ("- **卷十三**：谢公行处苍苔没。：8915（《庐山谣寄卢侍御虚舟》）\n",
   "- **卷十三**：谢公行处苍苔没。：8915（《庐山谣寄卢侍御虚舟》）｜ 过客难登谢朓楼。：9218（《寄崔侍御》）｜ 三山怀谢朓。：9291（《三山望金陵寄殷淑》）\n"),
  ("（缩进与句读按源文件）；冒号后为源文件行号。",
   "（缩进与句读按源文件）；冒号后为源文件行号（均为修复后文本行号，可用 `grep -n \"引句\"` 复核；若源文件再作编辑，行号可能整体偏移）。"),
 ],
 "cases/00_index.md": [
  ("本集卷四等有个别编码乱码行，本库引句均取自可正常检索区。",
   "原卷四、卷十二、卷十四、卷二十的整段编码损坏**已修复**，本集现为完整诗本（25 卷 · 1010 首），名篇齐备，本库引句均可正常检索引用。"),
  ("`03_missing-pieces.md`（本集缺失名篇 18 篇）。", "`03_missing-pieces.md`（本集未收篇目 5 篇 · 附编码修复说明）。"),
  ("另列缺失名篇 18 篇。", "另列本集真未收篇目 5 篇（见 `03_missing-pieces.md`）。"),
  ("若需引用《梦游天姥吟留别》等名篇，须先查 `03_missing-pieces.md`。",
   "本集名篇齐备（《梦游天姥吟留别》《望庐山瀑布》《黄鹤楼送孟浩然之广陵》《清平调》等均已在集）；确需引用本集未收的 5 篇（见 `03_missing-pieces.md`）时，须注明外部来源，**不得冒充本集原文**。"),
 ],
}

RUN = re.compile(rb"(?:\\x[0-9a-fA-F]{2}){4,}")


def unescape(bs):
    try:
        return bytes(int(bs[i + 2:i + 4], 16) for i in range(0, len(bs), 4))
    except Exception:
        return bs


for rel in ALL:
    p = os.path.join(B, rel)
    raw = open(p, "rb").read()
    for old, new in WORD.get(rel, []):
        ob, nb = old.encode(), new.encode()
        if ob in raw:
            raw = raw.replace(ob, nb); print("[word] %-38s %s" % (rel, old[:20]))
    for h in set(RUN.findall(raw)):
        print("[esc ] %-38s %s -> %s" % (rel, h[:66].decode("ascii", "replace"), unescape(h)))
    raw = RUN.sub(lambda m: unescape(m.group(0)), raw)
    if "\"\"装置".encode() in raw:
        print("[char] %-38s 补回「升格」" % rel)
        raw = raw.replace("\"\"装置".encode(), "\"升格\"装置".encode())
    open(p, "wb").write(raw)

print("--- final verify ---")
for rel in ALL:
    raw = open(os.path.join(B, rel), "rb").read()
    try:
        raw.decode("utf-8"); ok = "UTF-8 OK"
    except UnicodeDecodeError as e:
        ok = "UTF-8 BAD %s" % e
    t = raw.decode("utf-8", "replace")
    old = {k: t.count(k) for k in ["乱码", "缺失名篇", "18340 行", "卷次待考"] if t.count(k)}
    print("%-42s %-13s 行数=%-5d 旧词=%s 升格=%d 燕山雪花=%d 名篇齐备=%d 已修复=%d" %
          (rel, ok, t.count("\n") + 1, old or "无", t.count("升格"), t.count("燕山雪花"),
           t.count("名篇齐备"), t.count("已修复")))
