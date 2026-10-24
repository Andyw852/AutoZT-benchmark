# 10_mu_compare 预览（SS 材料，2026-10-24）

> 这是 **S8.3 [0078] 新出图功能的预览**，用归档里的旧结果 + 本地补图工具生成，
> **没有重跑任何计算**。

## 怎么生成的

```bash
# 1) 用项目里现有的 result 目录（S8.1/S8.2 是新鲜的，S8.4 用归档里的旧 transport.json）
cp -r <项目>/SS/ke-dft-cpu/result /tmp/prev_full/ke
cp <归档>/02_各材料最终结果/SS/transport.json /tmp/prev_full/ke/step8.4_amset2d/
cp <项目>/SS/literature/SS_literature_600K.csv /tmp/prev_full/literature/

# 2) 本地补图（不碰超算、不重跑计算）
python3 skill/ke-dft-cpu/tools/make_transport_plots.py /tmp/prev_full/ke /tmp/prev_full/plots SS
```

## 产物（600 K，10 张图 + 1 张数据表）

| 文件 | 内容 |
|---|---|
| `SS_sigma_vs_u_600K.png` | σ 三方对比（BT2×DPT-τ / AMSET ADP only / 文献） |
| `SS_S_vs_u_600K.png` | Seebeck |
| `SS_PF_vs_u_600K.png` | 功率因子 |
| `SS_kappa_e_vs_u_600K.png` | 电子热导 |
| `SS_mu_vs_u_600K.png` | 迁移率 |
| `*_mechanisms_600K.png` | 同上 5 个量，再加 AMSET 各机制组合（本轮旧结果没有子集文件，机制图只有全机制一条） |
| `SS_vs_u_600K.csv` | 图里每条曲线的数据 |

## 版式（[0078]）

- 横轴：化学势 u（**带隙中点 = 0**），下排把带边附近放大到 ±1 eV
- 上横轴：载流子浓度 |n|（3D 等效，2D 按层厚 t 归一，与 [0077] 同口径）
- 每列一个方向（xx / yy）
- 蓝实线 = BT2×DPT-τ；橙点 = AMSET ADP only；灰虚线 = 文献
- 粉底 = AMSET 掺杂网格覆盖范围；灰底 = 深能带区（离带边 >0.5 eV）

## 这张图直接印证了之前的结论

| 量 | 看图结论 |
|---|---|
| **S** | 蓝线与灰虚线**几乎完全重合**（峰 ±600 µV/K 位置、形状都对） |
| **σ** | 蓝线系统性高于灰虚线 —— 与"σ 偏高 1.5–2×"一致 |
| PF / κe | 继承 σ 的偏差（PF = S²σ、κe = L·σ·T） |

## ⚠️ 注意

- AMSET 数据来自**归档的旧结果**（19 档掺杂、旧层厚 6.9731 Å），不是最新代码；
  要完整的新版图必须重跑 S8.4（[0077] 新网格 23 档）
- 机制图（`*_mechanisms_600K.png`）只有全机制一条 —— 旧结果没开 WRITE_MESH，没有子集文件
- 文献 PF 的 yy 方向在 u≈1.3–1.6 eV 有个矩形尖峰，来自原始数字化数据，未修改
