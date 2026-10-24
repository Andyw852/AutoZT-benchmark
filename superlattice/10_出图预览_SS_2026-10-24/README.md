# 10_出图预览（SS 材料，2026-10-24，含 [0079]+[0080] 修复）

> 用**本地补图工具**基于归档旧结果生成，**没有重跑任何计算**。
> 目的是验收 [0079]（机制命名）和 [0080]（标题/图注精简 + 分段）这两轮出图修复。

## 生成方式

```bash
# 1) 组装一个"材料目录"：真实步骤目录用符号链接，S8.4 补回归档的 transport.json
mkdir -p /tmp/prev2/ke
for d in <项目>/SS/ke-dft-cpu/result/*/; do ln -s "$d" /tmp/prev2/ke/$(basename "$d"); done
cp <归档>/02_各材料最终结果/SS/transport.json /tmp/prev2/ke/step8.4_amset2d/
cp <项目>/SS/literature/SS_literature_600K.csv /tmp/prev2/literature/

# 2) 补图（不碰超算）
python3 skill/ke-dft-cpu/tools/make_transport_plots.py /tmp/prev2/ke /tmp/prev2/plots SS
```

## 目录（25 张图 + 57 个 CSV）

| 目录 | 内容 | 对应修复 |
|---|---|---|
| `mu_compare/` | σ/S/PF/κe/μ 随化学势 u：三方对比 + 加机制，各 5 张 | [0078] 新增 |
| `mobility_mechanisms_carrier_tuning_1e16-1e22/` | 掺杂段：μ 按散射机制拆（ADP / POP / IMP / ADP+POP+IMP） | **[0079] 命名修复** |
| `mobility_mechanisms_low_doping_1e10-1e15/` | **近本征段单独一张** | **[0080] 分段修复** |
| `transport_models_carrier_tuning_1e16-1e22/` | 掺杂段：σ/S/PF/κe 各机制 | [0079]+[0080] |
| `transport_models_low_doping_1e10-1e15/` | 近本征段 | **[0080]** |
| `temperature_series/` | 每个数据集一张，**文件名用机制组合**：`SS_ADP+POP+IMP_*`、`SS_ADP+POP_*`、`SS_ADP_*`、`SS_BT2_DPTtau_*` | **[0079]** |
| `intrinsic_carrier/` | 本征浓度 + 稀薄极限迁移率 | — |
| `mu_scan/` | μ − E_VBM 扫描 | — |
| `SS_params_<T>K.csv` | 每温度参数表 | — |

## 两轮修复的具体体现

### [0079] 图例按实际散射机制组合命名

- 以前：`phonon + impurity` / `phonon-limited`（含糊，不知道具体含哪几种机制）
- 现在：**`ADP+POP+IMP`**（全机制）、**`ADP+POP`**（去 IMP）、**`ADP`**（仅形变势）
- 单机制直接写 `ADP` / `POP` / `IMP`
- 实线 = AMSET 一次运行含该组合；虚线 = AMSET 单机制；点划线 = DPT(ADP) 带边值（写在各面板顶部）

### [0080] 标题/图注精简 + 分段

- 标题只写「材料 + 是什么 + 范围/温度」，例如：
  - `SS  mobility by scattering mechanism  (n = 1e16 - 1e22 cm⁻³, 100-900 K)`
  - `SS  σ vs chemical potential, 600 K`
- 图注压到 2–4 行：只写 AMSET/BT2×DPT-τ 各是什么、机制缩写、横轴口径、灰底含义
- 去掉了 `together` 之类含糊词，总值直接写机制组合
- **横轴是掺杂浓度的图分段**：`*_carrier_tuning_1e16-1e22/` 与 `*_low_doping_1e10-1e15/` 分开
- **横轴是化学势的图（mu_scan / mu_compare）两段画在一起**（浓度在上横轴）

## ⚠️ 注意：这是旧网格预览

| 项 | 预览里显示 | 重跑 S8.4 后（[0077] 新网格） |
|---|---|---|
| 掺杂段范围 | 1e16 – **1e22** | 1e16 – **1e21**（23 档） |
| 近本征段 | 1e10 – 1e15（只有 3 个点：1.5e10/1.5e12/1.5e14） | **1e11 – 1e15（每十年一个点，5 个）** |
| AMSET 机制子集 | 来自旧运行 | 新运行会有完整子集 |

AMSET 数据来自归档旧结果（旧层厚 6.9731 Å），σ 的绝对值比新结果高 3.6%。
