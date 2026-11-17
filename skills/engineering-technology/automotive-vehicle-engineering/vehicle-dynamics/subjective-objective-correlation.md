---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.subjective-objective-correlation
name: subjective-objective-correlation
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [subjective-objective-correlation, subjective-rating, objective-metrics, ratings, regression, handling-evaluation]
level: practitioner
status: draft
description: "Correlate driver subjective ratings with objective test metrics: rating scales, blind repeated drives, regression and target-setting."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "industry vehicle-dynamics evaluation practice"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Subjective to objective correlation

1. Choose a rating scale used company-wide (e.g. 1-10 with defined anchors) and a set of attributes (on-centre feel, response, roll control, ride comfort).
2. Test design: several trained evaluators, several vehicles (benchmarks plus variants), randomised blind order, repeated runs and the same routes/events.
3. Measure objective metrics on the same days (gradient, yaw gain, phase lag, hysteresis, ISO 2631 RMS).
4. Statistics: check evaluator agreement (spread, ANOVA-style analysis); average scores per vehicle; regress rating against each metric; accept relationships with sensible physics and adequate sample size (many more vehicles than predictors).
5. Use the result to set metric targets that deliver the desired rating, with tolerance bands.
6. Revisit when tyres or conditions change; correlations are tyre and market dependent.

**Gotchas:** overfitting with few vehicles; evaluator bias for brand.

## Verify
- [ ] Inter-evaluator agreement reported.
- [ ] Each target metric has a stated source correlation and range of validity.
