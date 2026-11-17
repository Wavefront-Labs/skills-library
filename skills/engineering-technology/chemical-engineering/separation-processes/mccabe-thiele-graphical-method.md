---
id: engineering-technology.chemical-engineering.separation-processes.mccabe-thiele-graphical-method
name: mccabe-thiele-graphical-method
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-distillation-shortcuts, mccabe-thiele-graphical-method, mccabe-thiele, binary-distillation, operating-line, q-line, stage-stepping, minimum-reflux, xy-diagram, graphical-design]
level: practitioner
status: verified
description: "Construct McCabe-Thiele diagrams for binary distillation: operating lines, q-line, minimum reflux pinch, stage stepping, multiple feeds and side streams."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# McCabe-Thiele graphical method

**Goal:** the stage count, feed stage and reflux for a binary column, and an intuitive picture of why.

## Assumptions
Constant molar overflow (similar molar latent heats, no heat loss), constant relative volatility or an equilibrium curve from data, saturated products.

## Construction
1. Plot the equilibrium curve y vs x and the 45-degree line.
2. Mark x_D, x_F, x_B on the diagonal.
3. **q-line**: through (x_F, x_F) with slope q/(q - 1).
4. **Rectifying line**: y = [R/(R + 1)] x + x_D/(R + 1), through (x_D, x_D).
5. **Stripping line**: from (x_B, x_B) to the intersection of the rectifying line with the q-line.
6. **Step off stages** from the top: horizontal to the equilibrium curve, vertical to the operating line, switching lines at the q-line intersection (the optimal feed stage).
7. **Minimum reflux**: draw the rectifying line through the intersection of q-line and equilibrium curve (or tangent to the curve for non-ideal systems); R_min/(R_min + 1) = intercept slope.
8. The number of stages (including the reboiler as a stage) and the optimal feed tray follow.

## Extensions
Side streams and multiple feeds give extra operating lines (changed slopes). Murphree efficiency can be included by stepping with a lowered equilibrium curve. Open steam stripping uses the line through (x_B, 0).

## Gotchas
- Pinch at a tangent below the intersection occurs for non-ideal (S-shaped) curves.
- Check (computed): stepping benzene-toluene alpha 2.4, z 0.5, q 1, x_D 0.95, x_B 0.05 at R = 1.54 with these lines gives 14 stages with the feed on stage 7, consistent with the shortcut estimate of 14.6.
- Resolution on paper is poor near the corners; use a numerical stepper (spreadsheet).

## Verify
- [ ] Stage count agrees within one stage with a rigorous model.
- [ ] Material balance from the operating lines matches D and B from the overall balance.
