# -*- coding: utf-8 -*-
import re, json

def norm(s):
    out=[]
    for c in s:
        o=ord(c)
        if c=='?': out.append('?')
        elif 0x4e00<=o<=0x9fff or 0x3400<=o<=0x4dbf: out.append(c)
    return ''.join(out)

base='/sandbox/workspace/libai/'
refs=[('ji','refs/li_taibai_ji.txt'),('wenji','refs/li_taibai_wenji.txt'),('qts','refs/quan_tang_shi.txt')]
src=[(k,norm(open(base+r,encoding='utf-8',errors='replace').read())) for k,r in refs]

def norm2map(s):
    out=[];m=[]
    for i,c in enumerate(s):
        o=ord(c)
        if c=='?' or 0x4e00<=o<=0x9fff or 0x3400<=o<=0x4dbf:
            out.append(c);m.append(i)
    return ''.join(out),m

lines=open(base+'modules/01_libai-shi-quanji.md',encoding='utf-8').read().split('\n')
res=[]
for li,l in enumerate(lines):
    if '?' not in l: continue
    if '<!--' in l: continue
    n,m=norm2map(l)
    for pos,c in enumerate(n):
        if c!='?': continue
        # context window: up to 6 norm chars, cut at parens
        left=n[max(0,pos-6):pos]; right=n[pos+1:pos+1+6]
        # cut right at '一作' end? keep
        pat=re.escape(left)+'.'+re.escape(right)
        cand={}
        for k,s in src:
            found=set()
            for mm in re.finditer(pat,s):
                found.add(mm.group()[len(left)])
            if found: cand[k]=sorted(found)
        res.append(dict(line=li+1, ctx=n[max(0,pos-8):pos+9], left=left,right=right, cand=cand,
                        line_text=l.strip()))
for r in res:
    print(f"{r['line']}\t{r['line_text'][:34]}\tctx={r['ctx']}\tL={r['left']} R={r['right']}\t{r['cand']}")
print('total',len(res))
