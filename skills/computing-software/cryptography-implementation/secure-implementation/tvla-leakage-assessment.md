---
id: computing-software.cryptography-implementation.secure-implementation.tvla-leakage-assessment
name: tvla-leakage-assessment
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, tvla, leakage-assessment, side-channel, power-analysis, welch-t-test, iso-17825]
level: sme
status: draft
description: "Run Test Vector Leakage Assessment (TVLA) on crypto implementations: fixed-versus-random Welch t-tests on power or EM traces, the 4.5 threshold, and acting on failures."
sources: ["https://csrc.nist.gov/csrc/media/events/non-invasive-attack-testing-workshop/documents/08_goodwill.pdf", "https://www.iso.org/standard/60612.html", "https://chipwhisperer.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TVLA leakage assessment

TVLA (Goodwill et al., 2011) is a conformance-style test: it detects whether power or EM measurements depend on
secret data, without mounting a full attack. ISO/IEC 17825 standardises a version.

## Method (non-specific fixed vs random)
1. Collect two trace sets on the same device and key: set A with a fixed input, set B with random inputs,
   interleaved randomly to avoid drift bias.
2. At each time sample, compute Welch's t-statistic between sets.
3. If |t| > 4.5 at any point (in two independent runs, at the same points), the implementation leaks
   (roughly 99.999% confidence per point).
4. Higher-order tests (centered, squared traces) for masked implementations.

## Setup
- ChipWhisperer (Husky, Lite) for microcontrollers; oscilloscope and EM probe for SoCs.
- Tens of thousands to millions of traces depending on noise; align traces before analysis.
- Specific tests (e.g. targeting an S-box output bit) help localise leakage.

## Interpreting
- Failure means "leakage exists", not "exploitable"; follow up with CPA/template attacks or fix.
- Pass is evidence for that trace count and setup only.
- Common fixes: masking, shuffling, constant-time code (removes timing but not power leakage), hardware
  countermeasures.

## Verify
- [ ] Report includes trace counts, sampling rate, t-plots for both runs, and the evaluated firmware build hash.
