---
id: engineering-technology.telecommunications-engineering.rf-link-budget.point-to-point-link-budget
name: point-to-point-link-budget
category: engineering-technology
field: telecommunications-engineering
product: rf-link-budget
tags: [telecommunications-engineering, rf-link-budget, link-budget, microwave-link, point-to-point, eirp, fspl, free-space-path-loss, antenna-gain, receiver-sensitivity, noise-figure, thermal-noise, ktb, fade-margin, fresnel-zone, k-factor, earth-bulge, itu-r-p530, itu-r-p838, itu-r-p837, rain-attenuation, multipath-fading, availability, acm, gaseous-absorption, backhaul]
level: practitioner
status: gated
description: "Build a point-to-point microwave link budget: EIRP, FSPL, sensitivity from kTB + NF + SNR, fade margin, 60% Fresnel clearance with k-factor, and ITU-R P.530/P.838 rain availability."
sources: ["ITU-R P.530 Propagation data and prediction methods for terrestrial line-of-sight systems", "ITU-R P.838 Specific attenuation model for rain", "ITU-R P.837 Characteristics of precipitation for propagation modelling", "ITU-R P.676 Attenuation by atmospheric gases", "ITU-R P.453 Radio refractive index", "Freeman, Radio System Design for Telecommunications", "Lehpamer, Microwave Transmission Networks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-to-point link budget — prove the link closes with margin

**Goal:** show that a line-of-sight radio link delivers enough received power above the receiver threshold, at the required modulation, for the target availability.

## 1. The budget equation (all in dB)

`Prx = Ptx - Ltx + Gtx - FSPL - Lgas - Lmisc + Grx - Lrx`

- **FSPL** = 20 log10(d_km) + 20 log10(f_MHz) + 32.44 (use +92.45 with f in GHz).
- **Antenna gain** (parabolic): G = 10 log10(eta (pi D / lambda)^2), with eta about 0.55-0.6. A 0.6 m dish at 23 GHz is about 40.6-41.0 dBi at eta 0.55-0.6 (computed; 40.5 is used in the example below); 3 dB beamwidth is roughly 70 lambda / D degrees (1.5 degrees here; the 70 factor (gated: unconfirmed, source is paywalled or blocked)).
- **Ltx/Lrx:** waveguide or coax, branching/circulators, radome and connectors. Typically 0.5-1.5 dB per end for ODU-on-antenna (gated: unconfirmed, source is paywalled or blocked), plus per-metre loss for long waveguide.
- **EIRP** = Ptx - Ltx + Gtx; check it against the licence or regulatory cap.
- **Gas absorption** (ITU-R P.676): small below 15 GHz, about 0.15-0.2 dB/km near the 22 GHz water-vapour line, and around 15 dB/km at 60 GHz (oxygen) (gated: unconfirmed, source is paywalled or blocked).

## 2. Receiver threshold

Noise floor N = -174 dBm/Hz + 10 log10(B_Hz) + NF. Threshold = N + required SNR for the modulation at the target BER. Example: a 56 MHz channel (+77.5 dB) with NF 6 dB gives N = -90.5 dBm. At ~28 dB SNR for 256QAM ((gated: unconfirmed, source is paywalled or blocked)), the threshold is about -62 dBm (computed: -90.5 + 28 = -62.5). **Always prefer the vendor's measured threshold at BER 1e-6 for each modulation**, because it includes implementation loss.

## 3. Worked example

23 GHz, 10 km, Ptx +18 dBm, 0.6 m dishes (40.5 dBi each), 1 dB loss per end, gas 2 dB:
FSPL = 20 + 87.2 + 32.44 = 139.7 dB (recomputed 139.67; the GHz form with 92.45 gives 139.68), so Prx = 18 - 1 + 40.5 - 139.7 - 2 + 40.5 - 1 = **-44.7 dBm**. Against -62 dBm, the fade margin is about 17 dB at 256QAM and 30 dB or more at QPSK. Hence **adaptive coding and modulation (ACM)**: a high-availability base modulation with a lower-availability top rate.

## 4. Path clearance

- First Fresnel radius: r1 (m) = 17.32 sqrt(d1 d2 / (f_GHz d)), with distances in km. At mid-path of 10 km at 23 GHz, r1 is about 5.7 m (recomputed 5.71).
- Earth bulge: h (m) = d1 d2 / (12.74 k), with distances in km. Use median k = 4/3 for normal clearance and also check a low k (around 2/3, or the climate's k_e at 99.9% from ITU-R P.530/P.453).
- A common criterion is **at least 60% of F1 clear at k = 4/3 plus a smaller clearance (for example 30% F1) at k_min** ((gated: unconfirmed, source is paywalled or blocked)). Add tree growth (allow 3-5 m, (gated: unconfirmed, source is paywalled or blocked)) and buildings. Some administrations set their own criteria.
- Long hops over water or flat ground need a reflection-point check; use space diversity if the reflection cannot be blocked.

## 5. Availability: rain and multipath

- **Rain (dominant above ~10 GHz):** specific attenuation gamma_R = k R^alpha dB/km with k and alpha from ITU-R P.838 (frequency- and polarisation-dependent; horizontal polarisation suffers more). Take R0.01 (mm/h exceeded 0.01% of the year) from ITU-R P.837 maps. Effective path length = d x distance factor from P.530, so A0.01 = gamma_R x d_eff. Scale to other percentages with the P.530 formula. Vertical polarisation and shorter hops are the cheapest fixes.
- **Multipath (dominant below ~10 GHz on long hops):** P.530 flat-fade method using the geoclimatic factor K, path inclination and frequency. Outage falls roughly 10x for every 10 dB of extra fade margin (the ITU-R P.530 flat-fade rule; (gated: unconfirmed, source is paywalled or blocked)). Diversity (space or frequency) helps here and does nothing for rain.
- Availability targets are typically 99.99-99.999% per hop for backhaul (gated: unconfirmed, source is paywalled or blocked).

## Gotchas

- Units: dBm and dBW differ by 30, and the 32.44 constant assumes km and MHz.
- Rain models that ignore polarisation or use one regional R0.01 can be 10+ dB wrong at 38 GHz and above.
- In dense bands interference, not noise, sets the threshold. Apply threshold degradation from the coordination study (for example 1 dB for I/N = -6 dB, (gated: unconfirmed, source is paywalled or blocked)).
- Datasheet sensitivity is typical; use the guaranteed value or derate 1-2 dB.
- Misalignment and wet radomes cost real decibels, so keep 1-3 dB of engineering margin.

Cellular sites that use these hops are planned in engineering-technology.telecommunications-engineering.radio-network-planning.lte-5g-coverage-and-capacity-planning.

## Verify

- [ ] FSPL, gains and losses recompute independently to within 0.5 dB of the planning tool.
- [ ] The receiver threshold is the vendor's guaranteed figure for each ACM step and channel width.
- [ ] The profile shows 60% F1 clear at k = 4/3 and the stated criterion at k_min, including vegetation allowance.
- [ ] Rain outage uses P.837 R0.01 and P.838 k/alpha for the actual polarisation.
- [ ] Commissioning RSL is within about +/-2 dB of prediction.
