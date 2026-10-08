# -*- coding: utf-8 -*-
"""建立 forward(X)=G 的逆向候选表，并对破损区逐字验证。"""
import zhconv, json, sys

def forward(x):
    """原文 X -> 破损字 G"""
    try:
        g = x.encode('gbk').decode('euc-jp', 'strict')
    except Exception:
        return None
    return zhconv.convert(g, 'zh-hans')

def build_reverse(path):
    rev = {}
    for i in range(0x81, 0xFF):
        for j in range(0x40, 0xFF):
            if j == 0x7F: continue
            try:
                x = bytes([i, j]).decode('gbk')
            except Exception:
                continue
            if len(x) != 1: continue
            g = forward(x)
            if g and len(g) == 1:
                rev.setdefault(g, set()).add(x)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({k: sorted(v) for k, v in rev.items()}, f, ensure_ascii=False)
    return rev

if __name__ == "__main__":
    rev = build_reverse("/sandbox/workspace/libai/scripts/reverse_map.json")
    print("rev size", len(rev))
    for g in "卯页咢采鲷湘爷嚏邦斜苧承朔":
        print(g, "->", "".join(sorted(rev.get(g, []))))
