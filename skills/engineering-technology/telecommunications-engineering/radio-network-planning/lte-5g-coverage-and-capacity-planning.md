---
id: engineering-technology.telecommunications-engineering.radio-network-planning.lte-5g-coverage-and-capacity-planning
name: lte-5g-coverage-and-capacity-planning
category: engineering-technology
field: telecommunications-engineering
product: radio-network-planning
tags: [telecommunications-engineering, radio-network-planning, lte, 5g-nr, cellular-planning, coverage-planning, capacity-planning, rsrp, sinr, rsrq, mapl, okumura-hata, cost-231-hata, 3gpp-38-901, propagation-model, model-tuning, atoll, planet, pci-planning, site-count, cell-range, drive-test, tems, nemo, shadow-fading, penetration-loss, link-budget]
level: practitioner
status: gated
description: "Plan LTE/5G NR coverage and capacity: link budget to MAPL, Okumura-Hata/COST-231/38.901 models tuned on drive data, site counts, sector capacity, PCI planning and drive-test acceptance."
sources: ["3GPP TR 38.901 Study on channel model for frequencies from 0.5 to 100 GHz", "3GPP TS 36.211 / TS 38.211 physical channels and modulation", "COST 231 Final Report, Digital Mobile Radio Towards Future Generation Systems", "Hata, Empirical formula for propagation loss in land mobile radio services (IEEE Trans. Veh. Tech., 1980)", "Holma and Toskala, LTE for UMTS", "Forsk Atoll and Infovista Planet user documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTE/5G coverage and capacity planning — enough sites, in the right places, carrying the load

**Goal:** produce a site plan and parameter set that meets agreed RSRP/SINR coverage targets and busy-hour throughput, then prove it with drive tests.

## 1. Set targets

Targets are operator-specific. Common starting points (all operator-specific and (gated: unconfirmed, source is paywalled or blocked)):

- **Coverage:** RSRP >= -105 dBm outdoor at 95% of area for good service, with -110 to -115 dBm as the usable cell edge. Plan indoor service by adding penetration loss, not by lowering the threshold.
- **Quality:** SINR >= 0 dB at cell edge and > 10 dB median. RSRQ > -15 dB (LTE).
- **Capacity:** cell-edge user rate (for example 5-10 Mbps DL) and busy-hour cell throughput with PRB utilisation below about 70%.

## 2. Link budget to maximum allowable path loss (MAPL)

MAPL = EIRP (per RE or per PRB) - receiver sensitivity + antenna gains - cable/body losses - shadow-fading margin - building/vehicle penetration - interference margin.

- Shadow-fading margin comes from log-normal sigma (6-10 dB) at the target edge probability. For 90% edge that is 1.28 sigma (normal quantile, computed 1.2816); the 90% edge to 95% area mapping depends on the path-loss exponent and sigma (gated: unconfirmed, source is paywalled or blocked).
- Typical penetration losses (check local measurements): car 6-10 dB; indoor 10-20 dB at sub-6 GHz (gated: unconfirmed, source is paywalled or blocked), rising sharply with low-E glass and at mmWave.
- Compute **both directions**; the uplink (UE ~23 dBm) usually limits LTE and NR mid-band edge coverage.

## 3. Propagation model and cell range

- **Okumura-Hata** (150-1500 MHz, base 30-200 m, 1-20 km; formula coefficients here and for COST-231 are (gated: unconfirmed, source is paywalled or blocked), original papers not fetched): L = 69.55 + 26.16 log f - 13.82 log hb - a(hm) + (44.9 - 6.55 log hb) log d.
- **COST-231 Hata** (1500-2000 MHz): L = 46.3 + 33.9 log f - 13.82 log hb - a(hm) + (44.9 - 6.55 log hb) log d + Cm, where Cm = 0 dB (medium city/suburban) or 3 dB (metropolitan). f is in MHz and d in km.
- **3GPP TR 38.901** UMa/UMi/RMa/InH (0.5-100 GHz) with LOS probability. Use it for NR mid-band and mmWave.
- Worked example: COST-231, 1800 MHz, hb 30 m, hm 1.5 m gives L = 136.2 + 35.2 log d (recomputed 136.20 + 35.22 log d using the small/medium-city a(hm) of 0.04 dB). With MAPL 130 dB, R is about 0.67 km (0.667). A three-sector site covers 1.95 R^2 ((gated: unconfirmed, source is paywalled or blocked)), about 0.87 km^2, so 100 km^2 needs about 115 sites (115.3) before capacity and terrain.
- In Atoll or Planet, use ray-tracing or tuned standard propagation models (SPM) with 5-20 m clutter/DTM. **Tune with CW measurements:** target mean error about 0 dB and standard deviation <= 8 dB per clutter class (gated: unconfirmed, source is paywalled or blocked).

## 4. Capacity per sector

- Sector throughput = bandwidth x average spectral efficiency x DL share (TDD). LTE 20 MHz 2x2 averages about 1.5-2 bit/s/Hz, roughly 30-40 Mbps per cell (20 MHz x 1.5-2 = 30-40 arithmetic ok; the efficiency (gated: unconfirmed, source is paywalled or blocked)). NR 100 MHz TDD with massive MIMO carries several hundred Mbps average; take the efficiency from vendor or field data.
- Required sectors = busy-hour demand (subscribers x busy-hour Mbps per subscriber) / (sector throughput x target utilisation). Add sites, carriers or sectors when this exceeds the coverage count. Backhaul hops are engineered in engineering-technology.telecommunications-engineering.rf-link-budget.point-to-point-link-budget, and aggregate demand in engineering-technology.telecommunications-engineering.network-architecture-design.capacity-dimensioning-and-resilience.

## 5. PCI and neighbour planning

- LTE has 504 PCIs (168 groups x 3) and NR has 1008 (336 x 3) (arithmetic checked; group counts per 3GPP TS 36.211 / 38.211, not fetched, (gated: unconfirmed, source is paywalled or blocked)).
- Plans must be **collision-free** (no neighbours sharing a PCI) and **confusion-free** (no cell with two neighbours sharing a PCI). Avoid equal PCI mod 3 on co-sited and facing sectors, and spread mod 30 for uplink reference-signal sequence groups ((gated: unconfirmed, source is paywalled or blocked)). Check vendor guidance for NR mod-4 PBCH DMRS rules.
- Reserve a PCI block for small cells and growth.

## 6. Validate with drive tests

Run TEMS or Nemo scanners with a calibrated roof-mounted antenna, binned at 20-50 m. Accept when the percentage of bins meeting RSRP and SINR targets meets the plan (for example 95%, operator-specific); investigate failing clusters (overshoot, missing neighbours, tilt errors).

## Gotchas

- Hata is invalid below 1 km, below 30 m antenna height or in street canyons; use 38.901 UMi or ray tracing there.
- Coverage without interference is fiction. High sites overshoot, so model with realistic load (50-100% (gated: unconfirmed, source is paywalled or blocked)) and verify SINR, not just RSRP.
- Scanner RSRP and UE-reported RSRP differ by antenna gain and body loss, often several dB.
- NR SSB beamforming means SS-RSRP depends on beam configuration; plan using the actual SSB beam set.

## Verify

- [ ] Link budget is computed for both UL and DL, and the limiting direction sets cell range.
- [ ] Propagation model is tuned to measurements (mean about 0 dB, sigma <= 8 dB).
- [ ] Predicted area meeting RSRP/SINR targets meets the plan at realistic network load.
- [ ] Sector capacity covers busy-hour demand at <= ~70% PRB utilisation.
- [ ] PCI plan passes collision, confusion and mod-3 checks.
- [ ] Drive-test bins meet acceptance, and failing clusters have a root cause.
