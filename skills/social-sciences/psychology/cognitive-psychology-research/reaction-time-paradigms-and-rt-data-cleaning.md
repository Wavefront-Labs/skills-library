---
id: social-sciences.psychology.cognitive-psychology-research.reaction-time-paradigms-and-rt-data-cleaning
name: reaction-time-paradigms-and-rt-data-cleaning
category: social-sciences
field: psychology
product: cognitive-psychology-research
tags: [cognitive-psychology-research, cognitive-psychology, psychology, reaction-time, rt, response-time, mental-chronometry, stroop, flanker, simon-task, posner-cueing, visual-search, n-back, priming, speed-accuracy-tradeoff, ies, drift-diffusion, ddm, ex-gaussian, outliers, rt-trimming, log-rt, mixed-models, accuracy, error-rates, cognitive-modelling]
level: practitioner
status: gated
description: "Run reaction-time experiments that measure cognition, not noise: trial structure, practice, speed-accuracy trade-offs, RT trimming rules and why to model raw RTs."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reaction-time paradigms and RT data cleaning

**Goal:** design chronometric tasks (Stroop, flanker, cueing, visual search, priming)
whose RT differences reflect the cognitive process of interest, and clean RT data
with rules you fixed in advance.

## 1. Trial anatomy
A standard trial: fixation (often jittered, e.g. 500–1000 ms, to stop anticipation) →
optional cue → stimulus → response window (e.g. up to 2000 ms) → feedback (practice
only) → inter-trial interval. Write every duration down; reviewers will ask, and the
timing must be verified on the actual hardware (see
social-sciences.psychology.experiment-software).

## 2. Design rules
- **Many trials per condition** — RT effects of 20–50 ms need dozens of trials per
  cell per participant; reliability of difference scores is notoriously low with few
  trials ("reliability paradox": robust group effects, poor individual-difference
  reliability).
- **Practice block** discarded from analysis; first trials of each block are often slow.
- **Counterbalance response mappings** (left/right key to category) across participants.
- **Randomise trial order** with constraints (e.g. no more than 3–4 repeats of the same
  condition) — but note that sequence effects (congruency sequence effect,
  repetition priming) exist and may need modelling.
- Instruct **"respond as quickly and accurately as possible"** and keep instructions
  identical across conditions.

## 3. Speed–accuracy trade-off
Always analyse accuracy alongside RT. If a condition is faster but less accurate, the
RT effect is uninterpretable on its own. Options: report both; combine with inverse
efficiency (IES = mean correct RT / proportion correct, only sensible when accuracy is
high, roughly > 90%); or fit a **drift-diffusion model** (e.g. HDDM, `rtdists`, fast-dm; `rtdists` is on CRAN, HDDM is on GitHub (hddm-devs/hddm, last PyPI release 1.0.1, Dec 2023)),
which separates processing speed (drift rate) from caution (boundary) and non-decision time.

## 4. Cleaning RTs — decide before you look
Typical preregistered pipeline:
1. Remove practice trials and error trials (for RT analysis; keep them for accuracy).
2. Remove trials after an error if post-error slowing is a concern.
3. Remove anticipations (e.g. < 150–200 ms) and timeouts / very slow responses
   (e.g. > 2000–3000 ms, or task-specific).
4. Optionally remove trials beyond ±2.5–3 SD of each participant's condition mean —
   but SD-based trimming is sensitive to cell size: with n trials in a cell the largest possible z-score is (n-1)/sqrt(n), so a ±2.5 SD rule can never remove anything when n ≤ 7 (max z 2.27) and an extreme trial inflates the SD that is meant to catch it (computed: 9 trials near 500 ms plus one 1500 ms trial gave z = 2.83, just over 2.5, versus a MAD-based score of about 45). Median absolute deviation is more robust.
5. Exclude participants with accuracy near chance or excessive trial loss (e.g. > 25–30%).
Report how many trials and participants each step removed.

## 5. Analysis
- RT distributions are positively skewed. Rather than averaging per participant then
  running ANOVA, prefer **trial-level mixed models** with participants and items as
  random effects (see social-sciences.psychology.behavioural-data-analysis).
- Log-transforming RT changes what interactions mean (additive vs multiplicative);
  generalised mixed models with a Gamma or inverse-Gaussian link on raw RT are an
  alternative (Lo & Andrews 2015 argue this; still debated).
- Distributional analysis (ex-Gaussian, delta plots, quantiles) shows *where* in the
  distribution an effect lives — useful for theory, e.g. whether an effect grows with RT.

## 6. Cognitive modelling
Go beyond mean differences when theory allows: diffusion models, race models, or
computational models of memory/attention fitted per participant. Check parameter
recovery on simulated data before trusting fitted parameters.

## Gotchas
- Keyboards add variable latency (tens of ms, device-dependent); a response box or
  validated setup matters for small effects, much less for large ones.
- Online samples have more noise and more inattentive participants — raise trial counts.
- Excluding outliers after seeing which choice gives significance is p-hacking.
- Uncertain: trimming cut-offs vary by task; cite field-specific conventions.
- Checked 2026-10-19: the max-z arithmetic and MAD example were computed; the Lo & Andrews (2015) GLMM argument and the "reliability paradox" were not re-read (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Trial timings documented and measured on the real setup.
- [ ] Accuracy analysed and speed–accuracy trade-off ruled out or modelled.
- [ ] Cleaning steps preregistered with counts of removed trials reported.
- [ ] Trial-level model with participant (and item) random effects used.
- [ ] Reliability of any individual-difference RT score reported.
