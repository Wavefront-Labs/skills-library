---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.fixed-point-scaling-and-conversion
name: fixed-point-scaling-and-conversion
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [fixed-point, fixdt, scaling, fixed-point-tool, overflow, quantisation, fixed-point-designer]
level: practitioner
status: gated
description: "Convert a floating-point controller to fixed point: choose word length and scaling from simulated ranges, handle overflow and quantisation, and verify."
sources:
  - "Fixed-Point Designer: fixdt (https://www.mathworks.com/help/simulink/slref/fixdt.html)"
  - "Fixed-Point Designer: Overflow handling and rounding methods (https://www.mathworks.com/help/fixedpoint/ug/overflow-handling-and-rounding-methods.html)"
  - "Oppenheim and Schafer, Discrete-Time Signal Processing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Fixed-point scaling and conversion

1. Log ranges: run representative and extreme scenarios with signal-logging and min/max instrumentation.
2. Choose type per signal: `fixdt(signed, wordlength, fractionlength)`; set LSB to the sensor/physical resolution, and range to the logged min/max plus margin.
3. Use the Fixed-Point Tool or the Data Type Assistant for proposals, then review by hand; prefer powers-of-two scaling for cheap shifts.
4. Overflow: use saturation on safety-relevant paths (saturation is the default for `fi` objects), wrap only where proven safe; set diagnostics for overflow to error.
5. Rounding mode: floor is cheapest, rounds toward negative infinity and is biased; nearest breaks exact ties toward positive infinity; use nearest or convergent where bias matters (integrators). Relative cost ranking of the modes: confirm in the rounding-mode tables (gated: unconfirmed, source is paywalled or blocked).
6. Integrator and filter states need extra fraction bits; check limit cycles in digital filters.
7. Compare against the floating-point baseline on the same test vectors.

**Gotchas:** division and gain chains lose precision; reorder operations.

## Verify
- [ ] No overflow in any run; maximum deviation vs float within the stated tolerance.
- [ ] Number of bits and scaling documented per interface signal.
