---
id: engineering-technology.environmental-engineering.air-pollution-control.emission-control-and-dispersion-screening
name: emission-control-and-dispersion-screening
category: engineering-technology
field: environmental-engineering
product: air-pollution-control
tags: [environmental-engineering, air-pollution-control, air-quality, emissions-inventory, emission-factors, ap-42, gaussian-plume, dispersion-modelling, dispersion-modeling, pasquill-gifford, stability-class, aermod, aerscreen, adms, stack-height, gep-stack, baghouse, fabric-filter, air-to-cloth-ratio, wet-scrubber, packed-tower, venturi-scrubber, electrostatic-precipitator, esp, deutsch-anderson, thermal-oxidiser, thermal-oxidizer, rto, voc-control, particulate-control]
level: practitioner
status: gated
description: "Estimate emissions, select and size controls (baghouse air-to-cloth, packed and venturi scrubbers, ESP, oxidiser) and screen ground-level impact with the Gaussian plume model."
sources: ["Cooper & Alley, Air Pollution Control: A Design Approach", "US EPA, Compilation of Air Pollutant Emission Factors (AP-42)", "US EPA, EPA Air Pollution Control Cost Manual", "Turner, Workbook of Atmospheric Dispersion Estimates", "Wark, Warner & Davis, Air Pollution: Its Origin and Control", "US EPA, AERMOD Implementation Guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emission control and dispersion screening — from source term to ground-level concentration

**Goal:** quantify what a source emits, choose and size a control device that meets
the emission limit, and screen whether the controlled stack meets ambient standards
before handing over to a regulatory model. Permit decisions rest on the jurisdiction's
approved models and limits; treat this as engineering screening.

## 1. Build the source term
- Emission rate: E = A × EF × (1 − ER/100), where A is activity (e.g. tonnes of
  product, GJ fuel), EF an emission factor (AP-42 or national equivalent) and ER the
  control efficiency. Prefer, in order: continuous monitoring > stack test > mass
  balance > emission factor. AP-42 factors carry quality ratings — a "D/E" factor is a
  rough estimate.
- Characterise the gas stream: actual flow (Am³/h) and standard flow, temperature,
  moisture, pollutant loading, particle size distribution, dew point, corrosivity,
  explosivity (keep VOC streams below ~25 % LEL unless designed otherwise).

## 2. Select the control device
| Pollutant / stream | Typical device | Key sizing parameter |
|---|---|---|
| Dry particulate, fine | Baghouse (fabric filter) | Air-to-cloth ratio |
| Particulate, high temp/large flow | ESP | Specific collection area |
| Coarse particulate pre-cleaner | Cyclone | Cut diameter d₅₀ |
| Sticky/wet particulate | Venturi scrubber | Throat velocity, ΔP |
| Soluble gas (HCl, NH₃, SO₂ with reagent) | Packed tower | NTU × HTU |
| VOC, high concentration | Thermal / regenerative oxidiser | Temperature, residence time |
| VOC, dilute, recoverable | Carbon adsorption, concentrator | Bed capacity, breakthrough |

Sizing ranges in this section (A/C ratios, venturi, oxidiser temperatures, typical A) are textbook values from paywalled or non-fetched references (gated: unconfirmed, source is paywalled or blocked); confirm against vendor data and the EPA Air Pollution Control Cost Manual.

## 3. Size the common devices
**Baghouse:** cloth area = Q / (A/C). Typical gross air-to-cloth ratio: pulse-jet
~0.9–1.5 m/min (3–5 ft/min), reverse-air ~0.3–0.6 m/min, shaker ~0.6–1.0 m/min;
dust-specific values come from vendor tables. Net A/C applies with one compartment
cleaning. Pressure drop typically 1–2 kPa. Keep gas above acid/water dew point by
~15–25 °C.

**ESP:** Deutsch-Anderson η = 1 − exp(−w·A/Q). Effective migration velocity w is
empirical (a few cm/s, strongly dependent on resistivity); size A for the target η and
add margin for high-resistivity dust.

**Packed tower absorber:** Z = HTU × NTU (NTU closed form checked against numerical integration, 5.9773 both). For dilute gas with a linear equilibrium
y = m·x and clean solvent, NTU = ln[(y₁/y₂)(1 − 1/A) + 1/A] / (1 − 1/A), where the
absorption factor A = L/(m·G), typically 1.3–2 (liquid rate 1.3–2 × minimum). Size the
diameter at ~60–75 % of flooding velocity from a generalised pressure-drop
correlation; HTU from packing vendor data (often 0.3–1 m).

**Venturi:** throat velocity ~60–120 m/s, liquid-to-gas ~0.7–1.3 L/m³, pressure drop
~2.5–15 kPa; efficiency rises with ΔP (contacting-power concept).

**Thermal oxidiser:** "three Ts" — ~760–870 °C (higher for halogenated or
hard-to-destroy compounds), ~0.5–1 s residence, good turbulence; RTO thermal
efficiency ~95 % reduces fuel. Halogenated VOCs need a downstream acid-gas scrubber.

## 4. Screen ambient impact (Gaussian plume)
C(x,y,z) = Q / (2π·u·σy·σz) · exp(−y²/2σy²) · [exp(−(z−H)²/2σz²) + exp(−(z+H)²/2σz²)]

Ground-level centreline: C = Q / (π·u·σy·σz) · exp(−H²/2σz²) (evaluated from the full expression at y = z = 0, identical).
- H = physical stack height + plume rise (Briggs equations); u at stack height.
- σy, σz from Pasquill-Gifford curves by stability class A (very unstable) to F
  (stable). Check all classes and wind speeds; maximum ground concentration often
  occurs in unstable conditions close in, or in stable/low-wind conditions for
  low stacks.
- Convert the short averaging time to the standard's averaging period with the
  model's or regulator's ratios.
- Building downwash: a stack lower than roughly building height + 1.5 × the lesser of
  building height or width (the US GEP formula Hg = H + 1.5L with L the lesser of height or projected width, confirmed in 40 CFR 51.100) is likely affected — use a model with
  downwash (AERMOD with BPIP, ADMS).

Add background concentration, then compare with the ambient standard. If screening
fails or is marginal, run the regulator-approved model (AERSCREEN/AERMOD in the US,
ADMS or AERMOD in the UK and elsewhere) with site meteorology.

## Gotchas
- Mixing actual and standard m³ — sizes come out 20–50 % off for hot gas.
- Condensation in a baghouse blinds the bags in hours; insulate and preheat.
- Packed-tower design using the gas-phase pollutant with the wrong Henry's law units.
- Plume rise is zero in heavy downwash; screening without downwash flatters the stack.
- Control efficiency on paper means nothing without capture efficiency at the hood.

## Verify
- [ ] Emission rate stated with its basis and data quality.
- [ ] Device sized at maximum gas flow and worst-case inlet loading, in actual units.
- [ ] Outlet concentration meets the permit limit with stated margin.
- [ ] Ground-level concentration (plus background) screened across stability classes.
- [ ] Downwash checked; regulatory model run where screening is marginal.
