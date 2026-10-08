import re, collections, json

path = '/sandbox/workspace/libai/modules/01_libai-shi-quanji.md'
raw = open(path, encoding='utf-8').read()
lines = raw.split('\n')
n = len(lines)

freq = collections.Counter(ch for ch in raw if '\u4e00' <= ch <= '\u9fff')
# suspicious lines
susp = [False] * n
for i, l in enumerate(lines):
    chs = [c for c in l if '\u4e00' <= c <= '\u9fff']
    if len(chs) >= 3:
        rare = sum(1 for c in chs if freq[c] <= 2)
        if rare >= 2 and rare / len(chs) > 0.4:
            susp[i] = True
# contiguous blocks
blocks = []
i = 0
while i < n:
    if susp[i]:
        j = i
        while j + 1 < n and (susp[j + 1] or (lines[j + 1].strip() == '' )):
            j += 1
        if j - i >= 4:
            blocks.append((i + 1, j + 1))
        i = j + 1
    else:
        i += 1
print("OCR噪声区块:", blocks)


def bad(pos):
    return any(a <= pos <= b for a, b in blocks)


def clean(s):
    s = re.sub(r'[（(][^（()）]*[)）]', '', s.strip())
    s = re.sub(r'[（()）]', '', s)
    return s.strip()


def isgarbage(s):
    chs = [c for c in s if '\u4e00' <= c <= '\u9fff']
    if not chs:
        return True
    rare = sum(1 for c in chs if freq[c] <= 2)
    return rare >= 2


tpos = []
for i, l in enumerate(lines):
    if l.startswith('\u3000\u3000') and l.strip():
        t = l.strip()
        if t.endswith(('。', '，', '？', '！', '、', '；')):
            continue
        if len(t) > 14:
            continue
        if i + 1 < n and lines[i + 1].strip() == '':
            tpos.append((i + 1, t))
tpos.append((n, 'END'))

vols = [(34, '卷一'), (1062, '卷二'), (1820, '卷三'), (3208, '卷五'), (3858, '卷六'),
        (4464, '卷七'), (5074, '卷八'), (5972, '卷九'), (6681, '卷十'), (7514, '卷十一'),
        (8887, '卷十三'), (10124, '卷十五'), (10677, '卷十六'), (11324, '卷十七'),
        (11903, '卷十八'), (12689, '卷十九'), (14239, '卷二十一'), (15096, '卷二十二'),
        (15805, '卷二十三'), (16818, '卷二十四'), (17899, '卷二十五')]


def volof(pos):
    v = None
    for s, name in vols:
        if pos >= s:
            v = name
    return v or '卷二十五'


punct = re.compile(r'[，。？！、；：]')
poems = []
for k in range(len(tpos) - 1):
    start, title = tpos[k]
    end = tpos[k + 1][0]
    if bad(start):
        continue
    body = []
    ok = True
    for l in lines[start + 1:end - 1]:
        s = clean(l)
        if not s:
            continue
        if re.fullmatch(r'[一二三四五六七八九十]+', s) or re.fullmatch(r'其[一二三四五六七八九十]+', s):
            continue
        if isgarbage(s):
            ok = False
            break
        body.append(s)
    if not body or not ok:
        continue
    lens = [len(punct.sub('', b)) for b in body]
    if any(l == 0 or l > 12 for l in lens):
        continue
    poems.append((volof(start), title, len(body), lens))
print("清洗后诗篇数:", len(poems))


def cls(nl, lens):
    if all(l == 5 for l in lens):
        if nl == 4: return 'A 五言四句(绝句型)'
        if nl == 8: return 'B 五言八句(律句型)'
        if nl > 8 and nl % 2 == 0: return 'C 五言多句齐言'
        return 'D 五言古体'
    if all(l == 7 for l in lens):
        if nl == 4: return 'E 七言四句(绝句型)'
        if nl == 8: return 'F 七言八句(律句型)'
        if nl > 8 and nl % 2 == 0: return 'G 七言多句齐言'
        return 'H 七言古体'
    if all(l in (5, 7) for l in lens): return 'I 五七杂言'
    if all(l in (3, 5) for l in lens): return 'J 三五言'
    return 'K 杂言长短句'


g = collections.Counter()
byv = collections.defaultdict(collections.Counter)
for v, t, nl, lens in poems:
    c = cls(nl, lens)
    g[c] += 1
    byv[v][c] += 1
print("\n=== 全书结构统计 ===")
for k in sorted(g):
    print(k, g[k])
tot = sum(g.values())
print("合计", tot, "；杂言类占比 %.1f%%" % ((g['K 杂言长短句'] + g['I 五七杂言'] + g['J 三五言']) / tot * 100))
print("四句+八句近体候选 %d (%.1f%%)" % (g['A 五言四句(绝句型)'] + g['B 五言八句(律句型)'] + g['E 七言四句(绝句型)'] + g['F 七言八句(律句型)'],
      (g['A 五言四句(绝句型)'] + g['B 五言八句(律句型)'] + g['E 七言四句(绝句型)'] + g['F 七言八句(律句型)']) / tot * 100))
print("\n=== 分卷 ===")
for v in [x[1] for x in vols] + ['卷二十五']:
    if v in byv:
        print(v, dict(sorted(byv[v].items())))

# 乐府区 titles
tau = [t for v, t, nl, lens in poems if 1062 <= [s for s, nm in vols if nm == v][0] < 3858]
print("\n乐府区(卷二-卷五)篇数:", sum(1 for v, t, nl, lens in poems if v in ('卷二', '卷三', '卷五')))
print("\n=== 乐府/古风区标题 ===")
print([t for v, t, nl, lens in poems if v in ('卷二', '卷三', '卷五')])

json.dump([(v, t, nl) for v, t, nl, lens in poems], open('/tmp/p2.json', 'w'), ensure_ascii=False)
