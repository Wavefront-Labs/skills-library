---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.link-budget-and-margin
name: link-budget-and-margin
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, spacecraft-communications, link-budget, spacecraft-comms, link-margin, eirp, free-space-path-loss, eb-n0]
level: practitioner
status: verified
description: "Compute a spacecraft RF link budget (EIRP, path loss, G/T, Eb/N0) and required margin, with a worked X-band example and units pitfalls."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Pratt, Bostian and Allnutt, Satellite Communications"
  - "CCSDS and ECSS telecommunications standards"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Link budget and margin

**Goal:** show the link closes with margin.

## Equations (dB form)
- `EIRP = P_tx + G_tx - L_tx`
- Free-space path loss: `L_fs = 20 log10(4 pi d/lambda)`
- Received `C/N0 = EIRP - L_fs - L_other + (G/T) - k` with `k = -228.6 dBW/K/Hz`
- `Eb/N0 = C/N0 - 10 log10(R_b)`; margin `M = Eb/N0 - (Eb/N0)_required`.
- `L_other`: atmospheric, rain, pointing, polarisation, implementation losses.

## Example
X-band downlink at 8.2 GHz (`lambda` = 0.0366 m), range 1,500 km: `L_fs` = 174.2 dB (computed). A 10 W (10 dBW) transmitter with 8 dBi antenna gain and ground station `G/T` of 30 dB/K, other losses 3 dB, at 100 Mbit/s (80 dB-Hz): `C/N0 = 18 - 174 - 3 + 30 + 228.6 = 99.6 dB-Hz`; `Eb/N0 = 19.6 dB`. Compare with the modem requirement for the modulation and coding chosen (uncoded BPSK/QPSK needs about 9.6 dB for BER 1e-5, computed as 9.7e-6 from `0.5 erfc(sqrt(Eb/N0))`; coded schemes need less).

## Practice
1. Compute worst-case range (minimum elevation) and weather.
2. Include implementation losses (typically 1-2 dB (gated: unconfirmed, source is paywalled or blocked)) and a project-specified margin (3 dB is a common minimum for planned operations (gated: unconfirmed, source is paywalled or blocked)).
3. Re-run for uplink with ground EIRP and spacecraft `G/T`.

## Gotchas
- Mixed dBW and dBm; bandwidth vs bit-rate confusion.
- Frequency allocation and licensing (ITU filings) are separate programme requirements.

## Verify
- [ ] The example gives an `Eb/N0` close to 19.6 dB and a positive margin vs the stated requirement.
