# 09_复核材料 —— 供第三方复核 σ/PF/κe 偏差用

> 目的：把"复核 σ 1.62× 偏差"所需的**原始数据、数字化中间产物、数字化脚本**集中放在一处，
> 让复核者不用重跑计算、也不依赖我的口头结论就能自己验证。
>
> 主文档：[`../08_σ偏差复核_2026-10-24.md`](../08_σ偏差复核_2026-10-24.md)

---

## 目录

```
09_复核材料/
├── 能带/                          S2.2 输出的能带路径数据（判 K–Γ 用）
│   ├── CrS2_band.dat / .json
│   ├── CrSe2_band.dat / .json
│   └── SS_band.dat / .json
├── K-Gamma/
│   └── K_vs_Gamma_价带.csv       我们算的 K 谷与 Γ 谷价带位置
├── 输运原始/                      S8.1 的逐化学势扫描输出（σ/S/PF/κe 的源头）
│   ├── CrS2_paper_mu_scan_600K.csv
│   ├── CrSe2_paper_mu_scan_600K.csv
│   └── SS_paper_mu_scan_600K.csv
└── 数字化/                        文献图的位图 + 我的数字化脚本 + 结果图
    ├── 文献Fig4_能带图.jpeg       正文 Fig. 4（能带 + DOS）
    ├── 文献Fig4a_CrS2能带_放大.png
    ├── 文献Fig4b_CrSe2能带_放大.png
    ├── 文献Fig4a_Γ区放大.png
    ├── 文献Figs3_kappa_e位图.png  SI Fig. S3（κe）
    ├── 数字化_Figs3_kappa_e.py    我用的数字化脚本
    ├── 数字化_Fig4_能带.py        能带图数字化（**结果不可靠，见下**）
    └── 数字化_Figs3_初版.py
```

---

## 各文件怎么用

### 1. `能带/*_band.dat`

格式（S2.2 输出）：
```
# functional: PBE
# k-distance(1/Angst)  E-E_VBM(eV) x N bands
   kdist   E1  E2  ...  EN
```
- 能量**已经以 VBM 为零点**
- 路径：CrS2/CrSe2 是 Γ–M–K–Γ；SS 是 Γ–X–S–Y–Γ（见同目录 `band_summary.json` 的 `labels_found`）
- 首尾两点都是 Γ（可交叉验证）

**复核点**：读 `top = max over bands with E<=0`，比较首点（Γ）与最高点（K）。

### 2. `K-Gamma/K_vs_Gamma_价带.csv`

我的计算结果（两个独立来源一致：本目录的 band.dat + S3 均匀网格 EIGENVAL）：

| 材料 | E_V(Γ) − E_VBM(K) |
|---|---|
| CrS2 | −0.0888 eV |
| CrSe2 | −0.1972 eV |
| SS | −0.1265 eV |

**待复核**：文献 Fig. 4(a)(b) 里 Γ 点价带顶的位置。我看图读数是 CrS2 ≈ −0.49 eV、
CrSe2 ≈ −0.44 eV（相对 VBM），但**我自己的机器数字化结果自相矛盾**（同一面板读出的
"K 点价带顶"高于所谓 VBM），所以这条**没有下结论**。

### 3. `输运原始/*_paper_mu_scan_600K.csv`

S8.1 按文献口径（thickness 归一化，乘 c/t）的逐化学势扫描，列含：
`mu_rel_efermi_eV, carrier_conc_cm-3, n_2D_cm-2, branch, tau_xx_fs, tau_yy_fs,
S_xx_uV/K, S_yy_uV/K, sigma_xx_S/m, sigma_yy_S/m, sheet_sigma_xx_S, sheet_sigma_yy_S,
PF_xx_W/mK2, PF_yy_W/mK2, kappa_e_WF_xx_W/mK, kappa_e_WF_yy_W/mK`

- 单位：σ 是 S/m（thickness 口径）、S 是 µV/K、PF 是 W/mK²、κe 是 W/mK
- Γ 相关：**u < 0 → branch = hole（p 型）**；u > 0 → electron（n 型）
- κe 就是 L·σ·T（自检 `ke/(L·σ·T)` 中位 = 1.000），**不含独立信息**

**复核点**：把它和 `01_对照表/文献数字化_FIG5_sigma.csv`、`文献数字化_FIG7_PF.csv`
按 **同一 |S|** 配对，就得 σ(S) 比值。

### 4. `数字化/`

- `文献Figs3_kappa_e位图.png`：SI Fig. S3 原始位图（4 个子图，红实线 xx、蓝虚线 yy）
- `数字化_Figs3_kappa_e.py`：我用的脚本（帧线定位 + 颜色掩膜 + 图例排除 + 轴刻度标定）
- 数字化结果：`01_对照表/文献数字化_Figs3_kappa_e.csv`

**已知精度问题**：位图数字化，误差约 ±3 W/mK；且 κe 表是按 u 逐点比的，
u 零点敏感（例如 CrS2 u=−1.5 处在尖谷旁，差几十 meV 能差 3 倍）。
**所以 κe 不作为判据**，只用于验证 WF 定律。

- `文献Fig4*_能带图` + `数字化_Fig4_能带.py`：能带图数字化的尝试。
  **结论：不可靠** —— 论文里能带曲线很细，颜色掩膜抓不全，读数在同一面板内自相矛盾。
  保留这些文件是为了让复核者看到我做了什么、在哪里卡住，**不要引用其数值**。

---

## 复核者可以独立做的三件事

1. **验证 σ(S) 比值**：用 `输运原始/` + `01_对照表/文献数字化_*` 重算，看是否复现
   "n 支 0.97–1.49、p 支 0.74–1.87"
2. **验证 K–Γ**：读 `能带/*_band.dat` 复算三点，看是否 88.8 / 197.2 / 126.5 meV
3. **判文献能带图**：直接看 `数字化/文献Fig4*_能带*png`，人工读 Γ 点价带顶。
   如果你能读出可靠数值，这一条就从"待核"变成"已定位"或"已排除"

---

## 还没有的

- **文献能带的数值数据**：只有位图，没有原始数据。若有作者提供的能带数据/补充表，可直接对比
- **SI Fig. S3 的原始数据**：同上，只有位图
- **ENCUT=550 / 真空 15 Å 的重算**：未做（改基准材料会让 S4/S8.4 失效；如需验证要单独 register 测试材料）
