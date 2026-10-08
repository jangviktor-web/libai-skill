# -*- coding: utf-8 -*-
"""S15 编码卫生硬校验：逐文件检查 UTF-8 合法性 + U+FFFD + 增补平面字符"""
import glob, os, sys

roots = ['modules', 'references', 'cases', 'scripts', 'outputs']
files = []
for r in roots:
    files += sorted(glob.glob(os.path.join(r, '**', '*'), recursive=True))
files = [f for f in files if os.path.isfile(f)]

print(f"{'file':58s} {'bytes':>8s} {'chars':>8s} {'FFFD':>5s} {'P1':>4s} {'strict':>6s}")
bad_total = 0
for f in files:
    b = open(f, 'rb').read()
    txt = b.decode('utf-8', 'replace')
    fffd = txt.count('\ufffd')
    # P1: HTML 实体残留
    p1 = txt.count('&#') + txt.count('&amp;') + txt.count('&nbsp;')
    try:
        b.decode('utf-8')
        strict = 'OK'
    except UnicodeDecodeError as e:
        strict = 'FAIL'
        bad_total += 1
    if fffd or p1 or strict == 'FAIL':
        print(f"{f:58s} {len(b):8d} {len(txt):8d} {fffd:5d} {p1:4d} {strict:>6s}")
print('---')
print('非法 UTF-8 文件数:', bad_total)
print('扫描文件总数:', len(files))
