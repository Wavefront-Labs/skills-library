---
id: health-medicine.neurology.eeg-systems.reading-a-routine-eeg
name: reading-a-routine-eeg
category: health-medicine
field: neurology
product: eeg-systems
tags: [neurology, eeg-systems, eeg, electroencephalography, routine-eeg, eeg-montage, bipolar-montage, referential-montage, 10-20-system, posterior-dominant-rhythm, epileptiform-discharges, spikes, sharp-waves, eeg-artifacts, phase-reversal, video-eeg, long-term-monitoring]
level: practitioner
status: draft
description: "Systematic routine-EEG read: check technical settings, background and posterior rhythm, state, epileptiform vs benign variants, artifacts, and a report that answers the question."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading a routine EEG

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** read a 20–40 minute scalp EEG in the same order every time, so you don't
over-call benign variants as epileptiform — the most common and harmful EEG error.

## 1. Technical check (before looking at brain waves)
- Electrodes per the **international 10–20 system**; impedances acceptable (commonly
  <5–10 kΩ) and balanced.
- Default display: **sensitivity 7 µV/mm**, **10 s/page** (30 mm/s equivalent),
  low-frequency filter 1 Hz (time constant ~0.16 s), high-frequency filter 70 Hz,
  notch filter off unless mains noise forces it (notch can disguise spikes).
- Note ECG channel, eye leads, video, activation procedures performed
  (hyperventilation 3–5 min, photic stimulation), and medications/sleep deprivation.

## 2. Montages
- **Longitudinal bipolar ("double banana")**: localise by **phase reversal** — two
  adjacent channels deflect in opposite directions around a shared electrode.
- **Transverse bipolar**: catches midline and lateral activity.
- **Referential (average or ear)**: amplitude maximum = location; beware an "active"
  reference (ear electrode picking up temporal spikes).
Review every candidate abnormality in at least two montages.

## 3. Background, in order
1. **Posterior dominant rhythm (PDR)** in relaxed wakefulness, eyes closed:
   adults ≥8.5 Hz, attenuates with eye opening, symmetric within ~50% amplitude.
2. Anterior beta (enhanced by benzodiazepines/barbiturates).
3. **Slowing:** focal (suggests structural lesion) vs generalised (encephalopathy);
   continuous vs intermittent; theta vs delta.
4. **Sleep:** vertex waves, spindles, K-complexes — their presence and symmetry.
5. Reactivity to eye opening, voice, noxious stimuli (critical in ICU studies).

## 4. Epileptiform discharges
True spikes (<70 ms) and sharp waves (70–200 ms) usually: stand out from background,
are asymmetric/peaky, have an **aftergoing slow wave**, disrupt the background, and
have a physiological field (spread to neighbouring electrodes).
Generalised 3 Hz spike-and-wave with hyperventilation → absence epilepsy; generalised
polyspike-wave → juvenile myoclonic epilepsy; centrotemporal spikes → self-limited
childhood epilepsy.

## 5. Benign variants — do not over-call
Wicket spikes, small sharp spikes (BETS), 14 & 6 Hz positive bursts, 6 Hz
phantom spike-wave, rhythmic midtemporal theta of drowsiness, hypnagogic
hypersynchrony in children, mu rhythm, lambda waves.

## 6. Artifacts
Eye blinks (frontal, Fp1/Fp2), lateral eye movements (opposite polarities F7/F8),
muscle (fast, temporal), ECG (time-locked to QRS), electrode pop (single electrode, no
field), sweat (very slow), 50/60 Hz mains.

## 7. Report
Technical description → background → abnormalities (type, location, frequency,
state) → **impression** (normal/abnormal, with grading) → **clinical correlation**
that answers the referral question. State that a normal interictal EEG does not
exclude epilepsy (routine EEG sensitivity is modest; repeat, sleep-deprived, or
prolonged/video EEG improves yield).

## Gotchas
- When in doubt about a sharp transient, call it normal or "uncertain significance" —
  a false epilepsy diagnosis is costly.
- Hyperventilation-induced slowing in children is normal.
- Drowsiness in adults can look like temporal slowing.

Uncertainty note: filter, sensitivity and PDR values are typical ACNS/IFCN conventions;
vendor defaults vary.

## Verify
- [ ] Filters, sensitivity, montage and activation recorded.
- [ ] PDR frequency and reactivity stated.
- [ ] Each candidate discharge confirmed in two montages with a field.
- [ ] Benign variants and artifacts considered.
- [ ] Impression answers the clinical question.
