---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.impedance-pneumography
name: impedance-pneumography
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [impedance-pneumography, respiration-monitoring, thoracic-impedance, respiratory-rate, bioimpedance-respiration]
level: advanced
status: gated
description: "Measure respiration by thoracic impedance: electrode placement, carrier frequency and current limits, signal processing, motion and cardiac artefact, and accuracy limits."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design (respiration chapter)", "IEC 60601-1 patient auxiliary current limits (confirm edition and values)", "https://www.iec.ch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Impedance pneumography

**Goal:** derive respiratory rate (and sometimes tidal trends) from the change in thoracic impedance during breathing using ECG electrodes.

## Principle
- A small high-frequency current is passed across the chest; breathing changes the volume of air and the impedance between the electrodes by a small amount (of the order of a fraction of an ohm up to an ohm or so on top of a baseline of tens of ohms; confirm for your configuration).
- Typical carrier frequencies are tens of kilohertz (for example 30 to 100 kHz) (gated: unconfirmed, source is paywalled or blocked), well above physiological signals, which allows synchronous demodulation (see lock-in-demodulation).

## Safety
- Patient auxiliary current must stay within limits in the general standard; limits rise with frequency above 1 kHz up to a ceiling in the milliampere range (confirm values and measurement method in your edition). Keep the carrier current in the tens of microamps to a few hundred microamps in practice.
- Interaction with pacemakers and implanted devices must be considered; the injected current can be mistaken for sensing; check with the pacemaker industry guidance and warn in labelling.

## Signal processing
1. Demodulate, band-pass (about 0.1 to 1 Hz or wider for neonates) and detect breaths (peak detection with adaptive threshold).
2. Reject motion and cardiac-related impedance changes (cardiogenic artefact) by filtering or adaptive methods.
3. Quality index to suppress implausible rates; apnea detection is sensitive to artefact, so alarm design needs care (see alarm-priority-and-signals).

## Verify
- [ ] Current levels measured and within patient auxiliary limits.
- [ ] Rate accuracy against capnography or airflow reference including motion.
- [ ] Failure to detect apnoea evaluated in the risk file.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
