# AutoZT 基准测试数据（Benchmark）

AutoZT 工作流（[`autozt`](https://github.com/Andyw852/AutoZT) + `skill/`）的**可复现基准测试数据集**。
本仓库只保存**结果层**（图、表、JSON 汇总），不含原始 VASP 文件（OUTCAR/WAVECAR/CHGCAR/vasprun.xml 等）。

---

## 批次索引

| 批次 | 材料 | 技能 | 状态 |
|---|---|---|---|
| **单层 TMD**（4 材料） | MoS2 / WS2 / WSe2 / MoSe2 | ke-dft-cpu | ✅ 完成 |
| **正交相 2D**（2 材料） | CrS2_ortho / CrSe2_ortho | ke-dft-cpu | ✅ 完成 |
| **横向超晶格**（4 材料） | CrS2 / CrSe2 / SS / LS | ke-dft-cpu | CrS2/CrSe2/SS 完成，LS 进行中 |

---

## 一、结果层收录规则

对每个材料只复制以下扩展名的文件（其余为原始 VASP 产物，不上传）：

```
.json  .csv  .png  .txt  .md
```

**体积对比**：原始数据 10+ GB → 结果层约 **129 MB**（本仓库）。

---

## 二、六个基准材料（电子输运）

来源集群 jzzn（CPU），技能 `ke-dft-cpu`（全流程 step1_opt … step8.4_amset2d）。

| 材料 | 类型 | 原始大小 | 结果层 |
|---|---|---|---|
| MoS2 | 1H 单层 TMD | 3.0 GB | 25 MB |
| WS2 | 1H 单层 TMD | 2.4 GB | 20 MB |
| WSe2 | 1H 单层 TMD | 2.5 GB | 20 MB |
| MoSe2 | 1H 单层 TMD | 1.7 GB | 21 MB |
| CrS2_ortho | 正交相 2D | 80 MB | 13 MB |
| CrSe2_ortho | 正交相 2D | 77 MB | 13 MB |

### 目录结构

```
<材料>/
├── ke-dft-cpu/
│   ├── provenance/            各步骤溯源 JSON
│   ├── step1_opt/ … step7d_ivs_phonon/
│   │                          （每步只保留 .json/.csv/.png/.txt/.md 结果）
│   ├── step8.1_boltztrap/     BoltzTraP2 CRTA（σ/τ、S、κe/τ，100–900 K）
│   ├── step8.2_dpt/           形变势迁移率 DPT
│   ├── step8.3_output/        多温度汇总（comparison_vs_T.csv 等）
│   ├── step8.4_amset2d/       AMSET 2D
│   │   ├── transport.json          overall（ADP+POP+IMP）
│   │   ├── intrinsic_transport.json intrinsic（ADP+POP）
│   │   └── intrinsic_ADP.json      ADP only
│   └── transport_plots/       独立绘图输出（按浓度段拆文件夹，图 + 同目录表）
├── kl-dft-cpu/                （部分材料）晶格热导
├── step5_fc/ step5_phonon_plot/ step6_kappa/   （部分材料）声子/力常数结果
├── fitting_dataset/
└── pheasy-gpu_8methods/
```

### transport_plots 图怎么看

- **每张图**：行 = 温度（100–900 K）；列 = 5 个量 μ / S / σ / PF / κe
- **每个面板**：x = 载流子浓度 n (cm⁻³，负=n 型，正=p 型，signed-log)；y = 该面板的量
- **曲线**：
  - 蓝 = DPT 路线（S8.1 CRTA × DPT-τ）
  - 红 = AMSET overall（ADP+POP+IMP）
  - 绿/橙 = AMSET **ADP only**（来自 `intrinsic_ADP.json`）
  - DPT 带边迁移率横线（仅 μ 面板）
- **灰底**：刚性能带近似不成立的浓度段（超出每原子 0.02 载流子），只看趋势

---

## 三、横向超晶格批次（`superlattice/`）

**目标**：用当前版 `ke-dft-cpu` 重跑四个横向超晶格体系，复现并核对文献
**J. Appl. Phys. 139, 024301 (2026)** 的形变势迁移率。

| 缩写 | 结构 | 原子数 | 带隙 PBE | 文献带隙 |
|---|---|---|---|---|
| CrS2 | 1H-CrS2 单层（六方原胞） | 3 | 0.9448 eV | 0.936 |
| CrSe2 | 1H-CrSe2 单层（六方原胞） | 3 | 0.7600 eV | 0.751 |
| SS | CrS2/CrSe2 短周期横向超晶格 | 12 | 0.8185 eV | 0.816 |
| LS | CrS2/CrSe2 长周期横向超晶格 | 24 | 待算 | 0.790 |

**关键结论**（详见 [`superlattice/00_关键数据速览.md`](superlattice/00_关键数据速览.md)）：

1. **E1、C_2D 与文献差 <2%** —— 弹性常数与形变势计算正确
2. **m\* 系统性偏轻 5–10%** —— 是**定义差异**：我们用 q⁴ 外推到 q→0（真带边曲率），
   文献用有限窗口抛物线拟合（含非抛物性）。证据：[mstar_窗口扫描.csv](superlattice/01_对照表/mstar_窗口扫描.csv)
3. **用文献口径 m\* 重算后，μ 与文献差 ≤3%**（CrS2 −2.7%/−2.5%；CrSe2 0.0%/+2.8%）
4. **Seebeck 反推对照中位数偏差 +0.4%**（23 点）—— 能带/态密度物理正确
5. **σ 系统性偏高 1.62×** —— 厚度(6.54 vs 6.53 Å)与 τ 均已排除，疑为 BoltzTraP2 Ω 归一化口径
6. **ZT 未算** —— 缺晶格热导 κ_L（kl 链未跑）

---

## 四、数据规模与许可

- 仓库体积：约 **129 MB**（1435 文件），无单文件超过 4 MB
- 原始计算数据在集群：`jzzn:/public/home/wangchao/Fullerene_Network/work/`
- 引用文献：J. Appl. Phys. **139**, 024301 (2026); doi: 10.1063/5.0308349
- 引用文献图表时请遵循原出版方版权；本仓库数据用于复现与方法验证

---

## 五、待办

- [ ] LS 材料计算完成并补入
- [ ] 更多技能批次（kl-dft-cpu 全流程、phonon、defect 等）
