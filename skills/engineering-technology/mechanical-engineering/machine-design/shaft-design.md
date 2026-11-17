---
id: engineering-technology.mechanical-engineering.machine-design.shaft-design
name: shaft-design
category: engineering-technology
field: mechanical-engineering
product: machine-design
tags: [shaft-design, machine-design, machine-elements, fatigue, endurance-limit, marin-factors, goodman, de-goodman, von-mises, stress-concentration, notch-sensitivity, keyway, shoulder-fillet, shaft-deflection, bearing-slope, critical-speed, shigley, power-transmission, torsion, bending, safety-factor]
level: advanced
status: verified
description: "Size a rotating shaft for fatigue (Marin factors, DE-Goodman), stress concentrations, deflection and slope limits at bearings and gears, and critical speed."
sources: ["Budynas and Nisbett, Shigley's Mechanical Engineering Design (McGraw-Hill)", "Norton, Machine Design: An Integrated Approach (Pearson)", "Peterson's Stress Concentration Factors (Wiley)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Shaft design — strength, fatigue, stiffness, speed

**Goal:** choose diameters and features so a rotating shaft survives infinite-life fatigue
with a stated safety factor, keeps bearings and gears within slope/deflection limits,
and runs well below its first critical speed. Numbers below follow Shigley (SI); check
the edition you use, as fitted constants are revised occasionally. Shigley is paywalled, so Marin constants, Kt values, reliability factors and the slope/deflection limits are recalled and unconfirmed (gated: unconfirmed, source is paywalled or blocked); the worked example was recomputed.

## 1. Layout and loads
1. Place bearings close to heavy loads, gears/pulleys near bearings. Short shafts are
   stiff shafts.
2. Resolve gear/pulley forces into two planes, solve reactions, draw shear, bending
   moment (combine planes vectorially: `M = sqrt(My^2 + Mz^2)`) and torque diagrams.
3. Critical sections: maximum moment, every shoulder, keyseat and ring groove near
   moment.

## 2. Endurance limit with Marin factors
`Se = ka kb kc kd ke kf Se'`, with `Se' = 0.5 Sut` (Sut <= 1400 MPa), else 700 MPa.

| Factor | Value |
|---|---|
| ka surface `a Sut^b` (MPa) | ground 1.58, -0.085; machined/cold-drawn 4.51, -0.265; hot-rolled 57.7, -0.718; as-forged 272, -0.995 |
| kb size (rotating) | `1.24 d^-0.107` for 2.79–51 mm; `1.51 d^-0.157` for 51–254 mm |
| kc load | 1 for bending; use 1 when combining via von Mises |
| kd temperature | 1 near room temperature |
| ke reliability | 50 % 1.0, 90 % 0.897, 99 % 0.814, 99.9 % 0.753 |

Example: 1050 CD (Sut ~690 MPa), machined, d = 40 mm, 99 %: ka = 4.51 × 690^-0.265 = 0.798, kb = 1.24 × 40^-0.107 = 0.836,
Se = 0.798 × 0.836 × 0.814 × 345 = 187 MPa (computed; the ~190 MPa shown earlier is consistent) — barely over half of `Se'`.

## 3. Stress concentrations
`Kf = 1 + q (Kt - 1)`; q from notch-sensitivity charts (approaches 1 for hard steels
and larger radii). First-pass Kt (bending/torsion) before geometry is known (gated: unconfirmed, source is paywalled or blocked):
sharp shoulder (r/d ~0.02) 2.7/2.2; well-rounded shoulder (r/d ~0.1) 1.7/1.5;
end-milled keyseat 2.14/3.0; retaining-ring groove 5.0/3.0. Replace with chart values
once r/d and D/d are set.

## 4. Fatigue diameter (DE-Goodman)
Typical rotating shaft, steady torque: alternating moment `Ma = M`, mean torque
`Tm = T`, `Mm = Ta = 0`.

```
d = { (16 n / pi) * [ (2 Kf Ma)/Se + sqrt(3) Kfs Tm / Sut ] }^(1/3)
```

General form uses `sqrt(4 (Kf Ma)^2 + 3 (Kfs Ta)^2)` and the mean equivalent likewise.
Iterate: d changes kb and q. Also check first-cycle yield with von Mises maximum
stress `sigma_max' = sqrt((sig_a + sig_m)^2 + 3 (tau_a + tau_m)^2) <= Sy / n_y`.
Gerber or ASME-elliptic are less conservative alternatives; Goodman is the usual
design choice. Target n ~1.5–2 for well-defined loads, higher for shock (practice figure (gated: unconfirmed, source is paywalled or blocked)).

## 5. Deflection and slope
Compute by superposition, singularity functions or numeric integration of `M/EI`
(stepped diameters matter). Typical limits (Shigley table):

| Location | Limit |
|---|---|
| Tapered roller bearing slope | 0.0005–0.0012 rad |
| Cylindrical roller bearing slope | 0.0008–0.0012 rad |
| Deep-groove ball bearing slope | 0.001–0.003 rad |
| Spur gear mesh, relative slope | < 0.0005 rad |
| Spur gear transverse deflection | ~0.25 mm (0.010 in) coarse pitch P<10, ~0.13 mm P 11–19, ~0.08 mm P 20–50 |

Stiffness is from E, so a higher-strength steel does **not** fix a deflection problem —
only diameter or bearing spacing does. Deflection scales with `d^-4`.

## 6. Critical speed
Rayleigh estimate for lumped masses: `w1 = sqrt( g * sum(wi yi) / sum(wi yi^2) )`
with static deflections yi. Keep the first critical at least **2x** operating speed (rule of thumb (gated: unconfirmed, source is paywalled or blocked))
(or justify running supercritical with a rotordynamics analysis).

## 7. Gotchas
- Keyseat ends and ring grooves at high-moment sections often govern — move them.
- Shoulder fillet radius is limited by bearing chamfer; use a relief groove or
  spacer to get a larger radius.
- Press fits add fretting and a Kt of roughly 2 or more at the hub edge (gated: unconfirmed, source is paywalled or blocked).
- Reversing torque makes torsion alternating, not mean.

## Verify
- [ ] Every critical section checked (max M, each shoulder, keyseat, groove).
- [ ] n_fatigue and n_yield both above target, with iterated kb and q.
- [ ] Bearing slopes and gear slopes/deflections within the table limits.
- [ ] First critical speed >= 2x maximum operating speed.
- [ ] Bending moment diagram reactions sum to the applied loads in both planes.
