# CrSe2（1H-CrSe2 单层）

## 结构
- 六方原胞，P-6m2（#187），3 原子（1 Cr + 2 Se）
- a = b = 3.152 Å（弛豫后），c = 20 Å
- 来源：归档 S1 CONTCAR（PBE，external pressure −0.79 kB）

## 计算链
与 CrS2 相同：S1/S2/S5/S6 归档复用，S3/S4/S7+ 新算。
- PBE 带隙 0.760 eV（文献 0.751）
- S3 = 48×48×3（新算）

## 最终结果（300 K，DPT）

| 载流子 | 方向 | E1 (eV) | C_2D (N/m) | m* (m₀) | **μ (cm²/Vs)** | τ (fs) |
|---|---|---|---|---|---|---|
| 电子 | x/y | 5.201 | 99.204 | 0.9801 | **81.31** | 45.31 |
| 空穴 | x/y | 2.981 | 99.204 | 1.0073 | **234.34** | 134.21 |

补充（`dpt_result.json` 主口径，q⁴ m* = 0.980/1.007）：
- 电子 μ = **83.86**，空穴 μ = **246.10**

## 与文献偏差
- E1: −0.7%/−1.8%，C_2D: +0.5% ✅
- m*: −6.6%/−5.8%
- μ: +16%/+18%（文献口径 μ 偏差 0.0%/+2.8%）

## 文件
同 CrS2 结构。

## S8.1（BoltzTraP2 CRTA × DPT-τ）产物
见 `step8.1_boltztrap/`：boltztrap_crta.json / boltztrap_summary.txt / paper_mu_scan_600K.csv(png) / paper_at_doping_600K.csv。
对应文献 Fig. 5–7（σ/S/κ_e），不是 Table I 的 μ。ZT 缺 κ_L 未算。
