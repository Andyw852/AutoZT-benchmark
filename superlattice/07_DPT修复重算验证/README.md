# DPT 修复（skill [0069]）重算验证

> 时间：2026-10-23
> 触发：用户修复了 `step8.2_dpt/gen_step12_dpt.py`（commit `439f176`，skill_rev `2026-10-22-0069-3d-valley-axis`）

---

## 一、修复内容（git commit 439f176）

**[0069] S8.2 3D 多谷 DPT**：3D 带边谷有对称等价谷时（Si 的 6 个 Δ 谷、Ge/PbTe 的 L 谷、Mg₂Si 的 X 谷）：

- **以前**：先对等价谷平均张量对角再进 μ ∝ 1/E1²，只剩静水部分（Si 导带 E1 = Ξ_d + Ξ_u/3 = 2.99 eV）
- **现在**：E1 取带边谷沿谷轴 â 的 LA 形变势 |â·D·â|（Si = Ξ_d + Ξ_u = 8.72 eV），
  C 取沿谷轴的纵向模量 C_L(â)，三个方向共用
- **影响**：Si 电子 DPT 从 36135 → 修正（高估 8.5 倍）
- **明确不影响**：单谷、简并带边、**2D**

## 二、重算过程

对三个已完成材料执行：

```bash
autozt -tt ke-dft-cpu -p <M> -j S8.2_dpt retry   # 重新生成 dpt_result.json
autozt -tt ke-dft-cpu -p <M> start               # 补下游 S8.1_bt2
autozt -tt ke-dft-cpu -p <M> start               # 补下游 S8.3_cmp
```

## 三、重算结果：**完全相同**

| 材料 | 载流子 | 旧 μ (rev 0034) | 新 μ (rev 0069) | 变化 |
|---|---|---|---|---|
| CrS2 | 电子 | 95.76 | **95.76** | 0.0000% |
| CrS2 | 空穴 | 333.79 | **333.79** | 0.0000% |
| CrSe2 | 电子 | 83.86 | **83.86** | 0.0000% |
| CrSe2 | 空穴 | 246.10 | **246.10** | 0.0000% |
| SS | 电子 | 125.42 | **125.42** | 0.0000% |
| SS | 空穴 | 342.17 | **342.17** | 0.0000% |

m*、E1、C_2D 也逐位相同。

## 四、为什么没变（代码路径核对）

`gen_step12_dpt.py` 中的谷轴逻辑：

```python
# L2482
va, va_why = _valley_axis_3d(cwd, carrier) if (e3 is not None and cd is not None) else (None, None)
# L2550
va = bd.get("valley_axis") if (not is_2d and bd.get("status") == "ok") else None
```

- `e3` 是 **3D 形变势**（`_e1_diag_3d` 的结果）；2D 体系该函数返回 None → 整段跳过
- L2550 显式判断 `not is_2d` → 2D 一律不用谷轴口径

**结论**：本次修复针对 3D 多谷体系，2D 材料（本项目的 CrS2/CrSe2/SS/LS）走的是原来的
分方向 2D 口径，因此结果不变。这与 commit message 中"单谷、简并带边、2D 不变"的说明一致。

## 五、下游状态

重算后 `S8.2_dpt` 的输入指纹变化导致下游 `S8.1_bt2`、`S8.3_cmp` 被标记失效，
已重新生成（数据相同），DAG 恢复完整。**S8.4_amset2d 未被影响**（不依赖 S8.2 的指纹）。

## 六、复现

```bash
git -C ~/software/AutoZT show 439f176 -- skill/ke-dft-cpu/step8.2_dpt/gen_step12_dpt.py
grep -n "valley_axis\|not is_2d" skill/ke-dft-cpu/step8.2_dpt/gen_step12_dpt.py
```
