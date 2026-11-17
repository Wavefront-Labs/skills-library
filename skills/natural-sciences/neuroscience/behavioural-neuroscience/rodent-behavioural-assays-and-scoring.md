---
id: natural-sciences.neuroscience.behavioural-neuroscience.rodent-behavioural-assays-and-scoring
name: rodent-behavioural-assays-and-scoring
category: natural-sciences
field: neuroscience
product: behavioural-neuroscience
tags: [behavioural-neuroscience, neuroscience, behavioral-neuroscience, rodent-behaviour, mouse-behaviour, open-field, elevated-plus-maze, morris-water-maze, fear-conditioning, freezing, novel-object-recognition, operant-conditioning, habituation, counterbalancing, blinding, randomisation, video-tracking, deeplabcut, eztrack, anymaze, ethovision, inter-rater-reliability, arrive-guidelines, sex-as-variable, circadian]
level: advanced
status: draft
description: "Run rodent behavioural assays that replicate: assay choice, controlling handling, time of day, order and sex, blinding and randomisation, automated tracking (DeepLabCut etc.) and reliable scoring."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rodent behavioural assays and scoring

**Goal:** behavioural data where differences reflect the manipulation, not the
experimenter, the time of day, the test order or the scoring method.

## 1. Choose the assay for the construct — and know its limits
- **Locomotion/exploration:** open field (distance, centre time).
- **Anxiety-like behaviour:** elevated plus maze, light–dark box (centre/open-arm
  measures are confounded by locomotion — report both).
- **Spatial learning/memory:** Morris water maze, Barnes maze.
- **Recognition memory:** novel object recognition (requires objects balanced for
  preference and well-cleaned to remove odour cues).
- **Associative learning:** Pavlovian fear conditioning (freezing), operant tasks
  (lever press/nose poke in chambers).
State the construct cautiously: "anxiety-like" or "freezing", not "fear" or "anxiety".

## 2. Control the hidden variables
- **Habituation:** to the room (≥30–60 min before testing), handling (several days
  of gentle handling; tunnel or cup handling reduces stress compared with tail pick-up).
- **Time of day:** rodents are nocturnal; test in a consistent circadian window,
  record it; consider reversed light cycles.
- **Experimenter:** the same person, or counterbalance experimenters across groups;
  experimenter sex/odour has been reported to affect rodent stress responses.
- **Environment:** light level (lux) in the apparatus, noise, cleaning agent and
  inter-trial cleaning (e.g. 70% ethanol), cage changes (not on test day).
- **Order effects:** in a test battery, run least stressful tests first; counterbalance order across groups.
- **Sex:** include both sexes or justify; oestrous stage may matter for some measures.
- **Housing:** single vs group housing changes behaviour; keep identical across groups.

## 3. Design
- **Randomise** allocation to groups and test order (by cage, accounting for litter).
- **Blind** the experimenter and scorer to group; code videos.
- **Power analysis** from pilot or published effect sizes; behavioural variance is large.
- Pre-define primary outcome measures and exclusion criteria (e.g. animals falling
  off the maze, tracking failures).
- Report per **ARRIVE** guidelines.

## 4. Recording and scoring
- Record video of every session, with consistent camera position, resolution and
  frame rate (≥25–30 fps; higher for fast behaviours), even lighting, and
  contrast between animal and arena.
- **Automated tracking:** commercial (EthoVision, ANY-maze) or open-source
  (ezTrack, Bonsai). **Pose estimation** with DeepLabCut or SLEAP tracks body
  parts; downstream tools (e.g. SimBA, B-SOiD, keypoint-MoSeq) classify behaviours.
- **Validate automated scores against blinded human scoring** on a subset
  (correlation and agreement), especially for freezing and social behaviours.
- Manual scoring: clear operational definitions written before scoring; two scorers
  on a subset; report **inter-rater reliability** (e.g. ICC or Cohen's kappa).

## 5. Analysis
- Account for repeated measures (mixed models with animal as random effect) and
  litter/cage clustering.
- Plot individual animals, not only means.
- Don't drop outliers post hoc without pre-set criteria.

## Gotchas
- Freezing thresholds in software (motion index, minimum duration) change results — validate settings per setup.
- Water-maze temperature, cue placement and swim ability (visible-platform control) confound learning.
- Sensory or motor deficits masquerade as cognitive effects; include control tests.
- All procedures need ethical approval and humane end-points.

## Verify
- [ ] Assay matches the construct; measures named cautiously.
- [ ] Habituation, time of day, experimenter and order controlled and recorded.
- [ ] Allocation randomised and scoring blinded.
- [ ] Automated scoring validated against blinded human scoring.
- [ ] Statistics handle repeated measures and clustering; reporting follows ARRIVE.

*Draft note:* habituation times and frame rates are common practice; validate them
for your apparatus and strain.
