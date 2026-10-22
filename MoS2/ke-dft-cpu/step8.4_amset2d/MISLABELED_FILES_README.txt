================================================================
⚠ 误标文件说明（2026-09-26，用户指示立即改名）
================================================================

1) transport_C_fullgrid_real.MISLABELED_do_not_use.json
   曾名 transport_C_fullgrid_real.json。
   实测其 md5 与 transport_141x141x11.json 完全相同（d7a4fd7dc78307fd01b2e2524ac96508），
   即它是**去对称化路径（step4_wave, 141x141x11）**的结果，**不是**"全网格 + 真实重叠"的 C 臂。
   组 C 的真结果由作业 3911287 写入 transport_263x263x21.json（提交于 2026-09-26 15:21）。
   本文件保留仅作历史，**不得再作为 C 引用**。

2) transport_B_factor4_unity.json
   这是正确的 B 臂（unity_overlap=true, 全网格, interpolation_factor=4），md5
   7b3286b63b... 与改名前的 transport_263x263x21.json 相同（B 是它的存档副本）。可以用。

3) intrinsic_transport.json
   若其 mtime 早于作业 3911287 的完成时间，则是**上一次（unity 口径）**的产物，
   在组 C 重跑后会由 postprocess_intrinsic 覆盖。引用前先核对 mtime。

判据来源：tmp/amset2d/STATUS_2026-09-26.md、bvc_prep.py、bvc_compare.py。
