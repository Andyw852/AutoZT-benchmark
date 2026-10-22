# MoS2 —— phonon + transport plots

本目录由 `kl-dft-cpu` 的 **S6.1_plot** 步骤自动生成（`run: gen`，不交作业）。

- `phonon_band/`：S5.1_plot 已算好的声子色散图**原样复制**（不改动、不重画）
- `kappa/`：S6_kappa 结果的 κL 图与表（ke 风格多面板）

## 收敛诊断（两类收敛分开看）

| 项 | 状态 | 说明 |
|---|---|---|
| q-mesh 收敛 | converged | 最细 138 138 1，最大相对变化 0.157% |
| FC3 截断收敛 | **not converged** | 采用 6.5 Å；κ 在数据能确定的范围内（≤ 6.50 Å）仍未到平台，报能确定范围内最大截断的 κ；更长程三阶项当前数据无法确定 |

> 两者是**不同**的收敛判据：q-mesh 决定 BTE 积分精度；FC3 截断决定三阶力常数的空间范围。

## 文件

- `phonon_band/band_nac.dat`
- `phonon_band/band_nac.path`
- `phonon_band/band_nac.png`
- `phonon_band/band_nac.yaml`
- `phonon_band/band_nac_lowfreq.png`
- `phonon_band/band_nonac.dat`
- `phonon_band/band_nonac.path`
- `phonon_band/band_nonac.png`
- `phonon_band/band_nonac.yaml`
- `phonon_band/band_nonac_lowfreq.png`
- `phonon_band/phonon_plot_summary.json`
- `kappa/MoS2_kl_overview.png`
- `kappa/MoS2_kl_anisotropy.png`
- `kappa/MoS2_kl_vs_T.csv`
- `kappa/MoS2_kl_summary.csv`
- `kappa/MoS2_kl_summary.json`

## 说明

- 声子谱图来自 S5.1_plot，保持技能原有出图不变；
- κL 原始值依赖 Lz；2D 归一化 κ·h/d 与 Lz 无关，跨算例可比；
- 2D 的 κzz 无物理意义（真空方向），仅作参考。
