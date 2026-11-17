---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.pressure-pipe-head-loss
name: pressure-pipe-head-loss
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [pressure-pipe, head-loss, hazen-williams, darcy-weisbach, colebrook, minor-losses, hydraulic-grade-line, pump-curve, water-main, friction-factor]
level: practitioner
status: draft
description: "Calculate pressure pipe head loss with Hazen-Williams or Darcy-Weisbach, minor losses, HGL and pump operating point, with C-values, units and limits."
sources: ["Crane Technical Paper 410 Flow of Fluids", "AWWA M32 Computer Modeling of Water Distribution Systems", "Mays, Water Distribution Systems Handbook", "Walski et al., Advanced Water Distribution Modeling and Management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pressure pipe head loss

## Equations
- Darcy-Weisbach (any fluid): hf = f (L/D) V^2/(2g). Swamee-Jain: f = 0.25 / [log10(eps/(3.7 D) + 5.74/Re^0.9)]^2; laminar f = 64/Re; Re = V D / nu.
- Hazen-Williams (water, turbulent, ordinary temperatures only): SI hf = 10.67 L Q^1.852 / (C^1.852 D^4.87) with Q in m3/s and D, L in m. C about 140 for new cement-lined ductile iron, 150 for PVC/PE, lower with age.
- Minor losses: hm = K V^2/(2g) with K from fitting tables. Often small on long mains.

## Method
1. Fix the demand and choose a diameter for a velocity of roughly 0.6 to 2.4 m/s (authority limits vary).
2. Head loss per segment; plot the hydraulic grade line (HGL) = pressure head + elevation along the profile.
3. Keep the HGL above the pipe crown everywhere. Check minimum residual pressure (commonly about 140 kPa / 20 psi under fire flow; rules vary) and the pipe pressure class.
4. Pumps: system curve H = Hstatic + K Q^2 against the pump curve gives the operating point; NPSH available must exceed NPSH required.
5. Surge (water hammer) from valve closure or pump trip needs separate transient analysis.

## Verify
Compute one segment by both equations; they should agree within roughly 10% in the normal water range.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
