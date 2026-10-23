# DPT 修复重算验证（[0069] / [0071] / [0061-m] A1）

> 时间：2026-10-23
> 相关提交：
> - `439f176` **[0069]** S8.2 3D 多谷 DPT（谷轴形变势）
> - `185d02e` **[0071]** S8.2 2D 面内各向异性谷的表头 m\* 改用 m_d
> - `53c580c` **[0061-m] A1** S7 写波函数 / S7.1 build 形变势矩阵 / S8.4 用 DFT 矩阵做 ADP
> - `a134fd3` **[0067]** S7 只补静态段 + **S7.1 对称补应变标签改正**（3/4/6 次轴 xy/xz 互换）

---

## 一、[0069] 3D 多谷 DPT —— 不影响 2D

**重算结果（2026-10-23 01:20）**：CrS2/CrSe2/SS 三个材料 μ **0.0000% 变化**，仅 skill_rev 更新。

代码依据：`_valley_axis_3d` 只在 `e3`（3D 形变势）非空时调用，2D 体系该函数返回 None；
L2550 显式 `not is_2d` 判断。commit message 也写明"单谷、简并带边、2D 不变"。

---

## 二、[0071] 2D 表头 m\* 改用 m_d —— 只影响 SS

| 材料 | 载流子 | 表头 m\* 旧→新 | 表头 μ 旧→新 | 变化 |
|---|---|---|---|---|
| CrS2 | 电子 | 0.869 → 0.869 | 95.76 → 95.76 | 0.00% |
| CrS2 | 空穴 | 0.8787 → 0.8787 | 333.79 → 333.79 | 0.00% |
| CrSe2 | 电子 | 0.9651 → 0.9651 | 83.86 → 83.86 | 0.00% |
| CrSe2 | 空穴 | 0.9829 → 0.9829 | 246.10 → 246.10 | 0.00% |
| **SS** | **电子** | **0.7636 → 1.0151** | **125.42 → 70.97** | **−43.41%** |
| **SS** | **空穴** | **0.8293 → 0.9895** | **342.17 → 240.35** | **−29.76%** |

**by_direction 逐方向值全部不变** → 所有基于逐方向的分析（双口径表、三线对比、综合报告、图）不受影响（md5 核对相同）。

---

## 三、[0061-m] S7.1 应变标签改正 —— 对 E1 **无影响**（实测）

### 背景

`a134fd3` 修正了 AMSET 对称补应变在 **3/4/6 次轴**下的标签错误
（原版会把 xy、xz 互换，导致 `deformation.h5` 与 `*_signed.h5` 的剪切分量出错）。
六方体系（CrS2/CrSe2，6 次轴）理论上在该 bug 射程内。

### 实测方法

用 SS **已有的旧 S7 数据**，只重跑 S7.1（gen 步骤，读取 S7 形变输出重新对称化），
对比新旧 `band_edges.json`：

| 量 | 旧 S7.1 | 新 S7.1 | 变化 |
|---|---|---|---|
| 电子 E1_xx (eV) | 4.106700 | 4.106700 | **0.0000%** |
| 电子 E1_yy (eV) | 3.657500 | 3.657500 | **0.0000%** |
| 电子 E1_zz (eV) | 2.368300 | 2.368300 | **0.0000%** |
| 电子 E1_vac_xx (eV) | 5.839000 | 5.839000 | **0.0000%** |
| 电子 E1_vac_yy (eV) | 5.369500 | 5.369500 | **0.0000%** |
| 空穴 E1_xx (eV) | 1.346700 | 1.346700 | **0.0000%** |
| 空穴 E1_yy (eV) | 1.457500 | 1.457500 | **0.0000%** |
| 空穴 E1_vac_xx (eV) | 3.079000 | 3.079000 | **0.0000%** |
| 空穴 E1_vac_yy (eV) | 3.169500 | 3.169500 | **0.0000%** |
| 边能量 (eV) | −1.1396 / −1.9581 | 相同 | 0.0000% |

### 结论

- 该改正影响的是**剪切分量**（xy/xz）；我们 DPT 用的是**面内法向分量** D_xx/D_yy，
  由实际的 ±xx / ±yy 应变构型直接给出，不受标签互换影响
- **E1 全部 0.0000% → DPT 结果（S8.2）无需重算，已有数值正确**
- 交叉验证：E1 与文献 Table I 的 12 个方向偏差全部 <5%（中位 −0.4%），
  若对称化有系统性错误不可能对得这么好

---

## 四、还要重算的（仅 ADP 侧）

S8.4 的 **ADP 简并修正**（`adp_degen`）需要用 S7 抽的波函数建 `deformation_matrix.h5`。
我们三个材料的 S7 都是旧代码（没写波函数），所以 S8.4 走的是回退路径（k·p 拟合）。

- CrS2/CrSe2 的 S8.4 本身也是旧代码（[0061-m] 之前）
- SS 的 S8.4 是新代码但缺矩阵，同样走回退

**这部分不影响论文对比（论文用 DPT，不用 AMSET）**，如需完整的最新 ADP，
需要 S7 重跑（10 帧 + 波函数）→ S7.1 → S8.4。

当前状态：CrS2/CrSe2/LS 的 S7 重跑已排在 jzzn（预计 2026-10-25 09:38 起跑）。

---

## 五、集群尝试记录

| 集群 | ke 可用 | S7 能否跑 | 结论 |
|---|---|---|---|
| jzzn | ✅ | ✅ | 但排队到 2 天后 |
| hfeshell | ✅（check 通过） | ❌ | **amset venv 坏**：`ModuleNotFoundError: No module named 'amset'`（`/public/home/wangch/software/AutoZT/venvs/amset051/bin/amset`）；包在 site-packages 里但入口脚本用了错误的解释器 |
| a800 | ❌ | ❌ | 缺 VASP / pymatgen / amset / BoltzTraP2 |
| 3090 | ✅ | ⚠️ | 56 核，GPU-VASP，可跑但慢 |

hfeshell 的 amset 修复方法（未执行）：
```bash
V=/public/home/wangch/software/AutoZT/venvs/amset051
$V/bin/python -m pip install --force-reinstall --no-deps amset==0.5.1   # 重写入口脚本的 shebang
```

---

## 六、复现命令

```bash
AZ=/home/wangchao/software/AutoZT/bin/autozt
cd /mnt/d/joint_research_project/AutoZT/基准测试/superlattice

# [0069]/[0071] 重跑 S8.2
$AZ -tt ke-dft-cpu -p <M> -j S8.2_dpt retry
$AZ -tt ke-dft-cpu -p <M> start     # S8.1
$AZ -tt ke-dft-cpu -p <M> start     # S8.3

# 验证 S7.1 应变标签改正对 E1 的影响
$AZ -tt ke-dft-cpu -p SS -j S7.1_read retry
python3 -c "import json;d=json.load(open('SS/ke-dft-cpu/result/step7b_deform_read/band_edges.json'));print(d['electron']['E1_vac_xx_eV'])"
```
