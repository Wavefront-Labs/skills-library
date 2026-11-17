---
id: social-sciences.management-and-organisational-research.accounting-finance-research.archival-earnings-management-and-accruals-studies
name: archival-earnings-management-and-accruals-studies
category: social-sciences
field: management-and-organisational-research
product: accounting-finance-research
tags: [accounting-finance-research, accounting-research, archival-research, earnings-management, discretionary-accruals, modified-jones-model, jones-model, kothari-performance-matched, dechow-dichev, accruals-quality, compustat, crsp, wrds, audit-analytics, disclosure-research, winsorizing, fixed-effects, clustered-standard-errors, petersen-2009, sas, stata, earnings-quality, financial-reporting]
level: advanced
status: draft
description: "Build an archival earnings-management study: Compustat sample, total accruals, modified-Jones and performance-matched discretionary accruals, winsorising, fixed effects and clustered errors."
sources:
  - "Dechow, Sloan & Sweeney (1995), Detecting earnings management, The Accounting Review"
  - "Kothari, Leone & Wasley (2005), Performance matched discretionary accrual measures, J. Accounting and Economics"
  - "Petersen (2009), Estimating standard errors in finance panel data sets, Review of Financial Studies"
  - "Dechow, Ge & Schrand (2010), Understanding earnings quality, JAE"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Archival earnings-management and accruals studies

**Goal:** test whether a set of firms (e.g. those about to issue equity, meet analyst
forecasts, or with weak boards) manage reported earnings, using the standard archival
toolkit of accounting research — and avoid the measurement traps that sink these papers.

## 1. Sample construction
- Data: Compustat Fundamentals Annual (via WRDS), merged to CRSP with the CCM link
  table; Audit Analytics for restatements and auditor data; I/B/E/S for analyst
  forecasts.
- Standard filters: exclude financial firms (SIC 6000–6999) and often utilities
  (4900–4999), require non-missing variables and enough firms per industry-year (e.g.
  ≥ 10 or ≥ 15 in a two-digit SIC group) to estimate accrual models.
- Keep a **sample-attrition table**: how many firm-years each filter removes.
- Use Compustat's standard data-format filters (INDFMT='INDL', DATAFMT='STD',
  POPSRC='D', CONSOL='C') to avoid duplicate records.

## 2. Measuring accruals
- **Total accruals** — prefer the cash-flow-statement approach (post-1988 US data):
  TA = income before extraordinary items (IB) − operating cash flow (OANCF −
  XIDOC). The balance-sheet approach introduces error around M&A and discontinued ops.
- **Modified Jones model**, estimated cross-sectionally per industry-year, all scaled
  by lagged total assets (A_{t−1}):
  TA/A_{t−1} = β0(1/A_{t−1}) + β1(ΔREV − ΔREC)/A_{t−1} + β2 PPE/A_{t−1} + ε
  (Strictly, Dechow et al. estimate on ΔREV and subtract ΔREC in the event period; many
  papers apply ΔREV−ΔREC in both — state which.) Residual = discretionary accruals (DA).
- **Performance matching** (Kothari et al.): add ROA to the model or subtract the DA of
  an industry-year firm with the closest ROA. Without it, high-growth or high-performing
  firms look like manipulators.
- Alternatives/robustness: Dechow–Dichev accruals quality (McNichols modification),
  real-earnings-management measures (Roychowdhury: abnormal CFO, production,
  discretionary expenses), restatements or AAERs as ex-post manipulation flags.

## 3. Testing
- Regress DA (signed for directional hypotheses; absolute DA for "quality") on the
  treatment variable plus controls: size (log assets/market cap), leverage, growth (MTB),
  ROA, loss indicator, CFO, plus year and industry fixed effects.
- **Winsorise** continuous variables at 1%/99% (by year is common) to tame outliers.
- **Cluster standard errors** by firm (and year, two-way, if cross-correlation is
  plausible) — Petersen (2009) shows OLS or Fama–MacBeth alone can badly understate errors.
- Address selection: propensity-score or entropy-balanced matched samples, difference-in-
  differences around a regulatory shock, or firm fixed effects. Reviewers now expect an
  identification argument, not just controls.

## Gotchas
- Accrual models are **noisy**: DA picks up growth, business-model change and M&A. A
  "significant" DA difference can be economic, not opportunistic. Triangulate.
- Scaling everything by lagged assets avoids heteroskedasticity but can make small firms
  dominate; consider deflator sensitivity.
- Using the full sample to estimate the model, then testing on a subsample, is standard —
  but excluding treatment firms from the estimation group is an option to discuss.
- Compustat variable definitions change; check the data guide for each mnemonic.
- Uncertain: exact current filter conventions vary across journals (TAR, JAR, JAE);
  copy a recent paper in your target outlet and cite it.

## Verify
- [ ] Attrition table reconciles from raw Compustat to final N.
- [ ] Total accruals computed from cash-flow-statement data; scaled by lagged assets.
- [ ] Industry-year estimation with a minimum firm count; model version stated.
- [ ] Performance-matched or ROA-controlled DA reported as a robustness test.
- [ ] Variables winsorised; SEs clustered by firm (and year if needed).
- [ ] An identification strategy beyond controls is argued.
