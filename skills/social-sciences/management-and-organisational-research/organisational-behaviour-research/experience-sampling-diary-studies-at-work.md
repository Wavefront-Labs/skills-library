---
id: social-sciences.management-and-organisational-research.organisational-behaviour-research.experience-sampling-diary-studies-at-work
name: experience-sampling-diary-studies-at-work
category: social-sciences
field: management-and-organisational-research
product: organisational-behaviour-research
tags: [organisational-behaviour-research, organizational-behavior, ob-research, diary-study, experience-sampling, esm, ecological-momentary-assessment, ema, daily-diary, within-person, multilevel-model, mlm, hlm, lme4, mplus, person-mean-centering, icc, work-attitudes, job-satisfaction, burnout, compliance-rate, attrition, qualtrics, expiwell, organisational-psychology, io-psychology]
level: practitioner
status: draft
description: "Design and analyse daily-diary / experience-sampling studies of employees: sampling schedule, short measures, compliance, centering and multilevel models for within-person effects."
sources:
  - "Bolger & Laurenceau, Intensive Longitudinal Methods (2013)"
  - "Ohly, Sonnentag, Niessen & Zapf (2010), Diary studies in organizational research, J. Personnel Psychology"
  - "Gabriel et al. (2019), Experience sampling methods: a discussion of critical trends, Organizational Research Methods"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Experience-sampling and diary studies at work

**Goal:** capture how employees' states (mood, workload, engagement) fluctuate day to day
and test *within-person* relationships ("on days with more interruptions, is exhaustion
higher?") that a one-shot survey cannot answer.

## 1. Decide the design before the app
- **Question level.** Between-person ("people with high workload are more exhausted")
  vs within-person ("on high-workload days, the same person is more exhausted"). Diary
  designs exist for the second; say which in your hypotheses.
- **Sampling scheme.**
  - *Daily diary*: 1–3 surveys/day (e.g. before work, end of work, bedtime) for 5–10
    workdays. Typical for work–home spillover and recovery.
  - *Experience sampling (ESM)*: 4–8 signals/day at random or semi-random times within
    working hours. Use for momentary affect or task switching.
  - *Event-contingent*: respondent reports after each event (conflict, meeting).
- **Length.** Ten workdays across two weeks is a common compromise; fatigue rises sharply
  past roughly 2–3 weeks (rule of thumb, not a law).
- **Power.** Level-2 N (people) matters more for cross-level effects; level-1 N
  (occasions) for within-person slopes. Around 100 people × 10 days is a frequently seen
  floor in OB journals; simulate with `simr` (R) or Mplus Monte Carlo rather than trusting it.

## 2. Measures
- Keep each signal under ~2–3 minutes. Shorten validated scales to 2–4 items, report
  which items, and check reliability **at both levels** (multilevel omega or
  within/between alpha via multilevel CFA).
- Reword to the time frame: "Today at work, I felt…" / "Right now…".
- Collect stable traits and demographics once, in a baseline survey.

## 3. Fieldwork
- Tools: Qualtrics with scheduled SMS/email links, or dedicated ESM apps (e.g.
  ExpiWell, m-Path, mEMA — check current features and data-residency terms yourself).
- Pilot with 5–10 people for 2–3 days: do signals arrive, do night-shift workers get
  pinged at sensible local times, how long does it really take?
- Send a reminder ~30–60 min after a missed signal and close the window after a fixed
  time; record the actual completion timestamp.
- Monitor compliance daily and nudge low responders. Report the compliance rate
  (completed / scheduled) and exclusion rules decided in advance.
- Incentives tied to compliance thresholds (e.g. bonus at ≥ 80%) help but disclose them.

## 4. Analysis
1. Data in long format: one row per person × occasion.
2. Compute the **ICC** of each variable (null multilevel model). A low ICC means most
   variance is within-person — exactly what justifies the design.
3. **Centre**: person-mean centre level-1 predictors (`x - mean_i(x)`) to isolate the
   within-person effect; add the person mean as a level-2 predictor to get the
   between-person effect. Grand-mean centring blends the two — the classic mistake.
4. Fit random-intercept, then random-slope models. In R:
   ```r
   library(lme4)
   m <- lmer(exhaustion ~ workload_cw + workload_pm + (1 + workload_cw | id), data = d)
   ```
   Add `day` (and lagged outcome for spillover) to control time trends and carry-over.
5. For lagged/mediation models across days, consider multilevel SEM in Mplus or
   dynamic SEM; autocorrelated residuals are common.
6. Report level-1 and level-2 N, missing data handling (MLM uses all available
   occasions under MAR), and both pseudo-R² levels if used.

## Gotchas
- **Reactivity**: being asked daily about stress can change it; note it as a limitation.
- **Weekend / shift gaps**: lags across a weekend are not one-day lags — model the gap
  or drop those pairs.
- **Same-source bias** persists within person; separating measurement times (morning
  predictor, evening outcome) helps.
- **Employer access**: if recruitment goes through the employer, guarantee that
  managers never see individual responses — say so in consent materials.

## Verify
- [ ] Hypotheses state within- vs between-person level explicitly.
- [ ] Pilot confirmed signal timing, duration and time zones.
- [ ] Compliance rate, exclusions and reliability at both levels are reported.
- [ ] Level-1 predictors person-mean centred; person means entered at level 2.
- [ ] Time trend / lagged outcome considered; weekend gaps handled.
