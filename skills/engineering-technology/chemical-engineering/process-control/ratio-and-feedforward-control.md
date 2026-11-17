---
id: engineering-technology.chemical-engineering.process-control.ratio-and-feedforward-control
name: ratio-and-feedforward-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-advanced-regulatory-control, ratio-and-feedforward-control, ratio-control, feedforward-control, lead-lag, disturbance-compensation, blending, wild-flow, feedback-trim, static-feedforward]
level: practitioner
status: gated
description: "Design ratio control and feedforward control (static gain, lead-lag, deadtime) with feedback trim, including typical blending and fuel-air examples."
sources:
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
  - "Smith and Corripio, Principles and Practice of Automatic Process Control (textbook)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ratio and feedforward control

**Goal:** act on a measured disturbance before it affects the controlled variable.

## Ratio control
Keep one flow (controlled) in proportion to another (wild flow): the setpoint of the controlled-flow controller = ratio x measured wild flow. A ratio station may be manual or set by a trim controller (for example, an analyser correcting the blend ratio). Typical use: blending, reactant feed ratio, fuel-air ratio (with cross-limiting for safe combustion; consult the burner management standards and a qualified specialist).

## Feedforward
1. **Model**: the process gain from disturbance G_d(s) and manipulated G_p(s). Ideal feedforward: G_ff = -G_d/G_p.
2. **Static feedforward**: use the steady-state gains: u_ff = -(K_d/K_p) d.
3. **Dynamic compensation**: lead-lag G_ff = -(K_d/K_p) (tau_lead s + 1)/(tau_lag s + 1), with tau_lead = process lag for the manipulated path and tau_lag = lag for the disturbance path; add a delay if the disturbance path is faster than the manipulated path.
4. **Feedback trim**: add the feedforward output to a feedback PID output (bias or summed) to correct model errors; the feedforward does the heavy lifting.
5. Tune the feedforward gain in service by looking at the response to disturbances; adjust the gain in small steps.

## Examples
- Heat exchanger outlet temperature with feedforward from the process flow.
- Boiler drum level: three-element (level, steam flow, feedwater flow) (gated: unconfirmed, source is paywalled or blocked).
- Distillation: feed rate feedforward to reflux/boilup.

## Gotchas
- A badly tuned feedforward can be worse than none; start with static, low gain and increase.
- Disturbance measurements need reliability checks (a failed disturbance signal must not drive the process).

## Verify
- [ ] Open-loop test of a disturbance step: the controlled variable deviation is reduced by the feedforward.
- [ ] A failed signal falls back safely (hold last value or switch to feedback).
