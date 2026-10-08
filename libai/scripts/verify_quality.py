# -*- coding: utf-8 -*-
"""Phase 3 质量验证：维度覆盖 + 死链检查 + 编码健康"""
import re, os

base = '/sandbox/workspace/libai/'
sk = open(base + 'SKILL.md', encoding='utf-8').read()

refs = sorted(set(re.findall(r'references/[\w\-\.]+\.md', sk)))
mods = sorted(set(re.findall(r'modules/[\w\-\.]+\.md', sk)))
print('SKILL.md 引用 references 文件:', len(refs))
for r in refs:
    print('   ', r, '存在' if os.path.exists(base + r) else '❌死链')

print('SKILL.md 引用 modules 文件:', len(mods))
for m in mods:
    print('   ', m, '存在' if os.path.exists(base + m) else '❌死链')

actual_refs = sorted(os.listdir(base + 'references'))
print('\nreferences/ 实际文件数:', len(actual_refs))
idx = [f for f in actual_refs if f[:2].isdigit()]
print('维度文件:', idx)

# 覆盖检测：实际文件是否都被 SKILL.md 引用
missing_in_sk = [f for f in actual_refs if ('references/' + f) not in sk]
print('未被 SKILL.md 索引的 references 文件:', missing_in_sk or '无 ✓')

# 行数统计
print('\n--- 各文件行数 ---')
for d in ['references', 'modules', 'scripts', 'cases']:
    p = base + d
    if os.path.isdir(p):
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            if os.path.isfile(fp):
                n = sum(1 for _ in open(fp, encoding='utf-8', errors='replace'))
                print(f'{d}/{f:42s} {n:6d} 行')
