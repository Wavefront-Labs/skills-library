---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.cgm-accuracy
name: cgm-accuracy
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [cgm-accuracy, mard, clarke-error-grid, continuous-glucose-monitor, icgm]
level: advanced
status: gated
description: "Evaluate continuous glucose monitor accuracy: MARD, error grids, 15/15 and 20/20 agreement, lag, study design, calibration effects and regulatory expectations."
sources: ["Clarke et al., Evaluating clinical accuracy of systems for self-monitoring of blood glucose (Diabetes Care, 1987)", "Parkes et al., A new consensus error grid (Diabetes Care, 2000)", "21 CFR 862.1355 Integrated continuous glucose monitoring system (https://www.ecfr.gov/current/title-21/section-862.1355)", "https://www.fda.gov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CGM accuracy metrics

**Goal:** present CGM accuracy using standard metrics and a study design that reflects real use.

## Metrics
- **MARD (mean absolute relative difference)** between sensor and reference glucose, averaged over pairs. A single number hides patterns, so show distribution by glucose range and sensor age.
- **Agreement rates:** percent of readings within 15 mg/dL or 15 percent (15/15), 20/20, and similar for low and high ranges.
- **Error grids** (Clarke, Parkes/consensus) classify pairs by clinical risk zone; the proportion in zones A and B is commonly reported.
- **Bias, lag and rate-of-change accuracy:** interstitial glucose lags blood glucose by several minutes, which increases error during rapid change (lag of several minutes (gated: unconfirmed, source is paywalled or blocked)); report rate-of-change accuracy and alerts performance (hypoglycaemia detection).
- **Precision:** repeatability between two sensors worn simultaneously.

## Study design
1. Reference: laboratory analyser (for example a yellow springs-type glucose analyser) rather than fingerstick, with frequent sampling and induced glycaemic excursions in clinic sessions.
2. Diverse subjects, sensor sites, wear duration to end of life, and calibration scheme (factory or user calibrated).
3. Interference substances tested (for example acetaminophen and ascorbic acid depending on the sensor chemistry).
4. Regulatory: in the US, 21 CFR 862.1355 (Integrated continuous glucose monitoring system, as fetched from eCFR) sets special controls: clinical accuracy data in the intended population, data transmission, manufacturing and release controls, interfering substances, sensor wear period, usability and labelling of performance data per population and insertion site. It also sets numeric adult accuracy criteria (for example a lower one-sided 95% confidence bound for the share of readings within 15 mg/dL below 70 mg/dL); read the current text for the values. Confirm equivalent expectations elsewhere.

## Verify
- [ ] Metrics reported across ranges and over sensor life.
- [ ] Reference method and sampling plan documented.
- [ ] Interferents and failure modes assessed.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
