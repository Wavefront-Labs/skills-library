---
id: natural-sciences.earth-sciences.geochronology.choosing-and-interpreting-radiometric-ages
name: choosing-and-interpreting-radiometric-ages
category: natural-sciences
field: earth-sciences
product: geochronology
tags: [geochronology, radiometric-dating, u-pb, zircon, concordia, ar-ar, argon-argon, k-ar, radiocarbon, c14, closure-temperature, mswd, weighted-mean, isochron, detrital-zircon, la-icp-ms, id-tims, shrimp, inheritance, lead-loss, isoplotr, sample-selection, half-life]
level: advanced
status: gated
description: "Pick the right dating method for a geological question, collect the right sample, and read the results: concordia, weighted means, MSWD, closure temperature, inheritance."
sources: ["Schoene, U-Th-Pb Geochronology (Treatise on Geochemistry)", "Vermeesch, IsoplotR documentation", "McDougall & Harrison, Geochronology and Thermochronology by the 40Ar/39Ar Method", "https://intcal.org/curves.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing and interpreting radiometric ages

**Goal:** get an age that answers your geological question — which means choosing the
system and sample to match the *event* you care about, then reading the data honestly.

## 1. Start from the question, not the method
Every age dates the moment a mineral **closed** to loss of the daughter isotope. Ask:
which event, which mineral recorded it, and at what temperature?

| Method | Typical material | Useful range | Dates |
|---|---|---|---|
| U-Pb | zircon, monazite, titanite, apatite | ~1 Ma to >4 Ga | crystallisation (zircon closure very high, >900 °C) |
| 40Ar/39Ar | sanidine, biotite, hornblende, muscovite | ~kyr to Ga | cooling through ~300–550 °C depending on mineral; eruption for sanidine |
| Rb-Sr, Sm-Nd | whole rock + minerals (isochrons) | Ma to Ga | metamorphic/igneous equilibration |
| Radiocarbon | organic carbon, carbonate | up to ~50 ka | death of organism; needs calibration |
| (U-Th)/He, fission track | apatite, zircon | Ma | low-T cooling/exhumation (~60–200 °C) |

*Closure temperatures, ranges and precisions in this skill are approximate and depend on grain size and cooling rate (gated: unconfirmed, source is paywalled or blocked).*

## 2. Sample selection
- A fresh, unaltered sample from a known stratigraphic position, logged and photographed.
- Volcanic ash beds date deposition of the host succession; a lava dates itself; a dyke
  dates a minimum age for what it cuts.
- Quantity: several kg of rock for zircon in an intermediate rock; much more for mafic rocks
  (little zircon). Clean all crushing equipment between samples — contamination with a
  previous sample's zircons is a real failure mode.
- **Detrital** zircons give a *maximum* depositional age (the sediment is no older than
  the youngest grain population), not the depositional age itself.

## 3. Reading U-Pb results
- Plot on a **concordia** diagram (Wetherill or Tera-Wasserburg). Concordant analyses sit
  on the curve; discordance indicates Pb loss, common Pb, or mixing of age domains.
- **Inheritance:** older cores inside magmatic zircon. Image grains by cathodoluminescence
  (CL) before analysis and target rims vs cores deliberately.
- **Weighted mean** of concordant, coeval analyses gives the age. Check the **MSWD**: ≈1
  means scatter matches stated uncertainties; much greater than 1 means extra geological
  scatter (Pb loss, inheritance, protracted crystallisation) — don't just quote the mean.
- Method precision: ID-TIMS ~0.1% or better; LA-ICP-MS and SHRIMP typically ~1–2% per
  spot. Systematic (reference-material, decay-constant) uncertainty must be added when
  comparing with ages from other methods or labs.

## 4. Ar/Ar and radiocarbon specifics
- Ar/Ar **step-heating spectra**: look for a plateau (several contiguous steps, >50% of
  39Ar, statistically indistinguishable). Disturbed spectra may record excess argon or
  reheating. The age depends on the flux-monitor standard age used — state it.
- Radiocarbon ages are in "14C years BP" (BP = 1950). **Calibrate** with the current curve
  (IntCal20 for northern-hemisphere terrestrial, SHCal20 for southern, Marine20 for marine; all three are the current curves on intcal.org) using OxCal or CALIB,
  and report the calibrated range with probability. Marine samples need a reservoir
  correction (ΔR).

## 5. Reporting
State the method, mineral, number of analyses used/rejected and why, the age ± 2σ
(analytical and, where relevant, full systematic), MSWD, and the reference materials and
decay constants. Ages should be reproducible from the data table (use IsoplotR).

## Gotchas
- Treating a cooling age as a crystallisation age (or vice versa).
- Rejecting outliers until MSWD looks nice — report the rejection criteria up front.
- Comparing U-Pb and Ar/Ar ages without systematic uncertainties.
- Quoting uncalibrated radiocarbon ages as calendar years.

## Verify
- [ ] The event to be dated and the closure behaviour of the chosen mineral match.
- [ ] Inheritance/Pb loss checked with imaging and concordia, not assumed away.
- [ ] MSWD reported and interpreted; rejection criteria stated.
- [ ] Radiocarbon ages calibrated with a named curve.
