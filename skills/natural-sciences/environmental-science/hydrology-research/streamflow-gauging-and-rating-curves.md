---
id: natural-sciences.environmental-science.hydrology-research.streamflow-gauging-and-rating-curves
name: streamflow-gauging-and-rating-curves
category: natural-sciences
field: environmental-science
product: hydrology-research
tags: [hydrology-research, hydrology, streamflow, discharge, stream-gauging, velocity-area-method, current-meter, flowtracker, adv, adcp, salt-dilution, dilution-gauging, stage, stage-discharge, rating-curve, power-law, cease-to-flow, gauge-height, pressure-transducer, barometric-compensation, hysteresis, catchment-studies, hydrograph, usgs, iso-748]
level: practitioner
status: gated
description: "Measure stream discharge (velocity-area, ADCP, salt dilution) and build a stage-discharge rating curve: panel spacing, 0.6-depth rule, logger compensation, power-law fit and rating shifts."
sources: [USGS Techniques and Methods 3-A8 (Turnipseed & Sauer 2010, discharge measurements), ISO 748 velocity-area methods, Moore 2004/2005 salt dilution notes (Streamline Watershed Management Bulletin)]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streamflow gauging and rating curves

**Goal:** turn a continuous water-level record into a continuous discharge (Q, m³/s)
record for a catchment study, by gauging Q many times across the flow range and
fitting a stage–discharge relationship.

## 1. Site selection
A good gauging section is straight for several channel widths upstream, has a stable
bed, no backwater from a downstream confluence or weed growth, and a **control** (riffle
crest, rock bar, or a weir/flume) that makes stage respond uniquely to flow. Install a
staff gauge and a stage logger (vented or non-vented pressure transducer in a
stilling well); survey both to a benchmark.

## 2. Measuring discharge
**Velocity-area (wading):**
- Stretch a tape across; divide into **≥20 verticals** (commonly cited; confirm the count in USGS TM 3-A8 or ISO 748 (gated: unconfirmed, source is paywalled or blocked)
  so no panel carries more than ~5–10% of total Q.
- At each vertical measure depth and velocity with a current meter or acoustic
  velocimeter (e.g. ADV units): at **0.6 × depth from the surface** when depth < ~0.75 m (gated: unconfirmed, source is paywalled or blocked);
  average of **0.2 and 0.8** for deeper water. Average ≥40 s per point.
- Q = Σ (width × depth × mean velocity) per panel (mid-section method).
- Stand downstream and to the side of the meter; your legs alter the flow.
**ADCP:** for deep or fast rivers, boat-mounted acoustic Doppler profilers; make an even number (≥2) of reciprocal transects with total exposure time ≥720 s (USGS memo, Oct 2011) and check moving-bed conditions.
**Salt dilution (slug):** for turbulent, rocky mountain streams where meters fail. Dump
a known salt mass upstream, log conductivity downstream after full mixing; Q = M / (k ×
∫(EC − EC_background) dt), with k calibrated in a bucket of stream water. Day (1976) found about 0.3 kg NaCl per m³/s adequate in steep gravel streams; scale by background EC, logger range and mixing length (Hudson & Fraser 2005: Q = M / A, A = area under the concentration-time curve in mg·s/L).

Grade each measurement (e.g. good ±5%, fair ±8%, poor >8%) and note conditions.

## 3. Logger processing
- **Non-vented transducers** record total pressure; subtract a co-located barometric
  logger. Same time stamps, same units, check for drift against staff readings at
  every visit.
- Remove dry periods, ice effects and spikes during downloads.

## 4. Fit the rating
Standard form: **Q = C (h − h₀)^β**, where h₀ is the stage of zero flow (cease-to-flow
level, ideally surveyed at the control's lowest point). Fit by non-linear least
squares or log-log regression with h₀ fixed. Typical β ~1.5–2.5 for natural sections (check against your control type); a synthetic test (C=3, h₀=0.1, β=2, 3 % noise) was recovered by `curve_fit` as C=3.03, β=2.00.
- Use separate segments if the control changes (e.g. low-flow riffle vs out-of-bank flow).
- Plot residuals by date: a systematic drift means a **rating shift** (scour, fill,
  vegetation) — apply time-varying shifts rather than forcing one curve.
- High flows are rarely gauged; extrapolating >1.5–2 × the highest measurement adds
  large uncertainty. Use a hydraulic model (slope-area, HEC-RAS) for floods and say so.

## 5. Uncertainty
Report Q uncertainty from both measurement error and rating fit (Bayesian tools like
BaRatin produce rating uncertainty bands). Don't present a 5-minute Q series to three
significant figures if the rating is ±20% at peak flows.

## Gotchas
- Hysteresis: on rising limbs Q can exceed the steady rating; matters in flashy catchments.
- Weed growth through summer causes slow positive shifts.
- Staff gauge readings at every visit are the only check on transducer drift.
- Salt dilution fails if mixing is incomplete — check with two probes across the channel.

## Verify
- [ ] Gauged ≥10–15 times spanning low to high flow, each graded.
- [ ] Stage record compensated and checked against staff readings.
- [ ] h₀ surveyed; rating residuals show no unexplained time trend.
- [ ] Extrapolated ranges flagged; uncertainty reported with Q.
