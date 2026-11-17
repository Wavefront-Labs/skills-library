---
id: natural-sciences.ecology.behavioural-ecology.focal-sampling-and-ethogram-design
name: focal-sampling-and-ethogram-design
category: natural-sciences
field: ecology
product: behavioural-ecology
tags: [behavioural-ecology, behavioral-ecology, animal-behaviour, animal-behavior, ethology, ethogram, focal-animal-sampling, focal-sampling, scan-sampling, instantaneous-sampling, one-zero-sampling, all-occurrences-sampling, ad-libitum-sampling, behavioural-states, behavioural-events, time-budget, inter-observer-reliability, cohens-kappa, boris, jwatcher, video-coding, observer-effects, habituation, altmann-1974, primate-behaviour, bird-behaviour, field-observation]
level: practitioner
status: draft
description: "Design an ethogram and collect behaviour data with focal-animal, scan and all-occurrences sampling: definitions, states vs events, sampling intervals, observer reliability."
sources: ["J. Altmann, Observational study of behavior: sampling methods, Behaviour 49 (1974) 227", "M. Bateson & P. Martin, Measuring Behaviour: An Introductory Guide (4th ed., 2021)", "O. Friard & M. Gamba, BORIS, Methods Ecol. Evol. 7 (2016) 1325"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Focal sampling and ethogram design

**Goal:** behavioural data (time budgets, rates, sequences) that answer a defined
question, are repeatable by another observer, and don't carry hidden sampling biases.

## 1. Start from the question
"Do dominant individuals feed longer?" needs per-individual durations of feeding;
"How vigilant is the group at dusk?" needs group-level proportions over time. The
question decides the sampling rule, the recording rule, and which behaviours belong in
the ethogram.

## 2. Build the ethogram
- Do **ad libitum pilot observations** (hours to days) to list what the animals do.
- For each behaviour write: name, code, an **operational definition** (observable
  movements/postures, not intentions — "head below shoulder height, muzzle in vegetation"
  not "looking for food"), start and end criteria, and whether it is a:
  - **State** — has meaningful duration (resting, foraging): measure duration/proportion.
  - **Event** — instantaneous (alarm call, bite): measure frequency/rate.
- States within a category should be **mutually exclusive and exhaustive** (include
  "out of sight" and "other").
- Keep it as small as the question allows; observers can reliably track ~10–20 codes.

## 3. Sampling rules (who to watch) — after Altmann 1974
- **Focal-animal sampling:** follow one individual for a fixed period (e.g. 10–20 min),
  recording all its behaviour; rotate through individuals in a pre-set randomised order
  balanced across time of day. The gold standard for individual-level questions.
- **Scan sampling:** at fixed intervals, record the behaviour of every visible individual
  in the group. Good for group time budgets; biased toward conspicuous behaviours/individuals.
- **All-occurrences sampling:** record every occurrence of specific rare, conspicuous
  events in the whole group (fights, copulations).
- **Ad libitum:** whatever is noticed; fine for pilots and anecdotes, biased for analysis.

## 4. Recording rules (how to record)
- **Continuous recording:** exact start/stop of states and every event — most accurate;
  easiest with software (BORIS, JWatcher, phone apps) or video.
- **Instantaneous (point) sampling:** state at each sample point (e.g. every 30 s) —
  estimates proportion of time; interval must be short relative to bout lengths.
- **One–zero sampling:** did it occur in the interval? Biased; avoid for durations or rates.

## 5. Reliability and bias
- Train observers on video until **inter-observer agreement** is high (Cohen's κ
  ≳ 0.8 per behaviour, or ICC for continuous measures); recheck mid-season for drift.
- Habituate animals; record observer distance; note if the animal reacted to you.
- Record "out of sight" time and exclude it from denominators; a focal animal visible only
  while active biases toward activity.
- Blind the observer to treatment/group where possible (e.g. coding video without labels).

## Analysis notes
- Repeated focal follows of the same individual are not independent: use mixed models with
  individual as a random effect, rates with observation time as an offset.
- Proportions from instantaneous samples are compositional (sum to 1).

## Gotchas
- Definitions drift during a season; keep the written ethogram with the data and version it.
- Choosing focal animals "when they're easy to find" biases toward bold or central individuals.
- *Uncertainty note:* the κ threshold and code-count guidance are conventions, not rules;
  report the actual reliability values.

## Verify
- [ ] Every behaviour has an operational definition with start/end criteria.
- [ ] States are mutually exclusive and exhaustive, including out-of-sight.
- [ ] Sampling and recording rules stated and matched to the question.
- [ ] Focal order randomised and balanced across individuals and times.
- [ ] Inter-observer reliability measured and reported.
