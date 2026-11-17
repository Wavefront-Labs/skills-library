---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.flood-frequency-analysis
name: flood-frequency-analysis
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [flood-frequency, log-pearson-iii, bulletin-17c, annual-maximum-series, return-period, aep, gev, gauge-record, regional-skew, confidence-limits]
level: advanced
status: draft
description: "Estimate design floods from gauge records: annual maximum series, Log-Pearson III per Bulletin 17C or GEV, plotting positions, skew, regionalisation and uncertainty."
sources: ["USGS Bulletin 17C Guidelines for Determining Flood Flow Frequency (SIR 2018-5118)", "Australian Rainfall and Runoff, Book 3 Flood Frequency Analysis", "Chow, Maidment and Mays, Applied Hydrology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Flood frequency analysis

Goal: peak flow quantile for a given annual exceedance probability (AEP) with confidence limits, from a stream-gauge record.

## Steps
1. Build an annual maximum series; at least 10 years, ideally 30+. Extrapolating beyond about twice the record length is poor. Check for regulation, urbanisation, rating changes, missing peaks and historic floods.
2. Test for trend, outliers and mixed populations (separate snowmelt from rain).
3. Fit. US federal practice: Log-Pearson Type III with the Expected Moments Algorithm (Bulletin 17C), which handles censored data and low outliers (multiple Grubbs-Beck test) and weights station with regional skew. Australia's ARR 2019 recommends GEV with L-moments or Bayesian fitting (confirm the current edition).
4. Return period T = 1/AEP. Probability of at least one exceedance in n years = 1 - (1 - 1/T)^n (about 63% over T years).
5. Report quantiles with confidence limits; plot data (Weibull p = m/(n+1)) against the fitted curve.

## Gotchas
- Station skew from short records is unstable; regional skew matters.
- Climate-change adjustments are a jurisdiction policy matter: state them explicitly.

## Verify
Curve passes through the data; compare against regional regression equations (USGS StreamStats in the US) and a rainfall-runoff estimate.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
