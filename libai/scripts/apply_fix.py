# -*- coding: utf-8 -*-
"""补正 modules/01_libai-shi-quanji.md 中的残留 ?（自动解 + 人工判定）"""
import re, collections

p='/sandbox/workspace/libai/modules/01_libai-shi-quanji.md'
lines=open(p,encoding='utf-8').read().split('\n')

# ---------- 1) 由权威源自动对齐得到的解 ----------
auto={}
r3=open('/sandbox/workspace/libai/fix_q3_output.txt',encoding='utf-8').read()
recs=collections.defaultdict(list)
for ln in r3.split('\n'):
    parts=ln.split('\t')
    if len(parts)<5: continue
    try: lineno=int(parts[0])
    except Exception: continue
    try: d=eval(parts[4])
    except Exception: d={}
    recs[lineno].append(d)
for lineno,ds in recs.items():
    chars=[];ok=True
    for d in ds:
        pick=None
        for k in ('ji','wenji','qts'):
            v=d.get(k)
            if v and len(v)==1:
                if pick is None: pick=v[0]
        if pick is None: ok=False
        chars.append(pick)
    if ok: auto[lineno]=chars

# ---------- 2) 人工判定（覆盖/补充自动解） ----------
manual={
 2538:['霄'], 2575:['翕'], 2667:['萧'], 2699:['香'],
 2850:['酩','酊','襄'], 2871:['襄'], 2899:['翡'], 2915:['向'], 2937:['相'],
 2977:['想','想'], 2984:['香'], 2994:['香'], 3015:['，'],
 3061:['霄','霄'], 3145:['巉'],
 8391:['霁','繇'], 8393:['霁'], 8487:['衾','羲'], 8515:['羡'],
 8524:['(',' )'.strip()], 8868:['限'], 8869:['想','像'], 9373:['，'], 9416:['(',' )'.strip()],
 9484:['翔'], 9660:['(',' )'.strip()], 9817:['(',' )'.strip()],
 9827:['香'], 9828:['，'], 9951:['鳌'], 10012:['鲵'], 10026:['相','相'],
 13683:['向','向'], 13691:['踟','蹰'], 13769:['，'], 13845:['想','像'],
 13947:['('], 13970:['('], 14016:['羡','跻'], 14056:['龌','龊'], 14088:['('],
 14165:['(',' )'.strip()], 14227:['翔','晓'],
}
rep=dict(auto); rep.update(manual)

# 无语源、保留 ? 的行
keep={3075,3124,14087}

# 整行/整段替换的特例
special={2968:('天人弄彩玉葩?','天人弄彩球。'),
         14077:('东流自潺诅葩?','东流自潺湲。')}

# 校验：除 keep/special 外，所有含 ? 的行都必须在 rep 中且长度匹配
missing=[]
for i,l in enumerate(lines):
    if i==0 or '?' not in l: continue
    n=i+1
    if n in keep or n in special: continue
    if n not in rep or len(rep[n])!=l.count('?'):
        missing.append((n,l.strip(),l.count('?'),rep.get(n)))
if missing:
    raise SystemExit('UNRESOLVED: '+repr(missing))

log=[]
for ln in sorted(rep):
    if ln in keep or ln in special: continue
    txt=lines[ln-1]; chars=rep[ln]
    assert txt.count('?')==len(chars)
    out=[]
    for ch in chars:
        i=txt.index('?'); out.append(txt[:i]); out.append(ch); txt=txt[i+1:]
    out.append(txt)
    new=''.join(out); assert '?' not in new
    lines[ln-1]=new; log.append((ln,''.join(chars)))

for ln,(old,new) in special.items():
    txt=lines[ln-1]; assert old in txt, (ln,txt,old)
    lines[ln-1]=txt.replace(old,new); log.append((ln,new.strip()))

# 删除第 1 行 HTML 注释
assert lines[0].startswith('<!--')
del lines[0]

rest=[(i+1,lines[i]) for i in range(len(lines)) if '?' in lines[i]]
app=[]
app.append('## 附：未修复残字清单')
app.append('')
app.append('本集原文件 4 段（卷四/十二/十四/二十，行 2530–3202 / 8273–8880 / 9356–10118 / 13625–14233）曾因 GBK 字节被误按 EUC-JP 解码而整段损坏；'
           '逆变换复原后，个别字符在损坏阶段即已丢失（显示为 `?`），权威源（《全唐诗》《李太白集》《李太白文集》）所载此三首均无对应异文可考，故保留原样：')
app.append('')
for n,t in rest:
    app.append(f'- 第 {n} 行：`{t.strip()}`')
app.append('')
app.append('> 说明：其余含 `?` 之处的补正依据为上述三种权威源（异文取与本书体例相合者）；'
           '损坏阶段一并丢失的全角标点（括号、逗号）已按本集体例补为半角括号/逗号，如「梦游天姥吟留别 (一作别东鲁诸公)」。')
app.append('')
open(p,'w',encoding='utf-8').write('\n'.join(lines)+'\n'+'\n'.join(app))
print('replaced count(处):',len(log))
print('replaced lines:',len(set(l for l,_ in log)))
print('remaining ?:',rest)
