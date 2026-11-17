---
id: transportation-logistics.diving-life-support-craft.gas-blending-management.partial-pressure-blending-and-gas-analysis
name: partial-pressure-blending-and-gas-analysis
category: transportation-logistics
field: diving-life-support-craft
product: gas-blending-management
tags: [diving-life-support-craft, gas-blending-management, gas-blending, partial-pressure-blending, nitrox, eanx, heliox, trimix, oxygen-analyser, oxygen-analysis, helium-analysis, mod, maximum-operating-depth, ppo2, fo2, oxygen-cleaning, oxygen-compatible, gas-quad, cylinder-bank, consumption-planning, gas-reserves, labelling, hypoxic-mix, gas-transfer, haskel-pump, booster-pump, daltons-law, commercial-diving, technical-diving]
level: advanced
status: gated
description: "Blend nitrox and heliox by partial pressure, compute MOD and ppO2, analyse and label every cylinder, handle oxygen safely, and plan gas quantities and reserves."
sources: ["https://www.ecfr.gov/current/title-29/part-1910/subpart-T", "https://www.hse.gov.uk/diving/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial-pressure blending and gas analysis

**Goal:** every cylinder or quad contains the mix its label says, you can prove it with a
fresh analysis, and there's enough of it for the job plus emergencies.

> Draft: arithmetic and practice common to commercial and technical diving. Gas blending
> with oxygen is a trained, certified task; equipment must be oxygen-clean where
> required. Real blends need temperature allowances and the use of your blending
> procedures. Figures assume ideal-gas behaviour (helium deviates noticeably at high
> pressure).

## 1. Core relationships (Dalton's law)
- **ppGas = FGas × P_absolute** (bar). At depth in seawater: P_abs ≈ (depth m ÷ 10) + 1.
- **MOD** (maximum operating depth) for a max ppO₂: MOD (msw) = (ppO₂max ÷ FO₂ − 1) × 10.
  Example: 32% at ppO₂ 1.4 → (1.4/0.32 − 1) × 10 ≈ **33.7 m**.
- Minimum depth for a hypoxic mix: e.g. a heliox with 5% O₂ gives only 0.05 bar at the
  surface — **not breathable at the surface**; it must only be breathed at depth.

## 2. Nitrox by partial pressure (top-up with air)
To make FO₂ target at final pressure P from an empty cylinder:
**O₂ to add (bar) = P × (FO₂target − 0.21) ÷ (1 − 0.21)**, then top up with oxygen-
compatible air to P.
Example: 32% at 200 bar → 200 × 0.11 / 0.79 ≈ **27.8 bar O₂**, then air to 200 bar.
- Fill oxygen **slowly** (heat and adiabatic compression ignite contaminants);
  keep to the fill rate your procedure sets for O₂.
- Let the cylinder cool and re-check pressure; top up if needed.

## 3. Heliox
- Commercial heliox is usually supplied **premixed** in quads/banks at fixed O₂%, or mixed
  on site by adding O₂ to helium (or blending two heliox mixes).
- Mixing two mixes to a target: by mass balance — e.g. combining P1 at F1 with P2 at F2
  gives F = (P1F1 + P2F2)/(P1 + P2) (ideal-gas approximation).
- Allow time for mixing (gas stratifies) — roll cylinders or wait before analysing.

## 4. Analysis
1. **Calibrate** the O₂ analyser: air (20.9%), and pure O₂ if the analyser and procedure
   call for a two-point calibration.
2. Analyse **every cylinder/quad** individually, at a controlled flow, with the reading
   stabilised.
3. Helium analysers for trimix; CO and other contaminant testing per schedule.
4. Two people sign: blender and diver/supervisor. Label: **O₂% (and He%), MOD, pressure,
   date, analyst initials**.
5. Re-analyse after any transfer, on receipt of delivered gas, and before connecting to
   a panel.

## 5. Oxygen safety
- Oxygen-clean components (no hydrocarbons) for gases over a set threshold (often 40%
  O₂ in many standards, some apply 23.5%; confirm yours (gated: unconfirmed, source is paywalled or blocked)).
- Open valves slowly; never use oil or grease; no smoking or naked flames near O₂.
- Ventilate the blending area; O₂-enriched clothing burns readily.

## 6. Consumption and reserves
- Consumption at depth = surface rate × P_abs. Example: demand helmet working diver
  ~40 L/min surface equivalent (illustrative; your manual has figures) at 30 m (4 bar)
  → 160 L/min.
- Quad capacity (litres of free gas) ≈ water volume × pressure (e.g. 64 × 50 L × 200 bar
  ≈ 640,000 L, ideal-gas).
- Plan: job duration × consumption × divers + **contingency** (treatment, bailout
  recharge, a lost day) per your company rule.

## Gotchas
- Mislabelled or un-analysed gas is a classic killer — analyse yourself, every time.
- Hot cylinders read high: analyse and measure pressure when cool.
- Heliox mixes deviate from ideal-gas arithmetic at high pressure — expect corrections.

## Verify
- [ ] MOD and ppO₂ computed for every mix on the job.
- [ ] Blend calculation done before filling; slow O₂ fill.
- [ ] Every cylinder analysed with a calibrated analyser and labelled with signatures.
- [ ] O₂-clean equipment used where the threshold requires it.
- [ ] Gas reserves cover the plan plus contingency.

## Checked

Jurisdiction: not applicable (gas-law arithmetic; diving regulators such as OSHA 29 CFR 1910 Subpart T or HSE apply to commercial work and were not read). Checked 2026-10-25 by recomputation: MOD for 32 percent at ppO2 1.4 = (1.4/0.32 - 1) x 10 = 33.75 m (skill says 33.7); O2 to add for 32 percent at 200 bar = 200 x 0.11/0.79 = 27.85 bar (skill 27.8); 5 percent O2 at the surface gives 0.05 bar; 64 x 50 L x 200 bar = 640,000 L. Oxygen-clean threshold left gated.

Method: documentation only; no commands were run.
