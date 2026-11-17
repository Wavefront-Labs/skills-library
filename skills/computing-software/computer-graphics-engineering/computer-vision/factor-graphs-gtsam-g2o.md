---
id: computing-software.computer-graphics-engineering.computer-vision.factor-graphs-gtsam-g2o
name: factor-graphs-gtsam-g2o
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, factor-graph, gtsam, g2o, pose-graph, isam2, slam-backend]
level: advanced
status: draft
description: "Build pose-graph and SLAM back-ends with factor graphs in GTSAM or g2o: variables, factors, noise models, robust kernels, iSAM2 incremental updates and marginal covariances."
sources: ["https://gtsam.org/tutorials/intro.html", "https://github.com/borglab/gtsam", "https://github.com/RainerKuemmerle/g2o"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Factor graphs (GTSAM, g2o)

A factor graph expresses MAP estimation as variables (poses, landmarks, biases) connected by
factors (measurements with noise models). Solving = sparse nonlinear least squares.

## GTSAM pose graph (Python)
```python
import gtsam, numpy as np
from gtsam.symbol_shorthand import X
g = gtsam.NonlinearFactorGraph(); v = gtsam.Values()
prior = gtsam.noiseModel.Diagonal.Sigmas(np.array([1e-3]*3 + [1e-3]*3))   # rot (rad) then trans (m)
odo = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.02]*3 + [0.05]*3))
g.add(gtsam.PriorFactorPose3(X(0), gtsam.Pose3(), prior))
for i, T in enumerate(odometry):            # relative Pose3 measurements
    g.add(gtsam.BetweenFactorPose3(X(i), X(i+1), T, odo))
robust = gtsam.noiseModel.Robust.Create(gtsam.noiseModel.mEstimator.Huber.Create(1.345), odo)
g.add(gtsam.BetweenFactorPose3(X(i_loop), X(j_loop), T_loop, robust))     # loop closure
result = gtsam.LevenbergMarquardtOptimizer(g, initial, gtsam.LevenbergMarquardtParams()).optimize()
marg = gtsam.Marginals(g, result); cov = marg.marginalCovariance(X(5))
```
- Pose3 noise ordering in GTSAM is **rotation first, then translation**; g2o's SE3 edges use
  translation first. Mixing these up is a classic bug.
- Initial values matter: chain odometry to initialise.

## Incremental: iSAM2
`isam = gtsam.ISAM2(); isam.update(new_factors, new_values); est = isam.calculateEstimate()`:
re-linearises only affected variables; real-time SLAM back-end.

## g2o
C++ library used by ORB-SLAM: choose a block solver and linear solver
(`BlockSolver_6_3` + `LinearSolverEigen`/`Cholmod`), `OptimizationAlgorithmLevenberg`, add
`VertexSE3Expmap`/`EdgeSE3ProjectXYZ`, set `RobustKernelHuber`. `.g2o` text files are a common
pose-graph exchange format (`gtsam.readG2o` reads them).

## Practical
- Robust kernels (Huber, Cauchy) on loop closures; false loops destroy maps. Consider switchable
  constraints or GNC (`GncOptimizer`) for many outliers.
- Information = inverse covariance: overconfident odometry noise prevents loop closures from
  correcting drift.
- Fix gauge freedom with one prior (or fix the first vertex in g2o).

## Verify
Error before/after optimisation (`g.error(values)`), ATE against ground truth, and chi-square
of each loop factor to flag outliers.
