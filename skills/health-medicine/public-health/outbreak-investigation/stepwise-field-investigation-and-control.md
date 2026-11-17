---
id: health-medicine.public-health.outbreak-investigation.stepwise-field-investigation-and-control
name: stepwise-field-investigation-and-control
category: health-medicine
field: public-health
product: outbreak-investigation
tags: [public-health, outbreak-investigation, outbreak-response, field-epidemiology, ten-steps, outbreak-case-definition, case-finding, line-list, epi-curve, point-source, propagated-outbreak, incubation-period, hypothesis-generation, trawling-questionnaire, case-control-study, cohort-study, attack-rate, odds-ratio, risk-ratio, food-borne-outbreak, contact-tracing, isolation, quarantine, control-measures, outbreak-control-team, wgs, genomic-epidemiology, declaring-outbreak-over]
level: practitioner
status: gated
description: "Field outbreak investigation: verify, define cases, find them, line list and epi curve, generate and test hypotheses (cohort/case-control), control measures, contact tracing and closure."
sources: ["https://www.cdc.gov/", "https://www.who.int/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stepwise field investigation and control

> General professional reference. Legal powers (exclusion, isolation, closures) and
> outbreak-plan roles are set by local law and the local outbreak plan.

**Goal:** stop transmission as fast as possible while collecting the evidence that
identifies the source — the steps overlap, and **control measures never wait for the
analytic study**.

## 1. The classic steps (run in parallel, not strictly sequential) (gated: unconfirmed, source is paywalled or blocked)
1. **Prepare** — team, roles, outbreak control team (OCT) if threshold met, lab
   liaison, communications lead.
2. **Confirm an outbreak exists** — compare to expected (surveillance baseline,
   seasonality); exclude artefacts (new test, reporting change, pseudo-outbreak from
   lab contamination).
3. **Verify the diagnosis** — clinical review, lab confirmation, typing (WGS).
4. **Case definition** — clinical + lab + person/place/time; tiered
   confirmed/probable/possible (see
   `health-medicine.public-health.disease-surveillance.case-definitions-notification-and-signal-detection`).
5. **Find and count cases** — notifications, labs, GPs, EDs, schools, attendee lists;
   build a **line list** (one row per case: ID, demographics, onset, symptoms, lab,
   exposures, outcome).
6. **Descriptive epidemiology** — time (epi curve), place (map), person (age, sex,
   occupation, attack rates).
7. **Hypotheses** — from descriptive data, trawling interviews of early cases, pathogen
   biology.
8. **Test hypotheses** — analytic study.
9. **Refine and do further studies** (environmental, food tracing, lab).
10. **Implement control and prevention** — from day one.
11. **Communicate** — OCT minutes, public messages, final report.
12. **Maintain surveillance** and declare the outbreak over.

## 2. Reading the epi curve
- Interval on the x-axis ≈ ⅛–⅓ of the incubation period (gated: unconfirmed, source is paywalled or blocked).
- **Point source**: tight peak within one incubation period range; estimate exposure
  time by counting back the median incubation from the peak (or min from first case,
  max from last).
- **Continuous common source**: plateau. **Propagated**: successive waves an
  incubation period apart. Outliers are informative (index case, secondary cases,
  different exposure).

## 3. Analytic studies
- **Cohort** (defined group, e.g. wedding guests): attack rate per exposure → **risk
  ratio**, with CI. Questionnaire everyone, ill and well.
- **Case-control** (open population): **odds ratio**; controls from the source
  population (neighbourhood, GP list, random digit dialling, case-nominated friends).
  Typically 2–4 controls per case where cases are few (gated: unconfirmed, source is paywalled or blocked).
- Look for dose–response and the exposure that explains most cases. Stratify for
  confounding; beware recall bias and multiple testing with long food lists.
- Microbiological and genomic links (same WGS cluster) and trace-back can be stronger
  evidence than the statistics.

## 4. Control measures (hierarchy)
- **Source**: remove/recall food, close premises, fix water treatment, decontaminate.
- **Transmission**: hygiene, exclusion of cases (e.g. food handlers until
  microbiologically clear per guidance), isolation, infection-control measures.
- **Susceptibles**: vaccination, post-exposure prophylaxis (**agent and dose per
  current national guidance**), quarantine of contacts.
- **Contact tracing**: define contact by exposure type/duration for the pathogen;
  prioritise high-risk contacts (immunocompromised, pregnant, healthcare workers,
  young children).

## 5. Communication
Single spokesperson, consistent messages, early holding statements, protect case
confidentiality, brief clinicians on testing and reporting.

## 6. Declaring it over
Commonly **two maximum incubation periods** with no new cases linked (gated: unconfirmed, source is paywalled or blocked) (pathogen-specific
criteria may differ). Write the final report with lessons and recommendations.

## Gotchas
- Waiting for "the study" before acting while people are still exposed.
- Case definition drift mid-outbreak without version control.
- Controls who aren't from the same population as cases.
- Forgetting the denominator — counts without attack rates mislead.

## Verify
- [ ] Outbreak confirmed against baseline; artefacts excluded.
- [ ] Versioned case definition and a maintained line list.
- [ ] Epi curve with appropriate interval and an exposure-window estimate.
- [ ] Analytic study with measure of association and CI, or reasoned why not.
- [ ] Control measures documented with start dates; contacts managed.
- [ ] End criterion stated; final report written.

## Checked

- Date checked: 2026-10-25. Jurisdiction: International; legal powers are local.
- Sources read: None: the CDC Principles lesson 6 page returned 404 and no other primary outbreak-method page loaded.
- Confirmed: Nothing in this skill could be confirmed.
- Corrected or removed: No corrections found; unverifiable specifics are marked.
- Gated: The step list, epi-curve interval rule, control-to-case ratio and the "two maximum incubation periods" closure rule.

Method: documentation only; no commands were run.
