---
id: health-medicine.public-health.disease-surveillance.case-definitions-notification-and-signal-detection
name: case-definitions-notification-and-signal-detection
category: health-medicine
field: public-health
product: disease-surveillance
tags: [public-health, disease-surveillance, epidemiological-surveillance, notifiable-diseases, notification, case-definition, confirmed-probable-suspected, passive-surveillance, active-surveillance, sentinel-surveillance, syndromic-surveillance, event-based-surveillance, indicator-based-surveillance, laboratory-surveillance, wastewater-surveillance, ihr-2005, aberration-detection, cusum, farrington-algorithm, ears, epi-curve, signal-verification, surveillance-evaluation, cdc-surveillance-guidelines, reporting-delay, completeness, timeliness]
level: practitioner
status: gated
description: "Running disease surveillance: surveillance types, writing tiered case definitions, notification workflows, aberration detection (CUSUM/Farrington), signal verification and evaluating the system."
sources: ["https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5013a1.htm", "https://www.who.int/publications/i/item/9789241580496"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case definitions, notification and signal detection

> General professional reference. Notifiable-disease lists, reporting timeframes and
> legal duties are set nationally/locally; check your jurisdiction's current list.

**Goal:** turn scattered clinical and lab reports into timely, comparable counts, and
notice the unusual early enough to act — without chasing noise.

## 1. Pick the right surveillance type
| Type | Use | Weakness |
|---|---|---|
| Passive (clinician/lab notification) | broad, cheap baseline | under-reporting, delays |
| Active (staff solicit reports) | elimination targets, outbreaks | resource-heavy |
| Sentinel (selected sites) | influenza, STIs, high-quality detail | not population-representative |
| Syndromic (ED chief complaints, calls) | early warning, mass gatherings | low specificity |
| Laboratory/genomic | pathogen typing, cluster detection | depends on testing behaviour |
| Event-based (media, rumours, IHR) | novel threats | verification burden |
| Environmental/wastewater | community trends incl. asymptomatic | no individual linkage |

## 2. Case definitions
- Components: **clinical** criteria, **laboratory** criteria, **epidemiological**
  link, plus **person, place, time** restrictions.
- Tier them: **confirmed** (lab), **probable** (clinical + epi link, or presumptive
  lab), **suspected/possible** (clinical only). Sensitive definitions for early
  outbreak case finding; specific ones for trend reporting and analytic studies.
- Use the national/international definition for routine reporting so data are
  comparable; record which version was used — a definition change creates an
  artefactual step in the trend.

## 3. Notification workflow
- Who reports (clinician, lab, school, care home), what (minimum dataset), how
  (electronic lab reporting, portal, phone for urgent), how fast (set by local law;
  check the jurisdiction's current list and timeframes).
- Intake: deduplicate, check against definition, classify, assign follow-up, record
  dates (onset, specimen, report) to measure delays.
- Under the **International Health Regulations (2005)** each State Party has a National IHR Focal Point. The Regulations were amended in 2022 and 2024, so check the current text and the Annex 2 decision instrument (gated: unconfirmed, source is paywalled or blocked) before notifying an event.

## 4. Analysis and signal detection
- Routine outputs: counts and rates by week, age, sex, area; **epi curves** by onset
  date (account for reporting delay — the last weeks are always incomplete; consider
  nowcasting).
- Thresholds: historical mean ± k SD, **CUSUM**, **Farrington** (quasi-Poisson,
  seasonality-aware), CDC EARS for syndromic data. Spatial/space-time scan statistics
  (SaTScan) for clusters (gated: unconfirmed, source is paywalled or blocked).
- A statistical alarm is a **signal, not an outbreak**. Verify: data artefact
  (duplicate batch, new lab, definition change, testing surge)? Real increase? Same
  organism/type? Linked cases?
- Single cases can be signals by themselves (e.g. botulism, polio, novel influenza,
  diphtheria) (gated: unconfirmed, source is paywalled or blocked).

## 5. Dissemination
Feed back to reporters (they report more when they see use), weekly bulletins,
dashboards with caveats on completeness, and rapid alerts to clinicians when action is
needed. Signal → `health-medicine.public-health.outbreak-investigation.stepwise-field-investigation-and-control`.

## 6. Evaluate the system (CDC framework)
Attributes: simplicity, flexibility, data quality, acceptability, **sensitivity**,
**positive predictive value**, representativeness, **timeliness**, stability.
Measure completeness and delays against targets; audit a sample against source
records.

## Gotchas
- Trend changes driven by testing policy, not disease.
- Small-number rates fluctuate wildly; aggregate or suppress per disclosure rules.
- Privacy: minimum necessary identifiers; secure transfer; small-cell suppression in
  publications.

## Verify
- [ ] Case definition version and tier recorded for each case.
- [ ] Onset, specimen and report dates captured; delays measured.
- [ ] Signals checked for artefacts before escalation.
- [ ] Alerts and feedback routinely sent to reporters.
- [ ] System evaluated against CDC attributes at least periodically.

## Checked

- Date checked: 2026-10-25. Jurisdiction: International (WHO IHR); notifiable-disease lists and timeframes are national or local.
- Sources read: CDC MMWR RR-13 (2001) surveillance evaluation guidelines; WHO IHR third edition landing page.
- Confirmed: The nine evaluation attributes (simplicity, flexibility, data quality, acceptability, sensitivity, predictive value positive, representativeness, timeliness, stability).
- Corrected or removed: The example reporting timeframes for meningococcal disease and measles were removed (not confirmed); the IHR sentence now says the Regulations were amended in 2022 and 2024 (per the WHO page).
- Gated: The Annex 2 instrument text, the CUSUM/Farrington/EARS/SaTScan descriptions and the single-case signal examples. The Farrington paper and the current IHR text were not read in this batch.

Method: documentation only; no commands were run.
