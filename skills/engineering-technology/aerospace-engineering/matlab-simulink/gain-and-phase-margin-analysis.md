---
id: engineering-technology.aerospace-engineering.matlab-simulink.gain-and-phase-margin-analysis
name: gain-and-phase-margin-analysis
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, control-design-matlab, margin-analysis, margin, allmargin, diskmargin, loop-breaking, stability-margins]
level: practitioner
status: docs-checked
description: "Compute classical and disk stability margins of a flight control loop in MATLAB, break loops at plant input and output, and report them against typical requirements."
sources:
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html"
  - "https://www.mathworks.com/help/robust/ref/dynamicsystem.diskmargin.html"
  - "https://www.mathworks.com/help/slcontrol/ug/sllinearizer.getlooptransfer.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Gain and phase margin analysis

**Goal:** margins that mean what the requirement means.

## Commands
```matlab
L = getLoopTransfer(slLin, 'u_cmd', -1);   % loop broken at the plant input
[Gm, Pm, Wcg, Wcp] = margin(L);              % classical margins
allmargin(L)                                 % all crossovers
[DM, MM] = diskmargin(L);                    % Robust Control Toolbox: DM loop-at-a-time, MM multiloop
```
`getLoopTransfer` on an `slLinearizer` object (Simulink Control Design) returns the positive-feedback loop transfer by default; the third argument `-1` is the sign, giving the negative-feedback form that `margin` assumes. A temporary opening can be passed before the sign to open an outer loop.

## Practice
1. Break the loop at each actuator input (and at sensor outputs for multi-loop) one at a time, then all together.
2. The required margins come from the programme or certification basis; cite that document.
3. Check margins across the flight envelope grid and with uncertainty (mass, cg, aerodynamic derivatives).
4. Report minimum margin and the frequency.

## Gotchas
- Single-loop margins are misleading for multi-loop systems; use disk margin or multi-loop analysis.
- Time delay and actuator rate limits do not appear in linear margins: simulate large-signal separately.

## Verify
- [ ] Margin values reproduce from a manual Bode inspection.
- [ ] Margins hold across the grid of flight conditions.

## Checked
2026-11-01. Confirmed on the MathWorks pages read: margin syntax `[Gm,Pm,Wcg,Wcp] = margin(sys)` with allmargin and diskmargin cross-referenced and disk margins described as more reliable for multivariable systems; diskmargin syntax `[DM,MM]` (Robust Control Toolbox) with simultaneous gain and phase variation; getLoopTransfer sign (+1 default) and temporary opening. Removed: the 6 dB / 45 degree target figures and the textbook source.
Method: documentation only; no commands were run.
