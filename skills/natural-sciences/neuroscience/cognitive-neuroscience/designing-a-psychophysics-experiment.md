---
id: natural-sciences.neuroscience.cognitive-neuroscience.designing-a-psychophysics-experiment
name: designing-a-psychophysics-experiment
category: natural-sciences
field: neuroscience
product: cognitive-neuroscience
tags: [cognitive-neuroscience, neuroscience, psychophysics, experiment-design, task-design, psychopy, psychtoolbox, jspsych, staircase, quest, method-of-constant-stimuli, psychometric-function, threshold, signal-detection-theory, d-prime, 2afc, reaction-time, display-timing, monitor-calibration, gamma, counterbalancing, power-analysis, preregistration, informed-consent, ethics, online-experiments]
level: advanced
status: verified
description: "Design a human psychophysics or cognitive task: stimulus timing and calibration, constant stimuli vs staircases, psychometric fits and d′, trial counts, counterbalancing and ethics."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing a psychophysics experiment

**Goal:** measure a perceptual or cognitive quantity (threshold, sensitivity, bias,
reaction time) precisely, with stimuli you actually presented as specified.

## 1. Define the quantity and the task
- What do you estimate? A detection or discrimination **threshold**, a **point of
  subjective equality (PSE)**, **sensitivity (d′)** vs **criterion**, or RT effects.
- **Forced-choice (2AFC/2IFC)** tasks reduce criterion effects; yes/no tasks need
  signal detection analysis to separate sensitivity from bias.
- Write the hypothesis and analysis plan; pre-register where possible.

## 2. Stimulus presentation and timing
- Use dedicated software: **PsychoPy**, **Psychtoolbox** (MATLAB/Octave),
  or **jsPsych**/PsychoJS online. Define durations in **frames**, not milliseconds,
  on a fixed refresh rate (e.g. 60 Hz → 16.7 ms per frame).
- Verify timing with a **photodiode** on the screen and log dropped frames. Reported
  timing from software is not proof; LCD response times and OS compositing add lag.
- **Monitor calibration:** measure luminance with a photometer, linearise **gamma**,
  set brightness/contrast fixed; for colour work, characterise the display spectrally.
- Fix viewing distance (chin rest) and express stimulus size in **degrees of visual angle**.
- Response devices: keyboards have variable latency (often several to tens of ms);
  use a response box for precise RTs.
- **Online experiments:** you lose control of display, distance and timing — choose
  measures robust to that and add attention checks.

## 3. Choosing levels: constant stimuli vs adaptive
- **Method of constant stimuli:** fixed levels spanning chance to near-perfect,
  randomly interleaved. Gives the whole psychometric function; needs more trials.
- **Adaptive staircases:** e.g. 2-down/1-up converges near 70.7% correct;
  3-down/1-up near 79.4%. Interleave 2+ staircases to hide the rule; average the last
  N reversals, discarding early ones.
- **QUEST / Bayesian adaptive** (e.g. QUEST+, Psi) methods estimate threshold and
  slope efficiently.

## 4. Analysis
- Fit a psychometric function (cumulative Gaussian or Weibull) with free
  **lapse rate** (a few %) so occasional errors don't bias slope; tools: `psignifit`,
  `quickpsy` (R), or custom maximum-likelihood fits.
- Signal detection: d′ = z(hit rate) − z(false-alarm rate); correct rates of 0 or 1
  (e.g. log-linear correction).
- Reaction times: right-skewed — use medians, log-transforms or mixed models; set
  fast/slow exclusion cut-offs a priori; analyse accuracy and RT together
  (speed–accuracy trade-off; drift diffusion models when appropriate).

## 5. Design details that matter
- **Trial counts:** thresholds typically need hundreds of trials per condition
  per participant; small-N, many-trial designs are legitimate in psychophysics.
- **Counterbalance** condition order and response mappings; randomise trial order within blocks.
- **Practice trials** and feedback rules decided in advance; fatigue breaks.
- Catch trials and attention checks.
- **Power analysis** at the level you'll test (participants and trials).

## 6. Ethics and protocol
Ethics approval, informed consent, right to withdraw, data protection
(pseudonymised IDs, no identifiable data in filenames), photosensitive-epilepsy
screening for flicker stimuli, and fair compensation. Combining with imaging or
stimulation adds screening requirements (see
natural-sciences.neuroscience.neuroimaging.fmri-preprocessing-and-first-level-analysis
for fMRI design).

## Verify
- [ ] Quantity to estimate and task type chosen to separate sensitivity from bias.
- [ ] Timing verified with a photodiode; display calibrated; visual angle computed.
- [ ] Level-selection method justified; trial counts sufficient.
- [ ] Psychometric fits include lapse; exclusions pre-specified.
- [ ] Ethics approval, consent and data-protection steps in place.

Checks run: transformed up-down rules converge where p^k = 0.5, i.e. 0.5^(1/2) = 70.7 % and 0.5^(1/3) = 79.4 %; simulated 2-down/1-up and 3-down/1-up staircases on a 2AFC cumulative-Gaussian observer converged to 70.3 % and 79.4 % correct. With a perfect hit rate and zero false alarms, d′ is infinite until corrected; the log-linear correction (add 0.5 to counts, 1 to totals) gives d′ = 4.50 for 40/40 hits and 0/40 false alarms. Keyboard latency figures vary greatly by hardware.
