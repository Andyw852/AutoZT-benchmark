
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
def digit(mask, P):
    x0,x1,yt,yb = P["x0"],P["x1"],P["ytop"],P["ybot"]
    xs, ys = [], []
    for c in range(x0+3, x1-3):
        col = np.where(mask[yt+3:yb-2, c])[0]
        if len(col)==0: continue
        r = yt+3+int(np.median(col))
        u = -3.0 + (c-x0)/(x1-x0)*6.0
        ke = (yb-r)/(yb-yt)*250.0
        xs.append(u); ys.append(ke)
    return np.array(xs), np.array(ys)

def sample(u_arr, ke_arr, targets):
    o = np.argsort(u_arr)
    return np.interp(targets, u_arr[o], ke_arr[o])

TARGETS = [-2.5,-2.0,-1.5,-1.0,-0.5,0.5,1.0,1.5,2.0,2.5]
print("=== Fig. S3 数字化结果（kappa_e, W/mK）===")
out = {}
for mat,P in PANELS.items():
    ux,kx = digit(red,P)
    uy,ky = digit(blue,P)
    out[mat] = (sample(ux,kx,TARGETS), sample(uy,ky,TARGETS))
    print("  %-6s xx: %s" % (mat, " ".join("%.0f"%v for v in out[mat][0])))
    print("         yy: %s" % " ".join("%.0f"%v for v in out[mat][1]))
np.save("/tmp/figS3_digit.npy", np.array([out[m][0] for m in ("CrS2","CrSe2","SS","LS")]))
print()
print("u 采样点:", TARGETS)
