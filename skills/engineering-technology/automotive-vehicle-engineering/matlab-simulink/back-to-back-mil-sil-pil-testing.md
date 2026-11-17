---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.back-to-back-mil-sil-pil-testing
name: back-to-back-mil-sil-pil-testing
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [back-to-back-testing, mil, sil, pil, equivalence-testing, simulink-test, embedded-coder]
level: practitioner
status: gated
description: "Run the same test vectors through model, generated code on host and processor-in-the-loop, and compare outputs with defined tolerances."
sources:
  - "Simulink Test: back-to-back equivalence testing (https://www.mathworks.com/help/sltest/ug/back-to-back-equivalence-testing.html)"
  - "ISO 26262 part 6 back-to-back guidance; confirm edition (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# MIL, SIL, PIL back-to-back equivalence

1. Define test vectors from requirements (and coverage gaps). Store as test cases with input timelines.
2. MIL: simulate the model; record outputs as baseline.
3. SIL: run generated code compiled for host (equivalence test in the Simulink Test Test Manager with Simulation 1 in Normal mode and Simulation 2 in Software-in-the-Loop mode). PIL: run on the target core or evaluation board (a separate target setup).
4. Compare with tolerances: bit-exact for fixed-point/integer logic, absolute+relative tolerance for floating point (state the numbers; float differences from compiler and math library are expected). Which back-to-back method ISO 26262-6 asks for at each ASIL: confirm in the current edition (gated: unconfirmed, source is paywalled or blocked).
5. Investigate every mismatch: scaling, data types, uninitialised state, compiler optimisation level, target word size.
6. Archive results, tool versions and compiler flags.

**Gotchas:** solver differences when plant is included; run the controller alone with recorded inputs.

## Verify
- [ ] All test cases pass within the stated tolerances.
- [ ] Compiler, flags and model version recorded with the results.
