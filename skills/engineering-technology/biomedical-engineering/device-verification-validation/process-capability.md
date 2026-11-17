---
id: engineering-technology.biomedical-engineering.device-verification-validation.process-capability
name: process-capability
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [process-capability, sample-size, statistical-sampling, cpk, ppk, spc, process-performance, non-normal-data]
level: practitioner
status: gated
description: "Calculate and interpret process capability indices Cp Cpk Pp Ppk for device characteristics: data requirements, normality, non-normal methods, targets and confidence intervals."
sources: ["Montgomery, Introduction to Statistical Quality Control (process capability chapter)", "AIAG Statistical Process Control (SPC) Reference Manual", "ISO 22514 series Statistical methods in process management - Capability and performance (parts and editions: confirm at iso.org)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Process capability indices

**Goal:** quantify how well a process fits its specification limits, to support validation (PQ) and ongoing control.

## Definitions
- **Cp** = (USL - LSL) / (6 sigma), potential capability ignoring centring.
- **Cpk** = min[(USL - mean) / (3 sigma), (mean - LSL) / (3 sigma)], capability including centring; sigma estimated from within-subgroup variation.
- **Pp and Ppk** use the overall (long-term) standard deviation, showing performance including drift between subgroups.
- A Cpk of 1.0 puts the nearer spec limit 3 sigma from the mean (about 0.27% total outside for a centred normal process; 2*sf(3) = 0.0027 computed); 1.33 is 4 sigma; 1.67 is 5 sigma.

## Typical targets (industry practice, to be set by risk)
Cpk at least 1.33 (gated: unconfirmed, source is paywalled or blocked, industry practice) for general characteristics and at least 1.67 for critical-to-safety features; some use 2.0 for key dimensions on high-volume lines. The target and rationale belong in the validation plan.

## Procedure
1. Ensure the **measurement system** is capable (see gauge-rr); measurement noise inflates sigma.
2. Collect data from a stable process: at least 30 individual values (50 or more preferred) taken over multiple lots, operators and times; use rational subgroups.
3. Check **stability** with control charts (individuals or X-bar and R); capability on an unstable process is meaningless.
4. Check **normality** (probability plot, Anderson-Darling test). For non-normal data (flatness, runout, leak rates), use transformation (Box-Cox, Johnson), fit a better distribution, or the percentile method (using the 0.135 and 99.865 percentiles, the normal +/-3 sigma points; computed 0.135%).
5. Compute Cp, Cpk (and Pp, Ppk) with confidence intervals; small samples give wide intervals, so report the lower confidence bound.
6. If one-sided specs, use the single relevant index.

## Gotchas
- Cherry-picked or pre-sorted data.
- Using data from a single machine run to claim capability across tools and cavities.
- Ignoring that a Cpk figure is sensitive to the estimated sigma and to outliers.

## Verify
- [ ] Control chart shows stability before capability is calculated.
- [ ] Lower 95% confidence bound for Cpk meets the target.
- [ ] Measurement system study referenced.
