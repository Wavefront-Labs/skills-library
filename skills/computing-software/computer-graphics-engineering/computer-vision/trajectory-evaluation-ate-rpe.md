---
id: computing-software.computer-graphics-engineering.computer-vision.trajectory-evaluation-ate-rpe
name: trajectory-evaluation-ate-rpe
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, absolute-trajectory-error, relative-pose-error, evo, slam-evaluation, benchmarking]
level: practitioner
status: verified
description: "Evaluate SLAM/VO trajectories: ATE and RPE definitions, timestamp association, SE(3)/Sim(3) alignment, evo command-line usage and reporting pitfalls."
sources: ["https://github.com/MichaelGrupp/evo", "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools", "https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trajectory evaluation (ATE, RPE)

## Metrics
- **ATE** (absolute trajectory error): RMSE of position differences after aligning the estimate to
  ground truth. Global consistency; dominated by drift and loop-closure quality.
- **RPE** (relative pose error): error of relative motion over a fixed interval (e.g. 1 s, 1 m,
  100 m); measures local drift, independent of where errors happened. Report translation (percent
  or m/m) and rotation (deg/m) separately. The KITTI odometry benchmark reports segment-based errors over fixed lengths (confirm the lengths
  in the KITTI devkit).

## evo
```bash
evo_ape tum gt.txt est.txt -va --plot --save_results ape.zip       # -a: SE(3) align
evo_ape tum gt.txt est.txt -vas                                    # -s: + scale (Sim(3)), monocular
evo_rpe tum gt.txt est.txt -va --delta 1 --delta_unit m --pose_relation trans_part
evo_traj tum est.txt --ref gt.txt -p --plot_mode xy
evo_res ape_*.zip -p --use_filenames                               # compare runs
```
Formats: `tum` (timestamp tx ty tz qx qy qz qw), `kitti` (3x4 matrices, no timestamps), `euroc`,
`bag`.

## Pitfalls
- **Association**: estimates and ground truth are matched by timestamp with `--t_max_diff`
  (default 0.01 s, confirmed in the evo source); clock offsets require `--t_offset`. Few associated
  poses = meaningless numbers. Tested (evo 1.x, synthetic spiral, 600 poses): an estimate stamped
  0.5 s late still associated (the 0.1 s sampling grid lets samples match 5 steps away) and gave a
  wrong APE RMSE of 0.2190 m; `--t_offset -0.5` restored the exact 0.2240 m.
- Alignment choice must be reported: SE(3) (`-a`) for stereo/lidar, Sim(3) (`-as`) for monocular,
  4-DOF (yaw + translation) for VIO (gravity observable) per Zhang and Scaramuzza; evo itself only
  offers Umeyama SE(3)/Sim(3), `--align_origin` and `--n_to_align`. A half-scale estimate gave APE
  RMSE 5.04 m with `-a` and 0.217 m with `-as`.
- Aligning on the whole trajectory hides drift; also report alignment on the first N seconds or
  RPE.
- Frame conventions (camera vs body/IMU frame) must match the ground truth's frame; apply the
  extrinsic before comparing.
- Run several times: multi-threaded SLAM is non-deterministic; report median and spread.

## Verify
Evaluate ground truth against itself (ATE about 0; evo printed rmse 0.000000) and a known-perturbed copy to confirm the tool chain.
