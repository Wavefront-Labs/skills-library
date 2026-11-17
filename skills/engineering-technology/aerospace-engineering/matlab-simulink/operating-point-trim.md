---
id: engineering-technology.aerospace-engineering.matlab-simulink.operating-point-trim
name: operating-point-trim
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, trim-linearization, operating-point, trim, findop, simulink-control-design, steady-level-flight]
level: practitioner
status: docs-checked
description: "Find trim conditions for a Simulink aircraft model with findop or trim, specify known states and outputs, and check the result is physically sensible."
sources:
  - "https://www.mathworks.com/help/slcontrol/ug/findop.html"
  - "https://www.mathworks.com/help/simulink/slref/trim.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Operating-point search and trim

**Goal:** steady-state initial conditions for simulation and linearisation.

## Using Simulink Control Design
```matlab
opspec = operspec('myAircraftModel');
% set known: altitude, airspeed, flight path angle, zero rates
opspec.States(1).Known = 1;      % example, adjust indices to your model
opspec.States(1).x = 100;        % the fixed value when Known
opspec.States(2).SteadyState = 1; % steady state required; x is then an initial guess
opspec.States(2).Min = 0;        % optional bound
op = findop('myAircraftModel', opspec);
```
The model must be open. Declare which states are known (fixed), which must be at steady state, and bound inputs (throttle, elevator); the findop page shows `Min` bounds.

## Using core Simulink
`[x, u, y, dx] = trim('myModel', x0, u0, y0, ix, iu, iy, dx0, idx)` where `ix`, `iu`, `iy` are index vectors of fixed states, inputs and outputs, and `idx` selects which entries of `dx0` the search must satisfy exactly.

## Procedure
1. Choose the trim condition: level flight at speed V and altitude h (flight path angle 0, rates 0), or climb or turn.
2. Set sensible initial guesses (alpha from `CL` requirement; throttle from drag estimate).
3. Run the search, inspect the residual: derivatives of the steady states must be near zero.
4. Check trim values: alpha, elevator, throttle within limits and plausible.
5. Save the operating point object for linearization and for simulation initial conditions.

## Gotchas
- A trim reported as converged on a local minimum can still have a nonzero derivative: check the derivative output.

## Verify
- [ ] Simulation started from the trim point stays at that point for tens of seconds.

## Checked
2026-11-01. Confirmed on the findop and trim pages: `findop(mdl, opspec)` with the model open, `operspec(mdl)`, States(i).Known with x as the fixed value, SteadyState with x as an initial guess, Min bound; trim argument list `(sys,x0,u0,y0,ix,iu,iy,dx0,idx)` and the meaning of ix, iu, iy, idx. Corrected the trim call (dx0 was missing). Removed: the 1e-6 threshold and the discrete-state advice.
Method: documentation only; no commands were run.
