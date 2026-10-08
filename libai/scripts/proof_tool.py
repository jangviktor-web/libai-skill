#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""4 个残损段逐诗比对：权威源《李太白集》(王琦本)。输出带模块行号的可疑点。"""
import re, difflib
from collections import Counter

MOD = 'modules/01_libai-shi-quanji.md'
JI = 'refs/li_taibai_ji.txt'
PUNCT = set('，。、？！：；·…—～()（）《》〈〉“”‘’"\'【】〔〕　 \t\r\n,.:;?!"\'[]{}<>-—＊*○')

def clean(s):
    s = re.sub(r'【[^】]*】', '', s)
    s = re.sub(r'（[^）]*）', '', s)
    s = re.sub(r'\([^)]*\)', '', s)
    return ''.join(c for c in s if c not in PUNCT)

SECS = {'卷四': (2530, 3208), '卷十二': (8273, 8887),
        '卷十四': (9356, 10124), '卷二十': (13625, 14239)}

def parse_module(lines, a, b):
    poems, cur, in_note = [], None, 0
    for i in range(a - 1, b):
        s = lines[i].strip()
        if not s: continue
        op = s.count('(') + s.count('（'); cl = s.count(')') + s.count('）')
        if in_note > 0 or s.startswith('(') or s.startswith('（'):
            in_note += op - cl
            if cur: cur[2].append((i + 1, s))
            continue
        core = re.sub(r'【[^】]*】', '', s)
        core = re.sub(r'\([^)]*\)|（[^）]*）', '', core).strip()
        if not core:
            if cur: cur[2].append((i + 1, s))
            continue
        if re.search(r'[。？！]$', core):
            if cur: cur[2].append((i + 1, s))
        else:
            cur = [i + 1, core, []]
            poems.append(cur)
    return poems

def parse_ref(path):
    txt = open(path, encoding='utf-8').read().replace('\r', '')
    out, cur = [], None
    for ln in txt.split('\n'):
        if '○' in ln:
            cur = [ln.split('○', 1)[1].strip(), []]
            out.append(cur)
        elif cur is not None and ln.strip():
            cur[1].append(ln)
    return out

def strip_yizuo(s, L):
    return re.sub(r'一作[\u4e00-\u9fff]{1,%d}' % L, '', s)

def main():
    lines = open(MOD, encoding='utf-8').read().split('\n')
    jis = parse_ref(JI)
    refs = []
    for t, bl in jis:
        c = clean(''.join(bl))
        c = re.sub(r'李太白全集[^\n]*', '', c)
        refs.append((t, c))

    for sec, (a, b) in SECS.items():
        poems = parse_module(lines, a, b)
        print('#' * 12, sec, len(poems), 'poems')
        for start, title, body in poems:
            parts = [(start, clean(title))]
            for ln, txt in body:
                c = clean(txt)
                if c: parts.append((ln, c))
            mbody = ''.join(p[1] for p in parts)
            if len(mbody) < 8: continue
            cand = []
            for idx, (jt, jc) in enumerate(refs):
                if not jc: continue
                if abs(len(jc) - len(mbody)) > 0.30 * len(mbody): continue
                inter = sum((Counter(mbody) & Counter(jc)).values())
                cand.append((inter / len(mbody), idx))
            cand.sort(reverse=True)
            sub = False
            if not cand or cand[0][0] < 0.75:
                cand2 = []
                for idx, (jt2, jc) in enumerate(refs):
                    if not jc: continue
                    inter = sum((Counter(mbody) & Counter(jc)).values())
                    cand2.append((inter / len(mbody), idx))
                cand2.sort(reverse=True)
                if not cand2 or cand2[0][0] < 0.85:
                    v = cand[0][0] if cand else -1
                    print(f'  [{start}] LOW({v:.2f}) {title} nbody={len(mbody)}')
                    continue
                cand, sub = cand2, True
            bs, best = cand[0]
            jt, r0 = refs[best]
            best_r, best_sc = r0, -1
            for L in (1, 2, 3):
                rr = strip_yizuo(r0, L)
                sc = difflib.SequenceMatcher(None, mbody, rr, autojunk=False).ratio()
                if sc > best_sc: best_sc, best_r = sc, rr
            r = best_r
            # 去掉标题（偏置），仅比对正文
            tlen = len(parts[0][1])
            mb = mbody[tlen:]
            offs, pos = [], 0
            for ln, c in parts[1:]:
                offs.append((pos, pos + len(c), ln)); pos += len(c)
            def lineno(idx):
                for s0, e0, ln in offs:
                    if s0 <= idx < e0: return ln
                return offs[-1][2] if offs else start
            sm = difflib.SequenceMatcher(None, mb, r, autojunk=False)
            ops = sm.get_opcodes()
            # 子串模式：切除首尾未对齐区
            keep = list(range(len(ops)))
            if sub:
                eqs = [k for k, o in enumerate(ops) if o[0] == 'equal' and o[2] - o[1] > 2]
                if eqs: keep = list(range(eqs[0], eqs[-1] + 1))
            flags = []
            for k in keep:
                tag, i1, i2, j1, j2 = ops[k]
                if tag == 'equal': continue
                if tag == 'insert' and not r[j1:j2]: continue
                flags.append((tag, mb[i1:i2], r[j1:j2], lineno(i1)))
            if flags:
                print(f'  [{start}] {title}  ~ji:{jt} ({bs:.2f}{" sub" if sub else ""})')
                for tag, mm, rr, ln in flags:
                    print(f'      L{ln:<6} {tag:8s} MOD="{mm[:26]}"  JI="{rr[:26]}"')

if __name__ == '__main__':
    main()
