---
id: engineering-technology.robotics-control-systems.state-estimation-sensor-fusion.kalman-filter-design
name: kalman-filter-design
category: engineering-technology
field: robotics-control-systems
product: state-estimation-sensor-fusion
tags: [state-estimation-sensor-fusion, kalman-filter, kf, extended-kalman-filter, ekf, error-state-kalman-filter, eskf, ukf, sensor-fusion, imu, gnss, gps, wheel-odometry, process-noise, measurement-noise, q-matrix, r-matrix, allan-variance, mahalanobis-gating, chi-square, nees, nis, filter-consistency, joseph-form, covariance, robot-localization, localisation, ins, dead-reckoning]
level: advanced
status: draft
description: "Design a Kalman/extended Kalman filter: state and noise models, Q/R tuning from sensor specs, IMU+GNSS/odometry fusion, outlier gating and NEES/NIS consistency checks."
sources:
  - "Bar-Shalom, Li and Kirubarajan, Estimation with Applications to Tracking and Navigation (Wiley, 2001)"
  - "Sola, Quaternion kinematics for the error-state Kalman filter (arXiv:1711.02508)"
  - "Groves, Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems"
  - "https://docs.ros.org/en/melodic/api/robot_localization/html/index.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kalman filter design — models, noise, gating and proof it is consistent

**Goal:** fuse noisy sensors (IMU, GNSS, wheel odometry, vision) into one state
estimate whose covariance honestly reflects its error, so downstream control and
planning can trust both the number and the uncertainty.

## 1. Write the models first
Discrete linear form (EKF: replace `F`, `H` with Jacobians at the current estimate):
```text
x_k = F x_{k-1} + B u_k + w,   w ~ N(0, Q)       process / motion model
z_k = H x_k + v,               v ~ N(0, R)       measurement model
Predict:  x⁻ = F x + B u ;        P⁻ = F P Fᵀ + Q
Update:   y = z - H x⁻ ;           S = H P⁻ Hᵀ + R
          K = P⁻ Hᵀ S⁻¹ ;          x = x⁻ + K y
          P = (I - K H) P⁻ (I - K H)ᵀ + K R Kᵀ     (Joseph form: stays symmetric PSD)
```
Choose the smallest state that explains the data, e.g. planar robot with IMU + wheel
odometry + GNSS: `x = [px, py, θ, v, ω, b_g]` (gyro bias `b_g` as a random walk).
Unmodelled bias is the most common reason a filter is confidently wrong.

**IMU as input, not measurement.** For inertial navigation, drive the prediction with
IMU accelerations and rates (`u`) and treat GNSS/odometry as measurements. With 3-D
attitude use an **error-state** filter (ESKF): nominal state integrates quaternions,
the filter estimates a small 3-vector attitude error, avoiding quaternion
normalisation problems in the covariance.

## 2. Get Q and R from physics, then tune
- **R** from sensor specs or a static log: GNSS horizontal σ 1-3 m (standalone),
  1-3 cm (RTK fixed); use the receiver's reported covariance only after checking it
  against truth, many receivers are optimistic. Wheel odometry: σ grows with distance
  (1-5% of distance travelled) and slip — inflate on turns.
- **Q** for an IMU-driven model from the datasheet or an **Allan variance** plot:
  angle random walk `N` (rad/s/√Hz) gives gyro white noise `Q_gyro = N²·Δt` per step
  on angle; bias instability / rate random walk set the bias random-walk `Q_b = K²·Δt`.
  Example: ARW 0.2 °/√h = 0.2/60 °/√s ≈ 5.8e-5 rad/√s → per-step angle variance at
  200 Hz `≈ (5.8e-5)²·0.005 ≈ 1.7e-11 rad²`.
- For a constant-velocity model with unknown acceleration σ_a, use the discretised
  white-noise-acceleration Q: for each axis
  `Q = σ_a²·[[Δt⁴/4, Δt³/2],[Δt³/2, Δt²]]`.
- Then tune with data: if NIS is too large, Q or R is too small; if too small,
  they're too large (section 4). Change one at a time, by factors of 2-10.

## 3. Real-world plumbing
- **Timestamps:** fuse each measurement at its sensor time; out-of-order data needs
  buffering and re-propagation from the stored state. A 50 ms GNSS latency at 2 m/s
  is a 10 cm bias if ignored.
- **Frames and lever arms:** GNSS antenna 0.5 m from the IMU adds `ω × r` velocity and
  `R·r` position terms; include them in `h(x)`.
- **Angle wrap:** wrap innovation `y` for headings to (-π, π] before using it.
- **Outlier gating:** reject a measurement if Mahalanobis distance `d² = yᵀ S⁻¹ y`
  exceeds the χ² threshold for its dimension (99%: 6.63 for 1-D, 9.21 for 2-D,
  11.34 for 3-D). Count rejections; if many consecutive rejects, the filter has
  diverged — re-initialise rather than keep gating.
- **Observability:** heading is unobservable from GNSS position while stationary;
  gyro bias needs rotation or a zero-velocity update. Don't expect states to converge
  without excitation.
- **Numerics:** keep `P` symmetric, use Joseph form (or a square-root filter) and doubles.

## 4. Prove it is consistent
With ground truth (simulation, RTK, motion capture):
- **NEES** `ε = (x - x̂)ᵀ P⁻¹ (x - x̂)` averaged over runs should sit near the state
  dimension `n`, inside the χ² bounds.
Without truth, on live data:
- **NIS** `yᵀ S⁻¹ y` per measurement should average near the measurement dimension `m`;
  innovations should be zero-mean and white (autocorrelation near zero beyond lag 0).
NEES of 50 for n = 6 means overconfident: it will reject good measurements even if the plot "looks good".

## 5. EKF vs UKF vs factor graphs
EKF is fine when the nonlinearity over one σ is mild (most wheeled robots, INS with
ESKF); a UKF helps with strongly nonlinear measurements (close-range range-bearing). When you need to relinearise past states (loop
closures, SLAM), move to smoothing / factor graphs (GTSAM, Ceres). In ROS 2,
`robot_localization` (`ekf_node`) implements a 15-state EKF with per-sensor boolean
masks for which fields to fuse; its parameter names are worth checking for your distro.

## Verify
- [ ] Every state has a model and every sensor has an `h(x)` including frames, lever arms and delay.
- [ ] Q and R derive from datasheets/Allan variance/static logs, with the tuning factors recorded.
- [ ] Average NIS ≈ measurement dimension; innovations zero-mean and roughly white.
- [ ] NEES within χ² bounds on runs with ground truth.
- [ ] Gating rejects injected outliers (e.g. a 20 m GNSS jump) and recovers afterwards.
- [ ] `P` stays symmetric positive-definite over a long run; no NaNs after hours of data.
