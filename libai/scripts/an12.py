import re, collections, json

lines = open('/sandbox/workspace/libai/modules/01_libai-shi-quanji.md', encoding='utf-8').read().split('\n')
n = len(lines)


def clean(s):
    s = re.sub(r'[（(].*?[)）]', '', s.strip())
    return s.strip()


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
    return v


punct = re.compile(r'[，。？！、；：]')
poems = []
for k in range(len(tpos) - 1):
    start, title = tpos[k]
    end = tpos[k + 1][0]
    body = []
    for l in lines[start + 1:end - 1]:
        s = clean(l)
        if not s:
            continue
        if re.fullmatch(r'[一二三四五六七八九十]+', s):
            continue
        body.append(s)
    if not body:
        continue
    lens = [len(punct.sub('', b)) for b in body]
    v = volof(start)
    poems.append((v, title, len(body), lens))

print("poems parsed:", len(poems))
cnt = collections.Counter(v for v, _, _, _ in poems)
for v, c in cnt.items():
    print(v, c)


def cls(nl, lens):
    if all(l == 5 for l in lens):
        if nl == 4: return '五言四句(五绝型)'
        if nl == 8: return '五律型'
        if nl > 8 and nl % 2 == 0: return '五言排律/长律型'
        return '五言古/乐府'
    if all(l == 7 for l in lens):
        if nl == 4: return '七言四句(七绝型)'
        if nl == 8: return '七律型'
        if nl > 8 and nl % 2 == 0: return '七言排律型'
        return '七言古/歌行'
    if all(l in (3, 5) for l in lens): return '三五言杂言'
    if all(l in (5, 7) for l in lens): return '五七杂言'
    return '杂言(长短句)'


g = collections.Counter()
by_vol = collections.defaultdict(collections.Counter)
for v, t, nl, lens in poems:
    c = cls(nl, lens)
    g[c] += 1
    by_vol[v][c] += 1
print("\n=== GLOBAL ===")
for k, v in g.most_common():
    print(k, v)
print("\n=== BY VOL ===")
for v in [x[1] for x in vols] + ['卷二十五']:
    if v in by_vol:
        print(v, dict(by_vol[v]))

json.dump([(v, t, nl, max(lens), min(lens)) for v, t, nl, lens in poems],
          open('/tmp/poems.json', 'w'), ensure_ascii=False)

# list of 4-line 5-char and 4-line 7-char poems (potential 绝句)
print("\n=== 4句5言 ===")
print([t for v, t, nl, lens in poems if nl == 4 and all(l == 5 for l in lens)])
print("\n=== 4句7言 ===")
print([t for v, t, nl, lens in poems if nl == 4 and all(l == 7 for l in lens)])
print("\n=== 8句5言 ===")
print([t for v, t, nl, lens in poems if nl == 8 and all(l == 5 for l in lens)])
print("\n=== 8句7言 ===")
print([t for v, t, nl, lens in poems if nl == 8 and all(l == 7 for l in lens)])
