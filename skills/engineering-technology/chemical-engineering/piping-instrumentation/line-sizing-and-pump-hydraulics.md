---
id: engineering-technology.chemical-engineering.piping-instrumentation.line-sizing-and-pump-hydraulics
name: line-sizing-and-pump-hydraulics
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, p-and-id, pid-drawing, line-sizing, pipe-sizing, hydraulics, darcy-weisbach, friction-factor, colebrook, swamee-jain, moody, pressure-drop, velocity-limits, erosional-velocity, api-rp-14e, pump-sizing, system-curve, pump-curve, npsh, npsha, npshr, control-valve, cv, valve-sizing, isa-5.1, isa-75, centrifugal-pump, fluidflow, pipe-flo, aspen-hydraulics]
level: practitioner
status: gated
description: "Size process lines and check pump hydraulics: velocity and dP/100 m criteria, Darcy-Weisbach, system curve, NPSH available vs required, control-valve dP allowance."
sources:
  - "Crane Technical Paper 410 (method only)"
  - "Hydraulic Institute ANSI/HI 9.6.1 guidance on NPSH margin (paraphrased)"
  - "https://www.bsee.gov/sites/bsee.gov/files/tap-technical-assessment-program/131af.pdf (SwRI for Minerals Management Service, Erosional/Corrosional Testing for Multiphase Flow Lines, 1995)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line sizing and pump hydraulics

**Goal:** pick line sizes that meet velocity and pressure-drop criteria, then build the
system curve that sets pump head, NPSH margin and control-valve ΔP for the P&ID and the
pump datasheet.

## 1. Screening criteria (use your company's line-sizing standard if it exists)
Indicative values, liquids of water-like viscosity (company-standard rules of thumb (gated: unconfirmed, source is paywalled or blocked)):
| Service | Velocity | ΔP |
|---|---|---|
| Pump suction | 0.6–1.5 m/s | ≤ ~0.1–0.2 bar/100 m |
| Pump discharge | 1.5–3 m/s | ~0.2–0.5 bar/100 m |
| Gravity / sewer | 0.5–1 m/s, self-venting | available head |
| Gas / vapour | 10–30 m/s, check ρv² | ~0.05–0.2 bar/100 m (pressure-dependent) |
| Two-phase | check erosional velocity, flow regime | — |
API RP 14E's erosional velocity V_e = C/√ρ (US units: ft/s, lb/ft³, C = 100 for continuous and 125 for intermittent service, 150-200 only where corrosion is controlled and no solids are present, per the SwRI report for the Minerals Management Service) is common for two-phase; it is a screening rule, not physics.
Slurries: stay above deposition velocity. Relief inlet/outlet lines follow the relief rules,
not this table.

## 2. Pressure drop (Darcy–Weisbach)
ΔP = f·(L_eq/D)·ρv²/2, with Re = ρvD/μ.
Turbulent f (Swamee–Jain, explicit): f = 0.25/[log₁₀(ε/(3.7D) + 5.74/Re^0.9)]²;
commercial steel ε ≈ 0.045 mm. Laminar f = 64/Re. Fittings: K-values or equivalent
lengths, ΔP = K·ρv²/2.
**Worked:** water 100 m³/h. 4-in Sch 40 (ID 102 mm) gives 3.4 m/s, too fast for discharge.
6-in Sch 40 (ID 154 mm): v = 1.49 m/s, Re ≈ 2.3e5, f ≈ 0.0175,
ΔP/100 m = 0.0175·(100/0.154)·1000·1.49²/2 ≈ 0.13 bar (recomputed: v = 1.489 m/s, Re = 2.3e5, f = 0.0174-0.0175, 0.126 bar; the 4-in case gives v = 3.38 m/s). Acceptable; for long lines compare
5-in vs 6-in on installed cost plus pumping energy.

## 3. System curve and pump head
H_system(Q) = (P_dest − P_source)/(ρg) + (z_dest − z_source) + h_friction(Q) + h_cv(Q).
Friction scales with ~Q² (slightly less in transition). Evaluate at rated flow (normal ×
1.1–1.2 design margin, state yours) and at minimum flow. Plot against the vendor pump curve;
the operating point sits where they cross. Keep the rated point near best efficiency
(roughly 80–110% of BEP flow (gated: unconfirmed, source is paywalled or blocked)) and stay above the vendor's minimum continuous stable flow;
add a minimum-flow recycle if the process can turn down below it.

## 4. NPSH
NPSH_a = (P_surface − P_vapour)/(ρg) + z_liquid above impeller − h_f,suction.
Use the **lowest** liquid level and highest temperature (vapour pressure) at the worst case.
Liquid at its bubble point (drum, column bottoms) means the first term is zero: NPSH_a is just
elevation minus friction, which is why bottoms pumps sit low and drums sit high.
Margin: NPSH_a ≥ NPSH_r (NPSH3) plus margin; ANSI/HI 9.6.1 gives margin ratios by service and suction energy (confirm values in the current edition (gated: unconfirmed, source is paywalled or blocked)), and many owners also require a minimum absolute margin.
NPSH_r rises at high flow; check at rated, not normal.

## 5. Control-valve ΔP allowance
The valve needs enough ΔP to control: a common rule is ~25–33% of the system's dynamic
(frictional) loss at design flow, or a minimum around 0.7 bar for pumped liquids (gated: unconfirmed, source is paywalled or blocked). Too little
gives a valve that sits wide open and can't control; too much wastes pump energy.
Liquid sizing (US units): Cv = Q·√(SG/ΔP) with Q in US gpm, ΔP in psi; use the full
IEC 60534 / ISA-75.01 equations for flashing, cavitation and choked flow. Select so normal flow
sits at ~50–80% open (characteristic-dependent).

## 6. Put it on the P&ID
Line number with size, spec class and insulation; pump with suction strainer, isolation
valves, discharge check valve, minimum-flow line; instrument bubbles per ISA-5.1 (FT, FV,
PI on suction/discharge); relief devices where the pump shut-off head can exceed downstream
design pressure (relief sizing per the current API 520/521 and reviewed by a competent
person).

## Verify
- [ ] Every line meets the velocity/ΔP standard, or the exception is justified.
- [ ] System curve at min/normal/rated flow plotted against the pump curve.
- [ ] NPSH_a at worst case exceeds NPSH_r with the required margin.
- [ ] Control valve has adequate ΔP and opening range at min and max flow.
- [ ] Shut-off head vs downstream design pressure checked.
