---
id: engineering-technology.aerospace-engineering.aerodynamics.drag-polar-build-up
name: drag-polar-build-up
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, drag-polar, drag-build-up, component-build-up, parasite-drag, cd0, zero-lift-drag, skin-friction, form-factor, interference-factor, wetted-area, induced-drag, oswald-efficiency, lift-to-drag, l-d-max, wave-drag, korn-equation, drag-divergence, transonic, conceptual-design, raymer, aircraft-performance]
level: practitioner
status: verified
description: "Estimate an aircraft drag polar by component build-up: skin-friction CD0 with form and interference factors, induced drag via Oswald e, and wave drag."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Anderson, Fundamentals of Aerodynamics"
  - "Hoerner, Fluid-Dynamic Drag"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
  - "Mason, Configuration Aerodynamics course notes (Virginia Tech)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Drag polar by component build-up — CD = CD0 + K·CL² (+ wave)

**Goal:** a defensible parabolic drag polar for a conceptual aircraft, built component by
component, sanity-checked against known aircraft before it feeds performance and sizing.

## 1. Parasite drag (CD0) — sum over components
```
CD0 = [ Σ (Cf_c · FF_c · Q_c · Swet_c) ] / Sref  +  CD_misc  +  CD_L&P
```
**Skin friction Cf** per component at cruise Reynolds number on its own length:
- Turbulent (Raymer's form, with compressibility):
  `Cf = 0.455 / [ (log10 Re)^2.58 · (1 + 0.144 M²)^0.65 ]`
- Laminar: `Cf = 1.328 / sqrt(Re)`. Use a laminar fraction only for genuinely smooth
  surfaces (composite GA wings maybe 10–50%; metal transports ~0).
- Surface roughness: if `Re` exceeds the roughness cut-off Reynolds number
  (Raymer gives `Re_cutoff ≈ 38.21 (l/k)^1.053` subsonic, k = roughness height), use the
  cut-off instead. This matters for painted or rough surfaces at high Re.

**Form factors FF** (Raymer; every Raymer constant in this skill is (gated: unconfirmed, source is paywalled or blocked)):
- Wing/tail: `FF = [1 + 0.6/(x/c)_m · (t/c) + 100 (t/c)^4] · [1.34 M^0.18 (cos Λ_m)^0.28]`,
  where (x/c)_m is max-thickness location and Λ_m the sweep of that line.
- Fuselage/canopy: `FF = 1 + 60/f³ + f/400`, with fineness `f = l/d`.
- Nacelle/smooth store: `FF = 1 + 0.35/f`.

**Interference Q:** nacelle mounted on the fuselage ~1.3–1.5, closer than one diameter
to the wing ~1.3, more than one diameter away ~1.0; filleted high/mid wing ~1.0,
unfilleted low wing 1.1–1.4; conventional tail ~1.03–1.05.

**Wetted area:** wing `Swet ≈ Sexposed · (1.977 + 0.52 t/c)`; fuselage from the CAD or a
sum of frustums. Use exposed areas only (inside-fuselage wing area does not count).

**Misc and leakage/protuberance:** upsweep, base areas, gear, flaps added separately;
L&P typically 2–5% of CD0 for transports, more for military/GA.

## 2. Induced drag
`K = 1 / (π A e)`. Oswald efficiency for preliminary work (Raymer-type fits (gated: unconfirmed, source is paywalled or blocked)):
- Straight wing: `e ≈ 1.78 (1 − 0.045 A^0.68) − 0.64`
- Swept (Λ_LE > 30°): `e ≈ 4.61 (1 − 0.045 A^0.68) (cos Λ_LE)^0.15 − 3.1`
Typical e = 0.75–0.85. Winglets: model as an effective span increase, and check the
added wetted area. Cambered wings have min drag at CL > 0; for them use
`CD = CD_min + K (CL − CL_minD)²`.

## 3. Wave drag (transonic)
- Korn equation for drag divergence (gated: unconfirmed, source is paywalled or blocked):
  `M_DD = κ_A / cos Λ − (t/c)/cos² Λ − CL/(10 cos³ Λ)`, κ_A ≈ 0.87 conventional
  sections, ≈ 0.95 supercritical (t/c and sweep at the appropriate chord line).
- Critical Mach: `M_cr ≈ M_DD − (0.1/80)^(1/3)` (definition where dCD/dM = 0.1).
- Lock's approximation: `CD_wave ≈ 20 (M − M_cr)^4` for M > M_cr. This is crude; above
  M_DD trust CFD or test data, not the formula.

## 4. Sanity numbers
Typical ranges from the sources named, not confirmed individually (gated: unconfirmed, source is paywalled or blocked).
| Aircraft class | CD0 | e | (L/D)max |
|---|---|---|---|
| Jet transport (clean) | 0.015–0.020 | 0.75–0.85 | 17–20 |
| Business jet | 0.018–0.022 | ~0.8 | 13–17 |
| Light GA, fixed gear | 0.025–0.035 | 0.7–0.8 | 10–13 |
| Sailplane | 0.008–0.012 | 0.85–0.95 | 40–60 |
`(L/D)max = 0.5 · sqrt(π A e / CD0)` at `CL* = sqrt(CD0 / K)`. If your build-up gives a
transport L/D of 25, a term is missing. Ranges here are typical, not certified values.

## Gotchas
- Every Cf uses that component's own reference length, not the MAC.
- Divide everything by the single Sref used for CL; mixing references is common.
- Trim drag (tail download) and cooling/excrescence drag are easy to forget; budget them.
- Takeoff and landing polars need flap/gear increments (ESDU or Raymer charts), not cruise
  CD0 with a higher CL.

## Verify
- [ ] Each component's Re, Cf, FF, Q and Swet are tabulated; the sum reproduces CD0.
- [ ] CD0 and (L/D)max fall in the class ranges above or the gap is explained.
- [ ] Re-running the method on a known aircraft lands within ~10% of its published CD0.
- [ ] e is in 0.7–0.9 and consistent with planform and sweep.
- [ ] Cruise Mach is below M_DD, or wave drag is explicitly added.
