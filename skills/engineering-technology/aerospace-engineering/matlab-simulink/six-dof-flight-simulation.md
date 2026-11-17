---
id: engineering-technology.aerospace-engineering.matlab-simulink.six-dof-flight-simulation
name: six-dof-flight-simulation
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, aerospace-blockset, 6dof, six-dof, flight-dynamics, flight-simulation, equations-of-motion, quaternion, euler-angles, coesa, isa-atmosphere, wgs84, lookup-table, aero-database, trim, findop, linearize, simulink-control-design, monte-carlo, parsim, dispersions, gnc, flat-earth]
level: practitioner
status: docs-checked
description: "Build a 6-DOF rigid-body flight simulation in MATLAB/Simulink (Aerospace Blockset): frames, aero tables, trim, linearise and Monte Carlo dispersions."
sources:
  - "https://www.mathworks.com/help/aeroblks/6dofquaternion.html"
  - "https://www.mathworks.com/help/aeroblks/6dofecefquaternion.html"
  - "https://www.mathworks.com/help/aeroblks/coesaatmospheremodel.html"
  - "https://www.mathworks.com/help/aeroblks/wgs84gravitymodel.html"
  - "https://www.mathworks.com/help/aeroblks/aerodynamicforcesandmoments.html"
  - "https://www.mathworks.com/help/simulink/slref/parsim.html"
  - "https://www.mathworks.com/help/simulink/slref/simulink.simulationinput.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Six-DOF flight simulation in Simulink — from aero tables to dispersed runs

**Goal:** a nonlinear rigid-body model you can trim, linearise for control design, and
run hundreds of times with dispersed parameters, with frames and units you can defend.

## 1. Decide the frame and fidelity first
- **Flat Earth** (`6DOF (Quaternion)` block, outputs position and velocity in the flat
  Earth reference frame): fine for aircraft and short-range missiles. Euler-angle
  attitude is singular at pitch +-90 degrees, so use quaternions for anything that can go
  vertical (launch, aerobatics, VTOL).
- **Rotating ellipsoidal Earth** (`6DOF ECEF (Quaternion)`, planet model Earth (WGS84)
  by default, rotating ECEF frame, precession/nutation/polar motion neglected): rockets,
  long-range trajectories, anything where Coriolis or curvature matters. Pair it with the
  `WGS84 Gravity Model` block (Taylor Series, Close Approximation or Exact) instead of
  constant g; for high-accuracy orbit prediction the block page points to EGM96 instead.
- Both blocks offer mass types Fixed, Simple Variable and Custom Variable, and use the
  scalar-first quaternion convention.
- Pick one unit system on every blockset block (the 6DOF block offers Metric (MKS) and two
  English options). Mixed units across blocks is the most common silent bug.

## 2. Model layout (one subsystem per job)
```
Environment  ->  Aerodynamics  ->  Propulsion  ->  Sum F/M  ->  6DOF EOM
 (COESA/ISA,      (alpha, beta,     (thrust,         (body-axis      (states: V_b,
  gravity, wind)   Mach, q, rates)   mass flow)       forces, moments) omega, q/euler, pos)
       ^------------------------- feedback of states via bus ---------------------|
```
- Use bus objects for state and environment signals.
- Aero: coefficients in lookup tables indexed by alpha, Mach (and beta,
  control deflections). Non-dimensionalise rates with the reference length:
  `Cm = Cm0(a,M) + Cm_de(a,M)*de + Cm_q(M)*q*cbar/(2V)`. The `Aerodynamic Forces and
  Moments` block takes a coefficient vector, dynamic pressure `qbar`, and CG and CP
  (moment reference point) inputs and returns force and moment about the CG; if your
  moment coefficients are already about the CG, set CP equal to CG so the force-transfer
  moment is not double-counted. The CG moves as fuel burns.
- **Table extrapolation:** configure lookup tables not to extrapolate (clip) unless you have a reason.
  Linear extrapolation outside the database (e.g. alpha beyond stall) can produce
  absurd moments that look like real departures.
- Mass properties: use the Custom Variable mass type if mass changes appreciably;
  remember the inertia-rate term.

## 3. Solver and attitude drift
- Choose the solver to suit the job (analysis versus code generation or HIL) and check
  results at a tighter tolerance or smaller step.
- The 6DOF quaternion block applies a correction that drives the quaternion norm back to 1;
  releases before R2025a also exposed a "Gain for quaternion normalization" parameter.
  Drift shows up as a slowly growing attitude error over long runs.

## 4. Trim and linearise
Use Simulink Control Design to create an operating-point specification for the model,
set known and steady-state flags per state (for example fix airspeed and altitude, free
alpha, throttle and elevator), find the operating point, then linearise between marked
linear-analysis points at that point. State indices depend on your model; inspect the
specification before setting them. Position states are never steady in cruise, so release
their steady-state flags or trim fails. Check that the trimmed state derivatives are
near zero before trusting the linear model, and inspect the poles for short period,
phugoid, Dutch roll, spiral and roll modes.

## 5. Monte Carlo dispersions
```matlab
N = 500;  in(1:N) = Simulink.SimulationInput(mdl);
for k = 1:N
  in(k) = in(k).setVariable('dCL', 0.05*randn);        % 1-sigma aero uncertainty
  in(k) = in(k).setVariable('massScale', 1 + 0.02*randn);
  in(k) = in(k).setVariable('windNorth', 5*randn);
end
out = parsim(in, 'ShowProgress','on', 'TransferBaseWorkspaceVariables','off');
```
- `parsim` runs serially if no parallel pool can be created. `TransferBaseWorkspaceVariables`
  defaults to off; the page advises against turning it on for large-scale runs.
- Seed the RNG (`rng(42)`) and save the draws so any outlier run can be replayed.
- Use uniform distributions for bounded tolerances and Gaussian for measured scatter;
  document 1-sigma vs 3-sigma clearly.
- Report percentiles and the worst runs, not just means; tail statements need many runs
  or a statistically justified bound (see the dispersion-statistics skill).

## Gotchas
- Body axes are x-forward, y-right, z-down; alpha = atan2(w,u). Sign errors in Cm_q or
  in elevator convention give a model that trims but diverges in a few seconds.
- Aero databases are usually referenced to a fixed moment reference point; forgetting
  the CG shift moves the static margin and changes stability.
- The COESA Atmosphere Model data covers about 0 to 84,852 m geopotential altitude;
  outside it the block extrapolates (temperature linearly, pressure logarithmically).
  Set and test its out-of-range action parameter before high-altitude cases.
- Block names and parameter dialogs have shifted between releases; confirm against your
  installed release's Aerospace Blockset docs.

## Verify
- [ ] With zero controls and zero forces except gravity, the model free-falls at g and
      attitude stays constant (sanity check of EOM wiring).
- [ ] Trim converges with state derivatives near zero.
- [ ] Linear-model eigenvalues match published or hand-calculated short-period and
      phugoid frequencies.
- [ ] Linear and nonlinear step responses agree for small inputs.
- [ ] Units are consistent across every blockset block.
- [ ] Monte Carlo draws are seeded, saved, and outliers are reproducible.

## Checked
2026-11-01. Confirmed on the MathWorks block and function pages in `sources`: block names
(6DOF (Quaternion), 6DOF ECEF (Quaternion), WGS84 Gravity Model, COESA Atmosphere Model,
Aerodynamic Forces and Moments), their options, the COESA range and extrapolation, parsim
serial fallback and `TransferBaseWorkspaceVariables` default, `Simulink.SimulationInput`
and `setVariable`. Removed: Euler Angles and Incidence/Sideslip block names (not read), J2
gravity, solver names, step sizes and tolerances, operspec/findop/linearize code and
tolerances, percentage thresholds. The Simulink Control Design workflow is described
without function names. `rng`/`randn`/`atan2` are core MATLAB.
Method: documentation only; no commands were run.
