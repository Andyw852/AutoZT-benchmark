# MoS2 单层 - pheasy-gpu 8 方法力常数拟合 + 晶格热导率 基准

> 本目录是 AutoZT 基准测试下 MoS2 的**晶格**热导率基准（lattice kappa）。电子热导率（AMSET）见同级 MoS2-test/。

## 1. 体系与口径

- 材料：单层 MoS2（3 原子原胞），超胞 5x5x1 = **75 原子**。
- 训练数据：**36** 个随机位移构型（力由 DFT 给出；帧 #36 为理想结构）。
- 拟合引擎：**pheasy-gpu**（3090，CUDA/torch，压缩感知力常数拟合）。
- 拟合模型：fc2 不截断 + fc3 截断 c3 扫描 {3.54, 4.19, 4.73, 5.24, 5.86, 6.50} A，自由 IFC 数 171→1294。
- kappa 计算：phono3py 三声子 BTE（**RTA**，同位素散射开，NAC 关，q 网格固定 **18x18x1**，真空轴压成 1）。
- 2D 层厚归一化：d = 6.7177 A，因子 **3.7215**（kl-dft-cpu S6 口径）；kappa_zz 对 2D 无物理意义。
- 温度：100-800 K（步长 100 K）。

## 2. 计算步骤（目录对应）

| 步骤 | 目录 | 内容 |
|---|---|---|
| S1 结构 | ../step1_std_opt/（已有） | VASP 弛豫 |
| S4 位移/力 | ../fitting_dataset/、fit-fc-thermal/ | 36 构型 dataset_*.npy |
| S5 拟合 | step5_fc/ | pheasy-gpu 8 方法 x 6 截断 |
| S6 kappa | step6_kappa/ | phono3py BTE，每方法每截断一次 |
| 截断选择 | step6_kappa/<方法>/cutoff_selection.json | 三判据自动选截断 |
| 汇总 | summary/ | 对比表 + kappa(T) + 绘图数据总表 |

## 3. 拟合结果（S5，in-sample 相对误差 %）

| 方法 | 3.54 | 4.19 | 4.73 | 5.24 | 5.86 | 6.50 |
|---|---|---|---|---|---|---|
| OLS | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| RIDGE | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| LASSO | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| ALASSO | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| RFE-OLS | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| RFE-OLS-TSQR | 0.602 | 0.542 | 0.388 | 0.304 | 0.285 | 0.258 |
| ARDR | 0.602 | 0.542 | 0.387 | 0.303 | 0.284 | 0.257 |
| RVM | 0.602 | 0.543 | 0.388 | 0.305 | 0.287 | 0.264 |

自由 IFC 数（所有方法相同）：171 / 238 / 340 / 568 / 798 / 1294（对应 6 个截断）。所有方法都通过 pheasy 的 atom-order 对齐闸（worst per-config corr = 1.0000）。

## 4. 热导率结果（S6，kappa_inplane 2D 归一化，W/mK）

### 4.1 kappa vs fc3 截断（每方法一张 2x2 图 kappa_vs_cutoff.png：(a) kxx | (b) kzz（2D 留空框） / (c) kyy | (d) 力 RMSE；底部图注区标注方法名（仅方法名，不带引擎前缀））

| 方法 | 3.54 | 4.19 | 4.73 | 5.24 | 5.86 | 6.50 |
|---|---|---|---|---|---|---|
| OLS | 132.2 | 124.1 | 121.7 | 96.6 | 84.4 | 80.1 |
| RIDGE | 133.5 | 124.0 | 123.0 | 97.8 | 82.9 | 80.4 |
| LASSO | 133.3 | 125.1 | 121.8 | 101.8 | 89.5 | 98.6 |
| ALASSO | 134.6 | 122.8 | 115.1 | 97.0 | 84.3 | 86.9 |
| RFE-OLS | 142.1 | 103.5 | 101.3 | 85.2 | 71.1 | 75.3 |
| RFE-OLS-TSQR | 135.4 | 121.1 | 119.4 | 92.6 | 80.6 | 82.2 |
| ARDR | 132.8 | 124.7 | 121.8 | 96.9 | 84.5 | 80.4 |
| RVM | 136.5 | 122.9 | 115.5 | 97.6 | 87.4 | 89.9 |

### 4.2 选中截断的 kappa(300 K) 对比

| 方法 | 选中截断 (Å) | 判据状态 | kappa_xx=yy (300K) | kappa_inplane (300K) | kappa_2D (300K) |
|---|---|---|---|---|---|
| OLS | 6.5 | not_converged | 21.528 | 21.528 | 80.12 |
| RIDGE | 5.86 | ok | 22.267 | 22.267 | 82.87 |
| LASSO | 6.5 | not_converged | 26.493 | 26.493 | 98.59 |
| ALASSO | 5.86 | ok | 22.644 | 22.644 | 84.27 |
| RFE-OLS | 6.5 | not_converged | 20.223 | 20.223 | 75.26 |
| RFE-OLS-TSQR | 5.86 | ok | 21.669 | 21.669 | 80.64 |
| ARDR | 5.86 | ok | 22.717 | 22.717 | 84.54 |
| RVM | 5.86 | ok | 23.476 | 23.476 | 87.37 |

### 4.3 kappa(T) 面内（W/mK，未做层厚归一）

| 方法 | 100 K | 200 K | 300 K | 400 K | 500 K | 600 K | 700 K | 800 K |
|---|---|---|---|---|---|---|---|---|
| OLS | 74.31 | 33.20 | 21.53 | 16.06 | 12.84 | 10.72 | 9.21 | 8.07 |
| RIDGE | 74.55 | 34.12 | 22.27 | 16.66 | 13.35 | 11.16 | 9.59 | 8.41 |
| LASSO | 97.52 | 41.35 | 26.49 | 19.67 | 15.71 | 13.10 | 11.24 | 9.85 |
| ALASSO | 74.25 | 34.57 | 22.64 | 16.96 | 13.61 | 11.38 | 9.78 | 8.58 |
| RFE-OLS | 66.47 | 30.94 | 20.22 | 15.12 | 12.11 | 10.11 | 8.68 | 7.61 |
| RFE-OLS-TSQR | 70.64 | 33.04 | 21.67 | 16.24 | 13.03 | 10.89 | 9.37 | 8.22 |
| ARDR | 76.03 | 34.81 | 22.72 | 16.99 | 13.62 | 11.38 | 9.79 | 8.59 |
| RVM | 78.21 | 35.95 | 23.48 | 17.56 | 14.08 | 11.76 | 10.11 | 8.87 |

## 5. 结论

1. **拟合精度**：8 个方法相对误差都 <=0.61%，随截断增大单调下降到 ~0.26%；ARDR/RVM（稀疏贝叶斯）与 OLS/RIDGE 同级。
2. **kappa 收敛性**：RIDGE、ALASSO、RFE-OLS-TSQR、ARDR、RVM 在 **5.86 A** 达到平台（status=ok）；OLS、LASSO、RFE-OLS 到最大截断 6.50 A 仍在下降（not_converged，报能确定范围内的最大值）。
3. **kappa(300 K) 面内排序**（选中截断）：RFE-OLS 20.22 < OLS 21.53 < RFE-OLS-TSQR 21.67 < RIDGE 22.27 < ALASSO 22.64 < ARDR 22.72 < RVM 23.48 < LASSO 26.49 W/mK。
4. **稀疏化并不单调降低 kappa**：LASSO（未去偏）kappa 最高，RFE-OLS 最低；去偏/求解口径对 kappa 影响可达 ~20%，比较时必须同口径。
5. **ARDR / RVM** 需要 pheasy-gpu 第九轮修复（--std 下 y 标准化、RVM alpha->inf 处理、lambda_t 分组 CV）；修复后二者从 ~7.8%/不收敛 降到 0.26%，kappa 与其它方法同量级。

## 6. 文件说明

- step5_fc/fit_metrics_by_cutoff.csv|json —— **S5 汇总**：8 方法 x 6 截断的 free_ifcs / in-sample 相对误差 / 方程数除以参数数 / 稳定性字段。
- step5_fc/<方法>/ —— cutoff_scan.json（该方法截断扫描原始记录）+ cutoff_selection.json + fit_manifest.json（若有）+ 选中截断的 fc2.hdf5 / fc3.hdf5。
- step6_kappa/kappa_vs_cutoff_all.csv|json —— **8 张 kappa-vs-cutoff 图的绘图数据总表**（每方法每截断的 kappa_xx/yy/inplane/2D归一/平台标志）。
- step6_kappa/<方法>/ —— kappa_vs_cutoff.png / .pdf（**2x2 期刊风格图**：(a) kxx (b) kzz (c) kyy (d) 力 RMSE；底部图注区标注方法名（仅方法名，不带引擎前缀））、kappa_vs_cutoff.json（**该图的绘图数据**）、cutoff_selection.json（选截断依据）、kappa_summary.json（选中截断完整 kappa，含 kappa(T)、张量、2D 归一）、kappa_config.json（计算参数）。
- summary/comparison_table.csv|json —— 8 方法选中截断的 kappa(300 K) 对比。
- summary/kappa_vs_T_all_methods.csv —— 8 方法 x 8 温度的 kappa(T) 绘图数据。

## 7. 口径与坑（务必注意）

- **去偏口径**：本表 LASSO / ALASSO 为 PHEASY_LASSO_DEBIAS=0 的原始解。去偏（debias=1）会显著改变 kappa，历史值：LASSO 26.49->22.66、ALASSO 23.35->20.83 W/mK。跨方法比较前必须统一去偏设置。
- **截断选择判据**：cut3_select 三判据中，判据①（残差 1-SE）输入是 in-sample 残差、不具否决权；判据②（逐壳层稳定性）因 CUT3_BOOTSTRAP=0 未测；**实际只有判据③（相邻截断 kappa 平台）在筛选**，与其他方法一致。
- **phono3py 版本**：本目录所有 kappa 均用 **phono3py 3.24.0** 计算，保证 8 方法同口径可直接叠比。
- **kappa 的网格固定 18x18x1**，未做网格收敛；绝对值随网格会变，方法间**相对**比较可靠。
- **右下角力 RMSE 的来源**：本基准没有 S1 的原生 FIT_RMSE_FRAMES 输出，用 train_rel_err × RMS(F) 还原（RMS(F)=0.370929 eV/A，36 帧）；已用 ARDR/RVM fit_manifest 的 rmse 校验，比值 0.370930 完全一致。
- pheasy-gpu 版本：第八轮（RFE->RFE-OLS）+ 第九轮（ARDR/RVM 修复），见 pheasy-gpu 仓库 main 的 24e4ac9、783e9ea。
