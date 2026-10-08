# -*- coding: utf-8 -*-
"""第二遍：把 08-faq.md 正文残留的精确行号改为'可 grep 命中'表述。"""
P08 = "/sandbox/workspace/libai/references/08-faq.md"
PAIRS = [
("（L3490—3495）", "（可 grep 命中『床前明月光』）"),
("（卷二乐府，L1270—1299）", "（卷二乐府；可 grep 命中『天生我材必有用』）"),
("《宣州谢朓楼饯别校书叔云》，L11710 一带", "《宣州谢朓楼饯别校书叔云》，可 grep『抽刀断水水更流』"),
("《月下独酌》，L15184 起", "《月下独酌》，可 grep『举杯邀明月』"),
("（L2274 起）、\"笑尽一杯酒", "（可 grep『少年学剑术』）、\"笑尽一杯酒"),
("（L1789 起）", "（可 grep『十步杀一人』）"),
("（L16509 起）", "（可 grep『为我一挥手』）"),
("（L15468 起）", "（可 grep『钟期久已没』）"),
("（L17105 起）", "（可 grep『何人不起故园情』）"),
("（L15611 起）", "（可 grep『相看两不厌』）"),
("（卷一，L38 起）", "（卷一；可 grep『自从建安来』）"),
("（卷十，L7044—7045）", "（卷十；可 grep『清水出芙蓉』）"),
("（卷二乐府，L1119 起）", "（卷二乐府；可 grep『蜀道之难』）"),
("**本集可验** L118 起）", "**本集可验**，可 grep『吾营紫河车』）"),
]
txt = open(P08, encoding="utf-8").read()
for old, new in PAIRS:
    c = txt.count(old)
    if c != 1:
        raise SystemExit("FAIL count=%d for: %s" % (c, old))
    txt = txt.replace(old, new)
open(P08, "w", encoding="utf-8").write(txt)
print("OK", len(PAIRS))
