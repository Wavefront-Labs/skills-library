---
id: social-sciences.management-and-organisational-research.strategy-management-research.event-studies-of-strategic-announcements
name: event-studies-of-strategic-announcements
category: social-sciences
field: management-and-organisational-research
product: strategy-management-research
tags: [strategy-management-research, strategic-management, event-study, abnormal-returns, car, cumulative-abnormal-return, market-model, estimation-window, event-window, crsp, compustat, wrds, eventus, sdc-platinum, acquisitions, m-and-a, alliance-announcements, ceo-succession, confounding-events, patell-test, boehmer-test, firm-panel-data, stock-market-reaction, finance-methods]
level: practitioner
status: draft
description: "Run a short-window stock-market event study of strategic announcements (acquisitions, alliances, CEO changes): windows, market model, CARs, confound screening and test statistics."
sources:
  - "MacKinlay (1997), Event studies in economics and finance, J. Economic Literature"
  - "McWilliams & Siegel (1997), Event studies in management research, Academy of Management Journal"
  - "Boehmer, Musumeci & Poulsen (1991), J. Financial Economics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event studies of strategic announcements

**Goal:** estimate how investors valued a strategic decision (acquisition, alliance,
divestiture, CEO succession, product recall) by measuring abnormal stock returns in a
short window around its first public announcement — and do it in a way reviewers in
strategy journals will accept.

## 1. Sample and event dates
- Draw events from a documented source: SDC Platinum (M&A, alliances), BoardEx or
  ExecuComp (executive changes), Factiva/LexisNexis searches for others.
- The **event date is the first public disclosure**, not the completion date. Check
  newswires: a rumour or leak earlier shifts day 0. If the announcement came after
  market close, day 0 is the next trading day.
- Price data: CRSP daily returns (US) via WRDS; Datastream/Refinitiv for non-US. Map
  identifiers carefully (CUSIP/PERMNO/ticker change over time).

## 2. Windows and the benchmark model
- **Estimation window**: e.g. trading days −250 to −30 (some use −255 to −46). It must
  end well before the event so leakage does not contaminate the baseline. Require a
  minimum number of valid returns (e.g. ≥ 100).
- **Event window**: short — (−1, +1) or (0, +1) is standard; report a couple of
  alternatives such as (−2, +2) and (−5, +5). Long windows invite confounds and the
  efficient-market assumption weakens.
- **Market model**: R_it = α_i + β_i R_mt + ε_it, estimated by OLS over the estimation
  window with a broad index (CRSP value-weighted). Abnormal return AR_it = R_it −
  (α̂_i + β̂_i R_mt); CAR = sum of ARs over the event window. Fama-French / Carhart
  factor benchmarks are a common robustness check.

## 3. Confound screening (where management studies get rejected)
McWilliams & Siegel's core warning: other firm news in the window (earnings releases,
dividend changes, lawsuits, other deals) can drive the return. Search news for every
event across the event window and drop or flag contaminated events; report how many.
Also watch **event clustering**: many firms with the same date (e.g. a regulatory
change) have cross-correlated returns, inflating t-statistics — use portfolio-level
tests or calendar-time methods.

## 4. Testing
- Cross-sectional t-test of mean CAR, plus at least one robust test: **Patell**
  (standardised ARs), **BMP / Boehmer et al.** (robust to event-induced variance
  increase), and a non-parametric test (generalised sign or Corrado rank).
- Tools: Eventus on WRDS, the WRDS event-study web tool, Stata `estudy`, or R
  (`estudy2`, or hand-rolled with `data.table`). Hand-rolling is fine — just verify on
  a few events against Eventus or a spreadsheet.
- **Second stage**: regress CAR on firm/deal characteristics (relatedness, payment
  method, governance) with appropriate controls; this is usually the theoretical
  contribution. Cluster standard errors by date or industry where events co-occur.

## Gotchas
- Thinly traded stocks have many zero returns, biasing β down; consider excluding or
  using trade-to-trade returns.
- Private targets and acquirers listed abroad need different data and exchange-hour logic.
- Survivorship: firms delisted later are still in CRSP — keep them.
- A significant CAR measures *expected* value creation at announcement, not realised
  performance; don't over-claim.
- Uncertain: exact window conventions vary by journal and subfield; mirror recent papers
  in your target outlet.

## Verify
- [ ] Each event date checked against the earliest newswire mention and market hours.
- [ ] Estimation window ends ≥ ~30 days before the event; minimum-observation rule applied.
- [ ] Confounding news screened and the number of dropped events reported.
- [ ] Results shown for 2+ windows and 2+ test statistics, including BMP or a rank test.
- [ ] A few CARs reproduced independently (spreadsheet or Eventus).
