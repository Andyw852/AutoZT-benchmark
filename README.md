# AutoZT 基准测试数据（Benchmark）

AutoZT 工作流（`autozt` + `skill/`）的**可复现基准测试数据集**。
每个子目录是一个基准测试批次，包含完整的逐步计算数据、结果表、图与说明文档。

> 上游软件：https://github.com/Andyw852/AutoZT

---

## 批次索引

| 批次 | 材料 | 技能 | 状态 | 说明 |
|---|---|---|---|---|
| [`superlattice/`](superlattice/README.md) | CrS2 / CrSe2 / SS / LS（横向超晶格） | ke-dft-cpu | CrS2/CrSe2/SS 完成，LS 进行中 | PBE 全链 + DPT + AMSET + BoltzTraP2；对照 JAP 139,024301 (2026) |

（历史批次：MoS2 / WS2 / WSe2 / MoSe2 / CrS2_ortho / CrSe2_ortho —— 待整理上传，见下）

---

## superlattice 批次（本仓库当前内容）

**目标**：用当前版 `ke-dft-cpu` 技能重跑四个横向超晶格体系，复现并核对文献 Table I 的形变势迁移率。

**四个材料**：
| 缩写 | 结构 | 原子数 | 带隙 PBE | 文献带隙 |
|---|---|---|---|---|
| CrS2 | 1H-CrS2 单层（六方原胞） | 3 | 0.9448 eV | 0.936 |
| CrSe2 | 1H-CrSe2 单层（六方原胞） | 3 | 0.7600 eV | 0.751 |
| SS | CrS2/CrSe2 短周期横向超晶格 | 12 | 0.8185 eV | 0.816 |
| LS | CrS2/CrSe2 长周期横向超晶格 | 24 | 待算 | 0.790 |

**关键结论**（详见 `superlattice/00_关键数据速览.md`）：
1. **E1、C_2D 与文献差 <2%** —— 弹性常数与形变势计算正确
2. **m\* 系统性偏轻 5–10%** —— 是**定义差异**：我们用 q⁴ 外推到 q→0（真带边曲率），
   文献用有限窗口抛物线拟合（含非抛物性）。证据见 `superlattice/01_对照表/mstar_窗口扫描.csv`
3. **用文献口径 m\* 重算后，μ 与文献差 ≤3%**（CrS2 −2.7%/−2.5%；CrSe2 0.0%/+2.8%）
4. **Seebeck 反推对照中位数偏差 +0.4%**（23 点）—— 能带/态密度物理正确
5. **σ 系统性偏高 1.62×** —— 厚度(6.54 vs 6.53 Å)与 τ 均已排除，疑为 BoltzTraP2 Ω 归一化口径
6. **ZT 未算** —— 缺晶格热导 κ_L（kl 链未跑）

---

## 目录约定

```
<批次>/
├── README.md               批次说明
├── 00_关键数据速览.md        关键数字速览（推荐先看）
├── 01_对照表/               与文献/其他来源的对照表（CSV）
├── 02_各材料最终结果/
│   └── <材料>/
│       ├── dpt_result.json       S8.2 DPT 完整结果
│       ├── transport.json        S8.4 AMSET 完整结果
│       ├── comparison_300K.png   S8.3 对比图
│       ├── step8.1_boltztrap/    S8.1 σ/S/κe/PF
│       ├── transport_plots/      9 个温度的 DPT 参数表
│       └── provenance/           各步骤溯源（输入指纹/命令/耗时）
└── 03_计算参数/               step.conf 配置副本
```

## 数据规模与许可

- 体积：约 15 MB（JSON/CSV/PNG，不含原始 OUTCAR/WAVECAR）
- 原始计算数据在集群：`jzzn:/public/home/wangchao/Fullerene_Network/work/superlattice/`
- 引用文献：J. Appl. Phys. **139**, 024301 (2026); doi: 10.1063/5.0308349
- 本仓库数据用于复现与方法验证，引用文献图表时请遵循原出版方版权

---

## 待办

- [ ] LS 材料计算完成并补入（S7 形变帧进行中）
- [ ] 历史 6 材料批次（MoS2/WS2/WSe2/MoSe2/CrS2_ortho/CrSe2_ortho）整理上传
- [ ] kl 链补跑后可计算 ZT
