---
id: social-sciences.sports-science-kinesiology.sports-performance-analysis-research.gps-load-monitoring-and-notational-analysis-reliability
name: gps-load-monitoring-and-notational-analysis-reliability
category: social-sciences
field: sports-science-kinesiology
product: sports-performance-analysis-research
tags: [sports-performance-analysis-research, performance-analysis, sports-science, kinesiology, gps, gnss, catapult, statsports, lps, local-positioning, accelerometry, playerload, high-speed-running, sprint-distance, speed-zones, acceleration-thresholds, dwell-time, training-load, session-rpe, acwr, acute-chronic-workload-ratio, ewma, notational-analysis, match-analysis, event-data, tracking-data, sportscode, hudl, nacsport, inter-observer-reliability, kappa, performance-modelling]
level: practitioner
status: draft
description: "Use GPS/load-monitoring and notational data in research: device validity, speed-zone and acceleration definitions, ACWR pitfalls, and inter-observer reliability of coding."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPS load monitoring and notational analysis — research-grade

**Goal:** turn tracking and coded-match data into research variables whose validity,
reliability and definitions are clear enough that results can be compared and replicated.

## 1. Tracking devices
- **GNSS units** (Catapult, STATSports, GPSports…) at 10–18 Hz; **LPS** (local
  positioning) and optical tracking in stadiums. Accuracy degrades for short sprints,
  high accelerations and changes of direction, and near tall stands (satellite
  blockage). Check validation studies for the specific model and firmware.
- Record and report: sampling rate, number of satellites and HDOP, firmware and software
  version (manufacturers' filtering changes between versions, shifting values).
- **Same unit per athlete** across the study — inter-unit differences can be meaningful.
- Inter-system comparisons (GPS vs LPS vs optical) are not interchangeable without
  calibration equations.

## 2. Define variables precisely
- **Speed zones:** absolute (e.g. high-speed running > 5.5 m/s, sprint > 7 m/s are common
  in football, but thresholds vary) or individualised (% of max sprint speed, or
  relative to MAS). State thresholds and how individual references were tested.
- **Acceleration/deceleration efforts:** threshold (e.g. > 2 or 3 m/s²) **and minimum
  dwell time** (e.g. 0.5 s) — dwell-time settings change counts dramatically.
- **Accelerometer load** (PlayerLoad and equivalents) is proprietary in detail; report
  the vendor metric name and version.
- **Internal load:** session RPE (CR-10 × duration, collected ~30 min post-session),
  heart-rate-based TRIMP.

## 3. Load–injury modelling cautions
- The **acute:chronic workload ratio (ACWR)** became popular but has been heavily
  criticised: mathematical coupling (acute load is part of chronic), spurious
  correlation, ratio artefacts, and weak predictive accuracy. Uncoupled versions and
  EWMA reduce some issues but don't make it a validated injury predictor.
- Model injury as a time-to-event or repeated-measures outcome with appropriate
  methods; report predictive performance (e.g. AUC with cross-validation), not just
  associations. Small numbers of injuries per team limit what's estimable.

## 4. Notational analysis
- Build an **operational definition for every event** (what counts as a "pass under
  pressure", where possession starts/ends), with video examples, before coding.
- Tools: Hudl Sportscode, Nacsport, Dartfish, LongoMatch, or custom tagging; commercial
  event data (e.g. Opta/StatsBomb-type providers) have their own definitions — read them.
- **Reliability:** two observers code a sample of matches independently; report
  Cohen's kappa for categorical events (κ > ~0.8 often treated as very good), ICC or
  percentage error for frequencies/times, plus intra-observer reliability after a
  delay (O'Donoghue's methods texts discuss thresholds).
- Code events as time-stamped data so they can be linked with tracking data.

## 5. Performance modelling
- Contextual factors matter: match location, opponent quality, score line, playing
  position, formation, minutes played — include them as covariates or random effects.
- Repeated observations per player and team → mixed models; normalise per 90 minutes
  cautiously (low-minute players produce extreme rates).
- Distinguish **performance indicators** (valid, linked to outcomes) from mere counts.

## 6. Data governance
Athlete tracking data are personal (sometimes health) data; contracts and GDPR-like
laws govern use. Get club and athlete consent for research use and de-identify outputs.

## Gotchas
- Changing vendor software mid-season breaks time series silently.
- Team-sport samples are small clusters; "n = 25 players × 40 sessions" is not n = 1000.
- Uncertain: threshold values and kappa cut-offs above are common conventions; they are not universal.

## Verify
- [ ] Device model, sampling rate, firmware/software version and unit allocation reported.
- [ ] Speed, acceleration thresholds and dwell times stated.
- [ ] Load–injury analyses avoid ACWR-only inference and report predictive accuracy.
- [ ] Notational definitions documented; inter- and intra-observer reliability reported.
- [ ] Context and repeated-measures structure modelled.
