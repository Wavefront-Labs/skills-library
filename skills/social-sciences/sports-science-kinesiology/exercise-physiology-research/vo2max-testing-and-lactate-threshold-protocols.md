---
id: social-sciences.sports-science-kinesiology.exercise-physiology-research.vo2max-testing-and-lactate-threshold-protocols
name: vo2max-testing-and-lactate-threshold-protocols
category: social-sciences
field: sports-science-kinesiology
product: exercise-physiology-research
tags: [exercise-physiology-research, exercise-physiology, sports-science, kinesiology, vo2max, vo2peak, cardiopulmonary-exercise-testing, cpet, metabolic-cart, gas-exchange, calibration, ramp-protocol, incremental-test, verification-bout, rer, plateau, lactate-threshold, lt1, lt2, obla, dmax, ventilatory-threshold, vt1, vt2, critical-power, cycle-ergometer, treadmill, training-intervention, responders, acsm, bases]
level: practitioner
status: draft
description: "Run research-grade VO2max and lactate threshold tests: calibration, ramp vs step protocols, plateau and verification criteria, threshold methods and training-study controls."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VO2max testing and lactate threshold protocols

**Goal:** produce maximal-oxygen-uptake and threshold values that are valid, repeatable
and comparable across participants and time points in a research study.

## 1. Before testing
- **Screening:** pre-participation health questionnaire (e.g. PAR-Q+), ACSM screening
  logic; medical supervision and an emergency plan per local rules.
- **Standardise:** no strenuous exercise 24–48 h before, no caffeine/food for ~2–3 h,
  same time of day across visits (circadian effects), similar hydration and footwear.
- **Calibrate the metabolic cart** before every test: gas calibration with certified
  reference gases, volume/flow calibration with a 3-L syringe; record ambient conditions.
  Periodically verify with a metabolic simulator if available.
- Familiarise participants with the ergometer, mouthpiece/mask and the RPE scale.

## 2. VO2max protocol
- **Mode:** treadmill typically yields ~5–10% higher VO2max than cycling in untrained or
  runners; use the sport-specific mode for athletes.
- **Ramp/incremental test** designed to reach exhaustion in about **8–12 minutes**
  (Buchfuhrer et al. 1983 is the usual citation). Example cycle ramp: 3-min warm-up then
  +20–30 W/min (adjust for fitness); treadmill: constant speed with grade increments.
- Strong verbal encouragement, standardised across participants.
- **Averaging:** report the highest value from a defined averaging interval (e.g. 30 s or
  a 15-breath rolling average). Breath-by-breath peaks with short windows inflate values;
  state the interval.

## 3. Was it maximal?
- Traditional secondary criteria (RER ≥ 1.10–1.15, HR within 10 bpm of age-predicted max,
  RPE ≥ 17–19, blood lactate ≥ 8 mmol/L) are **unreliable** — they can be met at
  submaximal efforts or missed at true max.
- A **VO2 plateau** (e.g. < 150 mL/min rise despite increasing work) occurs in only a
  subset of people.
- Best practice: a **verification bout** — after 10–20 min recovery, a constant load at
  ~105–110% of peak ramp power to exhaustion; VO2 within ~2–3% of the ramp peak confirms
  max. Report as VO2peak if not verified.

## 4. Lactate thresholds
- **Step test:** 3–5-min stages (lactate needs time to stabilise), earlobe or fingertip
  capillary sample in the last 30 s of each stage, analyser calibrated (Lactate Pro, Biosen).
- Methods differ and are **not interchangeable**: LT1 (first rise above baseline), fixed
  4 mmol/L (OBLA), Dmax/modified Dmax, log-log, baseline + 1 mmol/L. Name the method,
  and use one consistently. Software: Lactate-E or custom R/Python fits.
- Ventilatory thresholds (VT1 via V-slope/ventilatory equivalents, VT2/RCP) from the ramp
  test — blinded visual identification by two raters improves reliability.

## 5. Training-intervention studies
- Randomised control group (or crossover) — fitness improves from familiarisation and
  season alone.
- Match or record training load (session RPE, heart rate, power), monitor adherence.
- Typical error of VO2max is ~3–5%; individual "non-responder" claims need repeated
  testing and comparison against that error (Atkinson & Batterham; Hecksteden et al.).

## Gotchas
- Mask leaks and uncalibrated flow sensors silently corrupt data — watch for implausible RER.
- Expressing VO2max per kg body mass confounds fitness with body composition; consider
  allometric scaling or per kg fat-free mass.
- Uncertain: ramp rates and verification thresholds above are typical ranges from the
  literature, not single standards.

## Verify
- [ ] Gas and volume calibration logged before each test.
- [ ] Pre-test standardisation documented and repeated across visits.
- [ ] Test duration 8–12 min; averaging interval stated.
- [ ] Maximality confirmed by verification bout, else reported as VO2peak.
- [ ] Threshold method named and applied consistently; control group in interventions.
