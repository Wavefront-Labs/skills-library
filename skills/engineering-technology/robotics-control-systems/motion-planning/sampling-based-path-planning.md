---
id: engineering-technology.robotics-control-systems.motion-planning.sampling-based-path-planning
name: sampling-based-path-planning
category: engineering-technology
field: robotics-control-systems
product: motion-planning
tags: [motion-planning, path-planning, sampling-based-planning, rrt, rrt-connect, rrt-star, informed-rrt-star, prm, bit-star, configuration-space, c-space, collision-checking, fcl, ompl, moveit, nav2, path-smoothing, shortcutting, time-parameterization, totg, ruckig, trajectory-generation, jerk-limits, b-spline, a-star, hybrid-a-star, manipulator-planning]
level: practitioner
status: docs-checked
description: "Plan collision-free robot paths with RRT/RRT-Connect/RRT*/PRM, then shortcut, smooth and time-parameterise the result under velocity and acceleration limits."
sources:
  - "https://ompl.kavrakilab.org/planners.html"
  - "https://github.com/moveit/moveit2_tutorials"
  - "https://github.com/ompl/ompl"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampling-based path planning — from C-space to an executable trajectory

**Goal:** get a robot from start to goal without collision, in a configuration space
too large to grid (arms with 6-7 joints, or vehicles with kinematic constraints), and
turn the raw path into a smooth, time-parameterised trajectory the controller can follow.

## 1. Frame the problem in configuration space
- **C-space** = the joint vector for an arm (`q ∈ R^n`, with continuous joints as SO(2)),
  `(x, y, θ)` SE(2) for a mobile base. Planning happens here; collision checks map `q`
  back to geometry with forward kinematics.
- **Collision checker:** FCL (MoveIt's primary library) or Bullet (available in MoveIt) on simplified meshes. Use simplified
  collision geometry for links: detailed meshes make every check slower, and collision
  checking dominates planning time. Add a safety padding.
- **Distance metric:** weighted joint distance. Weight proximal joints more (they move
  more mass and sweep more volume) or the planner prefers wild shoulder motions.
- For 2-3 DOF problems with a good grid (mobile base in a 2-D map), search-based A* or
  Hybrid A* is simpler and deterministic. Use sampling as the dimension grows.

## 2. Choose the planner
| Planner | Use when | Notes |
|---|---|---|
| **RRT-Connect** | single query, need a feasible path fast | Two trees grown toward each other with greedy "connect". The planner used in the MoveIt tutorials (`RRTConnectkConfigDefault`). Not optimal: paths are jagged. |
| **RRT\*** / Informed RRT\* | you want shorter paths and can spend time | Asymptotically optimal by rewiring. Informed version samples only the ellipsoid that can improve the current best. |
| **PRM / PRM\*** | many queries in a static scene | Build a roadmap once, answer queries with graph search. |
| **BIT\*** / AIT\* | optimal planning with good anytime behaviour | Batch-informed and adaptively informed trees, both listed on the OMPL planners page. |

Key parameters: **range / step size** (OMPL `range`, the maximum step length), **goal bias**
(`goal_bias`, 0.05 in the MoveIt tutorial configuration), and **edge validity resolution**
(`longest_valid_segment_fraction`; 0.01 means edges shorter than 1/100 of the state space
are not sub-sampled). Too coarse and collisions are missed around small or narrow objects;
too fine and planning is very slow (MoveIt OMPL interface tutorial).

Core RRT step:
```text
q_rand = goal with prob p_goal else uniform sample
q_near = nearest(tree, q_rand)               # use a k-d tree / GNAT, not a linear scan
q_new  = steer(q_near, q_rand, step)
if motion_valid(q_near, q_new): add edge; if dist(q_new, goal) < tol: done
```
Narrow passages are the classic failure: uniform sampling rarely lands inside them.
Remedies: bridge-test or Gaussian sampling, a larger time budget, or decomposing the
task (approach pose first, then a short Cartesian move).

## 3. Post-process the path
Raw RRT paths zigzag. In order:
1. **Shortcutting:** repeatedly pick two random waypoints and replace the segment with a
   straight line if it's collision-free (many random attempts remove most detours).
   OMPL's `PathSimplifier` does this.
2. **Smoothing:** fit a B-spline or apply corner blending, then **re-check collisions**
   on the smoothed curve — smoothing cuts corners into obstacles.
3. Respect constraints: a car-like base needs Dubins/Reeds-Shepp steering in the planner
   itself; smoothing cannot repair a path that violates the minimum turning radius.

## 4. Time-parameterise
A path is geometry; the controller needs `q(t)`. Respect per-joint velocity and
acceleration limits (and jerk on industrial arms):
- **TOTG** (time-optimal trajectory generation): time-optimal under velocity/acceleration
  limits along a fixed path. The MoveIt tutorials recommend `TimeOptimalTrajectoryGeneration`.
- Use limits below datasheet values at first; datasheet limits are usually unloaded and
  torque-limited motion will lag and trigger following-error faults.
Sample the trajectory at the controller rate and check that velocity, acceleration and jerk
stay within limits on the sampled points.

## 5. MoveIt / OMPL pointers
In MoveIt 2, the planner is set per group in `ompl_planning.yaml`
(`planner_configs: [RRTConnectkConfigDefault, RRTstarkConfigDefault, ...]`) with
`longest_valid_segment_fraction` as the edge-check resolution; check names and
defaults against your MoveIt release, they have changed across versions. If RRT-Connect
regularly needs long planning times, the problem formulation
(padding, start in collision, unreachable goal IK) is usually wrong, not the planner.

## Checked
2026-11-01. Confirmed in the MoveIt 2 tutorials repo: FCL as primary collision library with Bullet available, `RRTConnectkConfigDefault`, `longest_valid_segment_fraction` meaning and trade-off, `goal_bias: 0.05`, TOTG recommendation. Confirmed in the OMPL source: `range` and `goal_bias` parameters, `PathSimplifier`; OMPL planners page lists Informed RRT*, BIT*, AIT*. Removed: speed-ratio, percentage, distance, attempt-count, rate and time figures, the RRT* radius formula, Smac, TOPP-RA and Ruckig claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Start and goal states are themselves collision-free and within joint limits.
- [ ] Edge-check resolution is fine enough that a dense re-check of the final path finds no collisions.
- [ ] Smoothed path re-checked for collision after smoothing.
- [ ] Trajectory samples respect velocity/acceleration (and jerk) limits with margin.
- [ ] Success rate measured over many randomised queries, with planning-time percentiles.
- [ ] Same query run with different seeds gives acceptable paths (no rare wild solutions).
