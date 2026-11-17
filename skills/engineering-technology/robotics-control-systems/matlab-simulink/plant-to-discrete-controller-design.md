---
id: engineering-technology.robotics-control-systems.matlab-simulink.plant-to-discrete-controller-design
name: plant-to-discrete-controller-design
category: engineering-technology
field: robotics-control-systems
product: matlab-simulink
tags: [matlab, simulink, control-system-toolbox, tf, ss, zpk, c2d, d2c, margin, allmargin, bode, step, stepinfo, pidtune, pidtuneoptions, pid, pidf, feedback, loopsens, system-identification, tfest, discretisation, tustin, zoh, fixed-step-solver, discrete-pid-controller, anti-windup, embedded-coder, code-generation, model-in-the-loop, mil, sil, servo-control, dc-motor]
level: practitioner
status: docs-checked
description: "MATLAB control design flow: tf/ss plant model, pidtune and margin checks, c2d discretisation, then a fixed-step Simulink controller ready for code generation."
sources:
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.pidtune.html"
  - "https://www.mathworks.com/help/control/ref/pidtuneoptions.html"
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.c2d.html"
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html"
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.allmargin.html"
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.stepinfo.html"
  - "https://www.mathworks.com/help/ident/ref/tfest.html"
  - "https://www.mathworks.com/help/simulink/slref/discretepidcontroller.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MATLAB/Simulink: plant model to a code-generation-ready discrete controller

**Goal:** take a plant (identified or first-principles), tune a controller to explicit
margins in Control System Toolbox, discretise it at a sensible rate, and drop it into a
fixed-step Simulink model that is ready for model-in-the-loop tests and code generation.
For vehicle plant models and HIL rigs see the automotive matlab-simulink skills; this one
stops at the controller.

## 1. Build the plant model
```matlab
s  = tf('s');
% DC-motor speed loop: mechanical pole 20 rad/s, electrical pole 200 rad/s, 1.5 ms delay
G  = 40/((0.05*s+1)*(0.005*s+1));
G.InputDelay = 1.5e-3;           % sensor/PWM/compute delay: never leave it out
Gss = ss(G);                     % state space when you need states or MIMO
```
From test data, use System Identification Toolbox: `data = iddata(y,u,Ts);
G = tfest(data, 2, 0, NaN);` (2 poles, 0 zeros, NaN = estimate the transport delay).
Validate on a **separate** data set, not the one used for fitting.

## 2. Tune with explicit targets
Pick crossover `wc` from what the plant allows: below the first unmodelled resonance,
well below the frequency where the delay eats the phase, and inside actuator limits.
```matlab
wc   = 60;                                  % rad/s target crossover
opts = pidtuneOptions('PhaseMargin',60,'DesignFocus','reference-tracking');
[C, info] = pidtune(G, 'PIDF', wc, opts);   % PIDF = PID with first-order derivative filter
C                                           % shows Kp, Ki, Kd, Tf
L = C*G;
margin(L)                                   % Bode plot with gain and phase margins marked
S = allmargin(L)                            % struct incl. DelayMargin
T = feedback(L,1);  stepinfo(T)             % Overshoot, SettlingTime
```
`DesignFocus` takes `'balanced'` (default), `'reference-tracking'` or
`'disturbance-rejection'`; `PhaseMargin` defaults to 60 degrees.
MathWorks' margin page says gain margins of 3 or more with phase margins between 30 and 60
degrees usually give reasonable bandwidth/stability trade-offs; set your own targets and
also check peak sensitivity `Ms = norm(feedback(1,L),inf)`. Check the controller effort
too: `step(feedback(C,G))` is the u-response to a reference step; if it saturates the
actuator, the linear margins are fiction.

## 3. Choose the sample time and discretise
Sample well above the closed-loop bandwidth, at a rate the target actually runs. The
sample-and-hold adds phase lag at crossover, so re-check margins *after* discretising:
```matlab
Ts  = 1e-3;                                 % 1 kHz, a rate the target runs
Cd  = c2d(C, Ts, 'tustin');                 % controller: Tustin keeps frequency shape
Gd  = c2d(G, Ts, 'zoh');                    % plant: ZOH matches DAC/PWM hold
margin(Cd*Gd)                               % compare with the continuous margins
```
`'zoh'` is the c2d default method. Alternatively tune directly in discrete time:
`pidtune(Gd,'PIDF',wc)` returns a discrete `pid` with `Ts` set; its `IFormula` defaults to
ForwardEuler (BackwardEuler and Trapezoidal are also available). Keep the integrator and
filter methods identical in Simulink and in any hand-written code.
If a filter has poles near crossover, prewarp: `c2d(C,Ts,c2dOptions('Method','tustin','PrewarpFrequency',wc))`
(`PrewarpFrequency` is the current replacement for the old `'prewarp'` method).

## 4. Put it into Simulink, code-generation-ready
1. Use a **Discrete PID Controller** block (Form: Parallel, Time domain: Discrete-time),
   sample time `Ts`, and choose **Integrator method** and **Filter method** (Forward Euler,
   Backward Euler or Trapezoidal) to match `Cd`. The filter coefficient `N` (block default
   100) sets the derivative-filter pole; match it to the `Tf` you tuned. Load gains from
   workspace variables (`C.Kp`, ...) or a `Simulink.Parameter` in a data dictionary, not
   typed-in numbers.
2. Tick **Limit output** at the actuator limits and pick an **Anti-windup method**
   (none is the default; clamping or back-calculation, with back-calculation coefficient
   `Kb`, default 1). Without it, a saturated step produces large overshoot that the linear
   design never showed.
3. Configuration Parameters -> Solver: choose a **fixed-step** solver for the model you will
   generate code from, with a step equal to `Ts` or an integer fraction of it.
4. Make the controller an atomic subsystem or referenced model with explicit
   sample times on its inports.
5. For code, set the system target file and hardware device for your Embedded Coder
   setup, and decide fixed-point or single-precision data types here, not after.

## 5. Model-in-the-loop test
Run the continuous-plant + discrete-controller model on step, ramp and disturbance
cases with the saturation active, and compare with the linear `step(T)`. Gaps point to
saturation, delay or a discretisation mismatch. Log signals with
`Simulink.SimulationOutput` and keep these as regression tests before SIL.

## Verify
- [ ] Plant includes delay and is validated on data it was not fitted to.
- [ ] Continuous loop meets your margin targets and the actuator is not saturated on nominal steps.
- [ ] `Ts` is well above the closed-loop bandwidth and `margin(Cd*Gd)` still meets the targets.
- [ ] Simulink block discretisation methods match the `pid` object used in analysis.
- [ ] Solver is fixed-step; no continuous sample times inside the controller.
- [ ] MIL step response matches the linear prediction; anti-windup tested at saturation.

## Checked
2026-11-01. Confirmed on the MathWorks pages in `sources`: pidtune type `PIDF`, pidtuneOptions
`PhaseMargin` (default 60) and `DesignFocus` values, c2d methods (`zoh` default, `tustin`) and
`PrewarpFrequency`, margin plot and the 3 / 30-60 degree guideline, allmargin `DelayMargin`,
stepinfo `Overshoot`/`SettlingTime`, tfest `NaN` delay, Discrete PID block options (Form, Time
domain, N default 100, methods, anti-windup, Kb default 1). Removed: fit percentage, sample-rate
multiples, phase-lag formula, Ms and margin numeric targets, Kb rule, solver names, menu paths,
`ert.tlc` and `bandwidth`/`compare` details.
Method: documentation only; no commands were run.
