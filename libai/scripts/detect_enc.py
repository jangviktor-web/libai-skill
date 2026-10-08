p = '/sandbox/workspace/uploads/李白诗全集.txt'
data = open(p, 'rb').read()
print('total bytes:', len(data))
print('first 16 bytes hex:', data[:16].hex())
for enc in ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'gb2312', 'big5', 'utf-16', 'cp1252']:
    try:
        s = data.decode(enc)
        print('---', enc, 'OK  len=', len(s))
        print('    sample:', repr(s[:50]))
    except Exception as e:
        print('---', enc, 'FAIL', type(e).__name__, str(e)[:60])
