---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.modulation-and-coding-selection
name: modulation-and-coding-selection
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [modulation-coding, bpsk, qpsk, forward-error-correction, ccsds-coding, eb-n0, spacecraft-communications]
level: practitioner
status: draft
description: "Select modulation and forward error correction for a space link, relate required Eb/N0 to bit error rate, and estimate bandwidth and data rate."
sources:
  - "CCSDS 131.0-B (TM synchronization and channel coding)"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Sklar, Digital Communications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Modulation and coding

**Goal:** a waveform that meets the data rate within bandwidth and power limits.

## Modulation
- BPSK and QPSK need about 9.6 dB `Eb/N0` for a bit error rate of 1e-5 uncoded (QPSK has the same `Eb/N0` as BPSK at twice the spectral efficiency).
- Occupied bandwidth about `R_s (1 + alpha)` with `alpha` the filter roll-off; `R_s = R_b / (bits per symbol * code rate)`.
- Constant-envelope schemes (GMSK, OQPSK) suit nonlinear power amplifiers.

## Coding
- Convolutional (rate 1/2, constraint length 7) with Reed-Solomon (255,223) outer code is the classic CCSDS concatenated scheme; turbo codes and LDPC codes give coding gain of several decibels more, and CCSDS and commercial standards define them (CCSDS 131.0-B for telemetry; DVB-S2 for broadcast-style links with adaptive coding and modulation).
- Coding gain lowers the needed `Eb/N0` at a bit error rate target, at the cost of bandwidth and decoder complexity.

## Procedure
1. State the data rate, bit error rate or frame error rate target, available bandwidth, and power.
2. Choose modulation to fit the bandwidth; add coding to lower power need.
3. Look up required `Eb/N0` for the pair from the standard's performance curves; add implementation loss (a dB or so) for real receivers.
4. Feed to the link budget as the required `Eb/N0` (see link-budget-and-margin).
5. Check ground station and regulator compatibility (spectral masks, ITU filings).

## Gotchas
- `Eb/N0` and `C/N0` are different: `Eb/N0 = C/N0 - 10 log10(R_b)`.
- Frame error rate is what matters for packet links, not only bit error rate.

## Verify
- [ ] The link budget closes with at least the required margin at the chosen code rate and data rate.
