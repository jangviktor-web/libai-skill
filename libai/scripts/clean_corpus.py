# -*- coding: utf-8 -*-
"""清洗李白诗全集：UTF-8 规范化 + 简体化（zhconv）+ 写入 modules/"""
import re

try:
    import zhconv
    def conv(s):
        return zhconv.convert(s, 'zh-cn')
    print('zhconv: enabled')
except Exception as e:
    def conv(s):
        return s
    print('zhconv: NOT available, skip ->', e)

src = '/sandbox/workspace/libai/李白诗全集.utf8.txt'
s = open(src, encoding='utf-8').read()
s = s.replace('\ufeff', '')
s = conv(s)
# 规范换行
s = s.replace('\r\n', '\n').replace('\r', '\n')

dst = '/sandbox/workspace/libai/modules/01_libai-shi-quanji.md'
open(dst, 'w', encoding='utf-8').write(s)

print('written:', dst)
print('chars:', len(s), 'lines:', s.count('\n') + 1)

# 卷次统计
juan = re.findall(r'卷[一二三四五六七八九十]+', s)
print('卷标记出现次数(含目录):', len(juan))

# 乱码/异常字符扫描（S15 P0/P1）
p0 = s.count('\ufffd')
print('U+FFFD(替换符) 数量:', p0)
import collections
weird = collections.Counter(ch for ch in s if ord(ch) > 0xFFFF)
print('增补平面字符(应极少):', sum(weird.values()))
