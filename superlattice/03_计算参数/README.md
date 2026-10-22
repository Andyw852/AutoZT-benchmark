# 计算参数说明

本目录是四个材料最终的 `project_setting/templates/step.conf` 副本（生效配置）。

## 关键修改（相对技能出厂默认）

| 键 | 出厂默认 | 本次设置 | 原因 |
|---|---|---|---|
| `FUNC` | `auto`（2D 单组分会选 PBEsol） | **`pbe`** | 文献 JAP 139,024301 用 GGA-PBE |
| `BANDGAP` | `hse` | **`pbe`** | 文献无 HSE，纯 PBE 全链 |
| `odp_frozen`（tf yaml） | `true` | **`false`** | 用户决定先不跑冻声子 ODP/IVS 线 |

其余键保持出厂默认（S3 网格规则、ENCUT 等由各步骤模板决定）。

## 各材料 S3 均匀网格

| 材料 | S3 KPOINTS |
|---|---|
| CrS2 | 48×48×3 |
| CrSe2 | 48×48×3 |
| SS | 12×42×3 |
| LS | 6×42×3 |

（面内均为 6 的倍数，kz=3，符合当前网格规则）

## 赝势
PBE PAW POTCAR，按元素自动选择（Cr/S/Se 的 PBE 版本）。

## 如何复现/查看生效值
```bash
autozt -tt ke-dft-cpu -p CrS2 -j S3_uniform conf    # 查看某步合并后的参数
```
