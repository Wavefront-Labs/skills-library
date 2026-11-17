---
id: engineering-technology.robotics-control-systems.robot-kinematics-dynamics.jacobian-inverse-kinematics
name: jacobian-inverse-kinematics
category: engineering-technology
field: robotics-control-systems
product: robot-kinematics-dynamics
tags: [robot-kinematics-dynamics, inverse-kinematics, ik, forward-kinematics, fk, jacobian, geometric-jacobian, analytic-jacobian, denavit-hartenberg, dh-parameters, product-of-exponentials, poe, damped-least-squares, levenberg-marquardt, pseudoinverse, singularity, manipulability, null-space, redundancy, joint-limits, se3, rotation-error, manipulator, robot-arm, pinocchio, kdl, trac-ik, moveit]
level: advanced
status: docs-checked
description: "Solve manipulator inverse kinematics numerically: DH/PoE forward kinematics, geometric Jacobian, damped least-squares iteration, joint limits and singularity handling."
sources:
  - https://hades.mech.northwestern.edu/images/7/7f/MR.pdf
  - https://www.math.ucsd.edu/~sbuss/ResearchWeb/ikmethods/iksurvey.pdf
  - https://github.com/traclabs/trac_ik
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numerical inverse kinematics with the Jacobian

**Goal:** given a target end-effector pose `T_d ∈ SE(3)`, find joint angles `q` that
reach it, robustly near singularities and within joint limits, for any serial arm
(including 7-DOF redundant ones where no closed form exists).

## 1. Forward kinematics you trust
Pick one convention and stick to it:
- **DH (standard or modified, never mixed):** each joint `i` contributes
  `A_i = Rot_z(θ_i)·Trans_z(d_i)·Trans_x(a_i)·Rot_x(α_i)`; `T = A_1···A_n`.
- **Product of exponentials (PoE):** `T(q) = e^[S1]q1 ··· e^[Sn]qn · M`, with screw axes
  `S_i` in the base frame at the zero pose and home pose `M`. Easier to read off a CAD
  model and no frame-placement rules.
In practice, load the URDF into a library (Pinocchio, KDL, `roboticstoolbox-python`,
MATLAB `rigidBodyTree`) rather than hand-coding. Test FK first: put the arm at three or
four known poses (zero, each joint at +90°) and compare to CAD or the vendor controller
to < 1 mm. Most "IK doesn't converge" bugs are FK or unit bugs (degrees vs radians, mm vs m).

## 2. The Jacobian
The geometric Jacobian `J(q)` (6×n) maps joint rates to the end-effector twist
`[v; ω] = J q̇`. For revolute joint `i` with axis `z_i` through point `p_i`, and
end-effector point `p_e`, all in the base frame:
`J_i = [ z_i × (p_e - p_i) ; z_i ]`. Prismatic: `J_i = [ z_i ; 0 ]`.
Check it numerically once: perturb each joint by 1e-6 rad and compare finite-difference
FK to `J`; errors above ~1e-5 mean a frame or ordering bug. Be clear which frame (base vs
end-effector, "space" vs "body") and which order (linear-first or angular-first) your
library uses; they differ (Modern Robotics puts angular first).

## 3. Damped least-squares iteration
Pose error, base frame: `e_p = p_d - p(q)`; orientation error from
`R_err = R_d · R(q)ᵀ` as an axis-angle vector `e_o = log(R_err)` (never subtract Euler angles).
Stack `e = [e_p; e_o]` and iterate:
```python
for k in range(max_iter):            # max_iter ~ 100-200
    e = pose_error(T_d, fk(q))
    if norm(e[:3]) < 1e-4 and norm(e[3:]) < 1e-3:  # 0.1 mm, ~0.06 deg
        break
    J = jacobian(q)
    W = diag([1,1,1, wr,wr,wr])      # wr balances metres vs radians; tune it
    lam2 = lam0**2 * (1 - min(manip(J)/m0, 1))**2 + 1e-6  # damping grows near singularity
    dq = J.T @ solve(J @ J.T + lam2 * eye(6), W @ e)
    dq = clip_step(dq, 0.2)          # limit per-iteration joint step (rad)
    q  = clamp_to_limits(q + alpha * dq)   # alpha 0.5-1
```
- Plain pseudoinverse `J⁺` blows up near singularities (`dq → ∞`). DLS
  `Jᵀ(JJᵀ + λ²I)⁻¹` (the Levenberg-Marquardt form, Buss) trades a little accuracy for bounded steps; tune `λ` per arm.
- Manipulability `w = sqrt(det(J Jᵀ))` (or the smallest singular value of `J`) is the
  singularity meter; schedule `λ` from it as above (`m0` a threshold below which damping engages).
- Adaptive step (Levenberg-Marquardt style: shrink `λ` when error drops, grow it when
  it rises) converges in a few iterations from a good seed.

## 4. Redundancy and joint limits
For n > 6, add a null-space term that does not disturb the task:
`dq = J⁺_dls·e + (I - J⁺J)·k0·∇H(q)`, with `H` e.g. distance from joint mid-range,
`k0` small (the null-space method goes back to Liégeois; Buss). Clamping alone makes the solver stall against a limit; the
null-space term steers away before it gets there. Wrap continuous joints to (-π, π].

## 5. Seeding and multiple solutions
A 6R arm has a finite number of IK branches (Modern Robotics ch. 6 Figure 6.5 shows four possible solutions for a PUMA-type arm; elbow up/down, wrist flip, shoulder
left/right). Numerical IK returns the one nearest the seed:
- For trajectories, seed with the previous waypoint's solution so the arm doesn't jump branches.
- For one-shot goals, run from several random seeds and pick the solution nearest the
  current configuration (or best manipulability). TRAC-IK (a MoveIt kinematics plugin) runs a KDL Newton solver with random jumps
  and an SQP solver concurrently and returns when either converges.
- If the arm has a spherical wrist, analytic IK (position from the wrist centre, then
  orientation) is faster and returns every branch; prefer it when available.

## 6. Dynamics hook (why the Jacobian matters later)
The same `J` gives static force mapping `τ = Jᵀ F`: a 50 N load at the tool requires
joint torques `Jᵀ·[0,0,-50,0,0,0]`. Use it to check that every IK solution is also
within torque limits, and remember that near singularities small joint torques give
very large forces along the degenerate direction.

## Checked
2026-11-01. Confirmed: product-of-exponentials form, screw axes and Newton-Raphson IK (Modern Robotics ch. 3, 4, 6); twist order angular-first (Vs = (ωs, vs)); damped least squares as Jᵀ(JJᵀ+λ²I)⁻¹, its Levenberg-Marquardt name, per-step clamping and null-space projection (Buss survey); TRAC-IK's concurrent Newton plus SQP design (its README). Removed: branch counts of 8 and 16, typical λ, wr and k0 ranges, the IKFast claim.
Method: documentation only; no commands were run.

## Verify
- [ ] FK matches CAD or the vendor controller at ≥ 3 test poses to < 1 mm.
- [ ] Finite-difference Jacobian agrees with the analytic one to ~1e-5.
- [ ] IK reaches 1000 random reachable poses (generated by FK of random `q`) with essentially 100% success (TRAC-IK's README reports its solve rates the same way, over 10,000 random reachable configurations).
- [ ] Near a known singularity (e.g. wrist aligned) the step stays bounded; no NaNs.
- [ ] Solutions respect joint limits; along a path, consecutive solutions stay on one branch.
- [ ] Errors use axis-angle orientation, and units are consistent (m, rad) throughout.
