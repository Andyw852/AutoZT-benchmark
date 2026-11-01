# CrS2（1H-CrS2 单层）

## 结构
- 六方原胞，P-6m2（#187），3 原子（1 Cr + 2 S）
- a = b = 3.038 Å（弛豫后），c = 20 Å（真空）
- 来源：归档 S1 CONTCAR（PBE 弛豫，external pressure −0.78 kB）

## 计算链
| 步骤 | 来源 | 说明 |
|---|---|---|
| S1_opt | 归档复用 | PBE，收敛 |
| S2.1 / S2.15 / S2.155 / S2.2_pbe / S2.2_pbe_plot | 归档复用 | PBE 带隙 0.9448 eV（文献 0.936） |
| S3_uniform | **新算** | 48×48×3（旧版 15×15×1 不合规） |
| S4_wave | 新算 | wavefunction.h5 |
| S5_dielect / S6_elastic | 归档复用 | INCAR 与当前一致 |
| S7_deform（10 帧）+ S7.1_read | **新算** | 形变势 |
| S8.2_dpt / S8.1_bt2 / S8.4_amset2d / S8.3_cmp | **新算** | 最终结果 |

## 最终结果（300 K，DPT）

| 载流子 | 方向 | E1 (eV) | C_2D (N/m) | m* (m₀) | **μ (cm²/Vs)** | τ (fs) |
|---|---|---|---|---|---|---|
| 电子 | x/y | 5.975 | 121.219 | 0.8858 | **92.16** | 46.41 |
| 空穴 | x/y | 3.165 | 121.219 | 0.8913 | **324.40** | 164.39 |

补充（`dpt_result.json` 主口径，q⁴ 外推 m* = 0.869/0.879）：
- 电子 μ = **95.76**，空穴 μ = **333.79**

AMSET 多机制（300 K 本征，`transport.json`）：
- ADP: 213.4 / 209.3（x/y）；POP: 214.2 / 212.6；IMP 可忽略
- **overall: 92.6 / 91.7**

## 与文献偏差
- E1: +0.5%，C_2D: +0.5% ✅
- m*: −5.6%（q→0）〜 +1%（文献口径 0.9498，文献 0.98/0.90）
- μ: +12%（文献口径 −2.7%）

## 文件
- `dpt_result.json` — S8.2 完整结果（含 provenance）
- `transport.json` — S8.4 AMSET 完整结果（19 掺杂 × 9 温度 × 3 机制）
- `comparison_300K.png` — S8.3 对比图
- `transport_plots/CrS2_params_{100..900}K.csv` — 9 个温度的 DPT 参数

## S8.1（BoltzTraP2 CRTA × DPT-τ）产物
`step8.1_boltztrap/`：
- `boltztrap_crta.json` — 完整输运系数（σ/τ, S, κ_e/τ, PF/τ vs μ）
- `boltztrap_summary.txt` — 摘要（300 K PF/τ 峰值等）
- `paper_mu_scan_600K.csv/png` — 文献口径（600 K，σ/S/κ_e 用 DPT τ）
- `paper_at_doping_600K.csv` — 按掺杂对齐

**ZT 未算**：缺晶格热导 κ_L（kl 链未跑）。
**τ 来自单谷 DPT**：600 K 电子占 97.7%、空穴占 59.3%（其余谷/谷间散射未计入）。

