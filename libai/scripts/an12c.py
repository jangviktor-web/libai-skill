import re, collections

path = '/sandbox/workspace/libai/modules/01_libai-shi-quanji.md'
raw = open(path, encoding='utf-8').read()
lines = raw.split('\n')
n = len(lines)
freq = collections.Counter(ch for ch in raw if '\u4e00' <= ch <= '\u9fff')


def clean(s):
    s = re.sub(r'[（(][^（()）]*[)）]', '', s.strip())
    s = re.sub(r'[（()）]', '', s)
    return s.strip()


def isgarbage(s):
    chs = [c for c in s if '\u4e00' <= c <= '\u9fff']
    if not chs:
        return True
    return sum(1 for c in chs if freq[c] <= 2) >= 2


tpos = []
for i, l in enumerate(lines):
    if l.startswith('\u3000\u3000') and l.strip():
        t = l.strip()
        if t.endswith(('。', '，', '？', '！', '、', '；')) or len(t) > 14:
            continue
        if i + 1 < n and lines[i + 1].strip() == '':
            tpos.append((i + 1, t))
tpos.append((n, 'END'))
punct = re.compile(r'[，。？！、；：]')
poems = {}
for k in range(len(tpos) - 1):
    start, title = tpos[k]
    end = tpos[k + 1][0]
    body, ok = [], True
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
    if body and ok:
        poems[(start, title)] = [len(punct.sub('', b)) for b in body]

# 分区统计 (卷六-卷二十四 古近体诗 = 3858..17899)
def seg(a, b):
    return {k: v for k, v in poems.items() if a <= k[0] < b}


def stat(d, name):
    c = collections.Counter()
    for t, lens in d.items():
        nl = len(lens)
        if all(x == 5 for x in lens):
            k = {4: '五绝型', 8: '五律型'}.get(nl, '五言齐言多句')
        elif all(x == 7 for x in lens):
            k = {4: '七绝型', 8: '七律型'}.get(nl, '七言齐言多句')
        elif all(x in (5, 7) for x in lens):
            k = '五七杂言'
        else:
            k = '杂言长短句'
        c[k] += 1
    tot = sum(c.values())
    print("\n##", name, "共", tot)
    for k, v in c.most_common():
        print("  %-10s %4d  %5.1f%%" % (k, v, v / tot * 100))
    return c


print("=== 卷一 古风 ===")
stat(seg(34, 1062), '卷一 古诗(古风五十九首)')
print("=== 卷二-卷五 乐府 ===")
stat({k: v for k, v in poems.items() if 1062 <= k[0] < 3858}, '卷二～卷五 乐府')
print("=== 卷六-卷二十四 古近体诗 ===")
stat(seg(3858, 17899), '卷六～卷二十四 古近体诗')
print("=== 卷二十五 补遗 ===")
stat({k: v for k, v in poems.items() if k[0] >= 17899}, '卷二十五 补遗')

# 重点篇目行式
targets = ['远别离', '蜀道难', '将进酒', '行路难三首', '关山月', '静夜思', '早发白帝城',
           '赠孟浩然', '渡荆门送别', '送友人', '独坐敬亭山', '望庐山瀑布', '黄鹤楼送孟浩然之广陵',
           '秋浦歌', '月下独酌', '宣州谢朓楼饯别校书叔云', '梦游天姥吟留别', '日出入行 ( 一作日出行 )',
           '长相思', '北风行', '侠客行', '子夜吴歌', '金陵酒肆留别', '客中行', '山中问答', '春夜洛城闻笛']
print("\n\n=== 重点篇目行式 ===")
for (pos, t), lens in poems.items():
    for tg in targets:
        if t == tg or t.startswith(tg):
            print("%-28s 句数=%d  句长分布=%s" % (t, len(lens), dict(collections.Counter(lens))))
            break
