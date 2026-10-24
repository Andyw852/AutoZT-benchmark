
import numpy as np
from PIL import Image
a = np.asarray(Image.open("/tmp/figS3_embed_0.png").convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
red  = (R>150)&(G<110)&(B<110)
blue = (B>140)&(R<110)&(G<160)
PANELS = {
  "CrS2":  dict(x0=254, x1=1524, ytop=50,  ybot=853),
  "CrSe2": dict(x0=1790,x1=3099, ytop=50,  ybot=853),
  "SS":    dict(x0=254, x1=1524, ytop=1090,ybot=1893),
  "LS":    dict(x0=1790,x1=3099, ytop=1090,ybot=1893),
}
def digit(mask, P, legend_frac=0.30):
    x0,x1,yt,yb = P["x0"],P["x1"],P["ytop"],P["ybot"]
    H = yb-yt
    xs, ys = [], []
    for c in range(x0+3, x1-3):
        u = -3.0 + (c-x0)/(x1-x0)*6.0
        col = np.where(mask[yt+3:yb-2, c])[0] + yt+3
        if len(col)==0: continue
        # 图例区：u>0.55 且 ke>170（占面板上部 32%）-> 排除
        if u > 0.55:
            col = col[(yb-col)/H*250.0 < 170]
        if len(col)==0: continue
        r = int(np.median(col))
        xs.append(u); ys.append((yb-r)/H*250.0)
    return np.array(xs), np.array(ys)
def sample(ua, ka, tg):
    o=np.argsort(ua); return np.interp(tg, ua[o], ka[o])
TARGETS=[-2.5,-2.0,-1.5,-1.0,-0.5,0.5,1.0,1.5,2.0,2.5]
print("=== Fig. S3 κe（数字化，已排除图例）W/mK ===")
print("%-6s %-6s %s" % ("材料","方向"," ".join("%5.1f"%t for t in TARGETS)))
dig={}
for mat,P in PANELS.items():
    ux,kx = digit(red,P); uy,ky = digit(blue,P)
    dig[mat]=dict(xx=sample(ux,kx,TARGETS), yy=sample(uy,ky,TARGETS))
    print("%-6s %-6s %s" % (mat,"xx"," ".join("%5.0f"%v for v in dig[mat]["xx"])))
    print("%-6s %-6s %s" % ("","yy"," ".join("%5.0f"%v for v in dig[mat]["yy"])))
np.savez("/tmp/figS3_digit.npz", targets=TARGETS, **{m+"_"+d: dig[m][d] for m in dig for d in dig[m]})
