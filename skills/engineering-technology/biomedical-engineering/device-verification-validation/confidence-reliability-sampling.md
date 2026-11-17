---
id: engineering-technology.biomedical-engineering.device-verification-validation.confidence-reliability-sampling
name: confidence-reliability-sampling
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [confidence-reliability, sample-size, statistical-sampling, success-run-theorem, binomial, attribute-sampling, risk-based-sampling]
level: practitioner
status: verified
description: "Choose sample sizes for pass/fail verification tests using confidence and reliability: success-run formula, common 95/95 tables, risk-based levels and failure-allowed plans."
sources: ["ISO 2859-1:2026 Sampling procedures for inspection by attributes, Part 1: AQL-indexed lot-by-lot schemes (https://www.iso.org/standard/2859-1)", "ISO 16269-6:2014 Statistical interpretation of data, Part 6: statistical tolerance intervals (https://www.iso.org/standard/57191.html)", "Montgomery, Introduction to Statistical Quality Control"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Confidence and reliability sampling (attribute data)

**Goal:** a defensible sample size for pass/fail verification that supports a stated claim such as "at least 95% of units conform, with 95% confidence".

## Zero-failure (success-run) formula
n = ln(1 - C) / ln(R), where C is confidence and R is reliability (proportion conforming). Round up.

| Confidence / reliability | Sample size (0 failures) |
|---|---|
| 90% / 90% | 22 |
| 95% / 90% | 29 |
| 95% / 95% | 59 |
| 95% / 99% | 299 |
| 99% / 99% | 459 |

## Plans that allow failures
Use the binomial distribution: find the smallest n such that the probability of observing at most c failures, when the true reliability equals the claimed minimum R, is at most 1 - C. For 95/95 with up to 1 failure, n is 93; with 2 failures, 124 (computed with the binomial cdf in scipy; verify with software before use). Allowing failures increases sample size, so a design with margin that passes with zero failures is more efficient.

## Choosing confidence and reliability by risk
A common industry approach (not a regulation) ties levels to the severity of harm from failure of the characteristic: higher severity gets higher reliability and confidence (for example 95/99 for critical, 95/95 for major, 95/90 for minor characteristics; an illustration, not a standard). The rationale must be written in the plan and consistent with the risk file.

## When to use variable data instead
If the characteristic is measured (force, dimension, leak rate), **tolerance intervals** with normal or other distribution assumptions allow smaller sample sizes for the same claim (see tolerance-intervals), provided the distribution is verified.

## Practical points
- Samples must represent production (multiple lots, tools, operators) or the claim applies only to the tested lot.
- Define the failure criterion and accept/reject before testing.
- Retests are not allowed to hide failures; a failed run needs investigation.

## Verify
- [ ] Sample size formula and inputs recorded in the protocol.
- [ ] Rationale for chosen confidence and reliability in the plan.
- [ ] Results table shows the achieved confidence and reliability.
