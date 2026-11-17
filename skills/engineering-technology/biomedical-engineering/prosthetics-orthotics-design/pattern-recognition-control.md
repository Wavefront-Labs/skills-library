---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.pattern-recognition-control
name: pattern-recognition-control
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [pattern-recognition, upper-limb-prosthesis, myoelectric, upper-limb-prosthetics, emg-classification, lda, hudgins-features, controller-delay]
level: advanced
status: gated
description: "Design pattern-recognition control for myoelectric prostheses: electrode layout, feature sets, classifiers, window and delay, training, robustness and clinical validation."
sources: ["Hudgins, Parker and Scott, A new strategy for multifunction myoelectric control (IEEE Trans Biomed Eng 1993)", "Englehart and Hudgins, A robust real-time control scheme for multifunction myoelectric control (IEEE Trans Biomed Eng 2003)", "Scheme and Englehart, Electromyogram pattern recognition for control of powered upper-limb prostheses: state of the art and challenges for clinical use (J Rehabil Res Dev 2011)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pattern recognition control for myoelectric prostheses

**Goal:** let a user select several hand and wrist movements by contracting forearm muscles in different patterns, instead of switching with two-site control.

## Pipeline
1. **Acquisition:** 4-8 bipolar surface EMG channels (or a ring of electrodes) around the residual limb, 1 kHz or higher sampling, band-pass about 20-450 Hz (gated: unconfirmed, source is paywalled or blocked) (see emg-signal-processing).
2. **Windowing:** 150-250 ms windows with 50 ms increments (gated: unconfirmed, source is paywalled or blocked).
3. **Features:** time-domain (Hudgins) features per channel: mean absolute value, waveform length, zero crossings, slope sign changes; add autoregressive coefficients or frequency features where helpful.
4. **Classifier:** linear discriminant analysis (LDA) is the standard baseline (fast, robust, low data need); alternatives include support vector machines, neural networks and regression for proportional control.
5. **Post-processing:** majority voting or confidence thresholds to remove spurious transitions; a "no movement" class.
6. **Mapping** to prosthesis movements (hand open and close, wrist rotation, grips) and proportional speed from amplitude.

## Training
- Record several repetitions of each movement (typically 3-5 contractions of 3-5 seconds) in the socket, in different arm positions and loads to broaden the training data.
- Update (re-train) periodically; adaptive schemes retrain online from user corrections.

## Performance and limits
- **Offline accuracy** (often 90-95% in the lab) overestimates real use; **online metrics** such as the motion completion test and clinically relevant tasks matter more.
- **Controller delay:** total delay (window length plus processing) is commonly kept under about 300 ms (gated: unconfirmed, source is paywalled or blocked), and shorter is better for user perception (studies suggest the optimum is shorter than this).
- **Robustness issues:** electrode shift, sweat, arm position, load changes and muscle fatigue degrade accuracy; mitigate with training in varied conditions, electrode design, and recalibration routines.

## Clinical considerations
Targeted muscle reinnervation increases the number of independent signals; the number of controllable degrees of freedom is limited by signal quality and user training.

## Verify
- [ ] Cross-validation by session and by arm position, not random windows.
- [ ] Online task testing with the intended prosthesis.
- [ ] Failsafe behaviour (stop movement on low confidence or electrode fault).
