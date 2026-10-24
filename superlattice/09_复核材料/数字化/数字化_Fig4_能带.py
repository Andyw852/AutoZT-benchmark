import numpy as np
from PIL import Image
a = np.asarray(Image.open("/tmp/paper_p8_img0.jpeg").convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
Y0, Y1 = 32, 830
E0Y = Y0 + 0.5*(Y1-Y0)          # E=0 行
def e_of(y): return 3.0 - (y-Y0)/(Y1-Y0)*6.0
red  = (R>140)&(G<130)&(B<130)
dark = (R<160)&(G<160)&(B<160)
def top_curve(mask, xs, ybot, ytop_off=8):
    d = {}
    for x in xs:
        ys = np.where(mask[int(E0Y)+ytop_off:ybot, x])[0]
        if len(ys): d[x] = int(E0Y)+ytop_off+ys.min()
    return d
def report(name, d, gx0, gx1):
    if not d: print(name, '空'); return
    xs = sorted(d); ev = [e_of(d[x]) for x in xs]
    iK = int(np.argmax(ev))
    gvals = [ev[i] for i,x in enumerate(xs) if gx0<=x<=gx1]
    gE = max(gvals) if gvals else float('nan')
    print('%-8s VBM 在 x=%d E=%.3f | Γ 附近价带顶 E=%.3f | ΔE(K-Γ)=%.3f eV' % (name, xs[iK], ev[iK], gE, ev[iK]-gE))
# 面板 a: x 213..798, Γ 在左端
da = top_curve(red, range(213, 799), 820)
report('CrS2(a)', da, 213, 240)
# 面板 b: 找到左边框
cols = ((R<100)&(G<100)&(B<100)).sum(axis=0)
cands = [i for i in range(1000,1300) if cols[i] > 500]
x0 = cands[0] if cands else 1150
print('(b) 左边框 x =', x0)
db = top_curve(dark, range(x0+6, x0+690), 820)
report('CrSe2(b)', db, x0+6, x0+40)