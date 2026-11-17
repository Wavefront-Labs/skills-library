---
id: engineering-technology.marine-naval-engineering.naval-architecture.resistance-and-powering-estimate
name: resistance-and-powering-estimate
category: engineering-technology
field: marine-naval-engineering
product: naval-architecture
tags: [naval-architecture, resistance, powering, holtrop-mennen, ittc-1957, friction-line, form-factor, wave-resistance, effective-power, delivered-power, propulsive-efficiency, hull-efficiency, wake-fraction, thrust-deduction, sea-margin, engine-margin, mcr, froude-number, reynolds-number, concept-design]
level: practitioner
status: gated
description: "Estimate calm-water resistance with Holtrop-Mennen/ITTC-1957 and size installed power: PE, propulsive efficiency, shaft losses, sea margin and MCR, with worked example."
sources:
  - "Holtrop & Mennen, An approximate power prediction method, International Shipbuilding Progress (1982)"
  - "Holtrop, A statistical re-analysis of resistance and propulsion data (1984)"
  - "ITTC Recommended Procedures 7.5-02-03-01.4, 1978 ITTC performance prediction method"
  - "Molland, Turnock & Hudson, Ship Resistance and Propulsion (Cambridge University Press)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resistance and powering estimate (concept stage)

**Goal:** from main dimensions and a service speed, get a defensible installed-power
figure (MCR) within roughly +/-10 %, and know which assumptions drive the error.

## 1. Fix the inputs
- L (use LWL for resistance), B, T, displacement volume, Cb, Cp, Cm, Cwp, LCB (% L
  from midships), wetted surface S (from hydrostatics, or the Holtrop regression),
  transom immersed area, bulb area, appendages.
- Water: sea water at 15 C, density 1025 kg/m3, kinematic viscosity about
  1.19e-6 m2/s ((gated: unconfirmed, source is paywalled or blocked); take the exact value from ITTC tables for your temperature).
- Non-dimensionals: Fn = V / sqrt(gL), Rn = VL / nu.

## 2. Build the resistance (Holtrop-Mennen structure)
RT = RF(1 + k1) + RAPP + RW + RB + RTR + RA

1. **Friction, ITTC-1957 line:** CF = 0.075 / (log10 Rn - 2)^2 (ITTC-1957 line, standard form; ITTC PDF not fetched, (gated: unconfirmed, source is paywalled or blocked)), RF = 0.5 rho V^2 S CF.
2. **Form factor (1 + k1)** from the Holtrop regression (typically 1.15-1.35 for
   full merchant hulls, (gated: unconfirmed, source is paywalled or blocked)); it is very sensitive to LCB and the run length.
3. **Wave resistance RW** from the Holtrop formula; note it changes form above
   Fn about 0.40 (the 1984 version interpolates between low- and high-speed fits) ((gated: unconfirmed, source is paywalled or blocked); the scanned 1982 paper text read was too garbled to confirm).
4. **Bulb (RB), immersed transom (RTR), appendages (RAPP)** as separate terms.
5. **Correlation allowance RA** (model-ship correlation, includes hull roughness).
6. Stay inside the regression's database: commonly quoted as Fn < 0.45, Cp 0.55-0.85, L/B 3.9-15 and B/T 2.1-4.0 (from a secondary forum summary, (gated: unconfirmed, source is paywalled or blocked); an earlier version of this skill said L/B up to 9.5, which could not be confirmed; check the exact limits in Holtrop and Mennen 1982/1984 or your software). Outside it,
   use a series that matches the hull type or CFD/model tests.

## 3. From resistance to power
1. Effective power PE = RT x V.
2. Propulsive coefficients (from Holtrop regressions or similar ships): wake fraction
   w, thrust deduction t, relative rotative efficiency etaR (0.98-1.02 single screw, (gated: unconfirmed, source is paywalled or blocked)),
   open-water efficiency eta0 from the propeller (see
   engineering-technology.marine-naval-engineering.marine-propulsion.propeller-selection-and-engine-matching).
3. Hull efficiency etaH = (1 - t) / (1 - w); quasi-propulsive etaD = etaH x eta0 x etaR,
   usually 0.60-0.75 for conventional single-screw ships ((gated: unconfirmed, source is paywalled or blocked)).
4. Delivered power PD = PE / etaD; brake power PB = PD / etaS with shaft/gearing
   efficiency etaS about 0.98-0.99 (direct drive) or about 0.96 with a gearbox ((gated: unconfirmed, source is paywalled or blocked)).
5. **Margins:** add a sea margin (commonly 15 %, chosen by route, (gated: unconfirmed, source is paywalled or blocked)) for weather and
   fouling, then size the engine so the service point sits at about 85-90 % MCR
   (the engine margin, (gated: unconfirmed, source is paywalled or blocked)).

## Worked mini-example
(Recomputed: Rn 6.05e8, log10 Rn 8.782, CF 1.631e-3, PE 2160, PD 3086, PB 3149, with sea margin 3621, MCR 4023 kW; 14 kn = 7.20 m/s.)
L = 100 m, V = 14 kn = 7.20 m/s, nu = 1.19e-6 m2/s.
- Rn = 7.20 x 100 / 1.19e-6 = 6.05e8; log10 Rn = 8.78; CF = 0.075 / 6.78^2 = 1.63e-3.
- Suppose the full build-up gives RT = 300 kN. PE = 300 x 7.20 = 2160 kW.
- etaD = 0.70: PD = 3086 kW; etaS = 0.98: PB = 3149 kW (trial, calm, clean).
- +15 % sea margin: 3621 kW at service; at 90 % MCR, MCR = 3621 / 0.90 = about 4020 kW.
Select the nearest engine rating above about 4000 kW and re-check with its actual
propeller law and layout diagram.

## Gotchas
- **Wetted surface** errors pass straight into RF, which is often 60-80 % of RT for
  slow full ships ((gated: unconfirmed, source is paywalled or blocked)). Use measured S, not a guess.
- **Units in Holtrop:** LCB sign convention (forward positive in the paper) and the
  use of LWL vs LPP trip people up; check the implementation you use.
- **Trial vs service:** contracts quote trial speed at a draft and power; do not
  compare a service-margined figure with a trial curve.
- The 1978 ITTC method (with roughness allowance) is for extrapolating model tests;
  do not mix its correlation terms with Holtrop's RA.
- Recent revisions of Holtrop-type regressions exist; results differ by a few percent.
  State which version you used.

## Verify
- [ ] Fn, Cp, L/B and B/T are inside the method's database at every speed reported.
- [ ] CF hand-check agrees with the tool to three significant figures.
- [ ] etaD falls in a plausible band for the hull type and propeller.
- [ ] PB at the service point includes shaft losses and the chosen sea margin.
- [ ] MCR leaves the service point at about 85-90 % load.
