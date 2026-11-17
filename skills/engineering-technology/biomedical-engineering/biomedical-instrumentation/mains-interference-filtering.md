---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.mains-interference-filtering
name: mains-interference-filtering
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [mains-interference, signal-conditioning, biomedical-filters, notch-filter, 50-hz, 60-hz, powerline-noise, adaptive-filter, comb-filter]
level: practitioner
status: gated
description: "Remove 50 or 60 Hz interference from biosignals: root-cause fixes first, then notch, comb or adaptive filtering with ringing, phase and amplitude trade-offs."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design", "Pan and Tompkins, A real-time QRS detection algorithm (IEEE Trans Biomed Eng 1985, for filtering context)", "Widrow et al., Adaptive noise cancelling: principles and applications (Proc IEEE 1975)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mains (powerline) interference filtering

**Goal:** get a clean ECG, EMG or EEG trace with the least distortion of the signal's own frequency content.

## Fix the source first
1. Check electrode impedance and imbalance (see skin-electrode-impedance) and lead shielding.
2. Use a driven right leg or similar common-mode feedback; twist and shorten leads.
3. Keep patient and cables away from mains cords and fluorescent fixtures; use isolated power for the patient side.
4. Ensure the device ground is solid and the chassis is shielded.

## Filtering options
- **Analog notch** (twin-T) before the ADC prevents saturation, but good Q needs matched components and drifts.
- **Digital IIR notch** at 50 or 60 Hz: simple, narrow, low delay; it rings after transients (a QRS), adding ripple; use a narrow bandwidth, and avoid for diagnostic ECG where 50-60 Hz content matters.
- **Comb filter** removes harmonics (100, 150, 200 Hz) if the interference is distorted.
- **Adaptive filtering** (LMS) with a reference sine at the line frequency or a pickup reference removes interference while following amplitude and phase change; keep step size small to avoid distorting the signal.
- **Subtract-and-estimate** methods fit a sinusoid over a window and subtract it, with minimal ringing (frequency must be tracked).
- **Linear phase** FIR notch for post-processing.

## Design decisions
- Mains frequency drifts slightly (often within +/- 0.5 Hz) (gated: unconfirmed, source is paywalled or blocked); the notch must be wide enough or adaptive.
- Choose sample rate as a multiple of the line frequency to align the notch.
- Diagnostic ECG standards require retained bandwidth to 150 Hz; check what filtering is permitted (notch typically optional, not default).

## Verify
- [ ] Inject a 50 or 60 Hz test tone; show attenuation (for example 40 dB) at the target and passband change below 2 dB at 40 Hz.
- [ ] Step or QRS test shows acceptable ringing and ST distortion.
- [ ] Unfiltered trace is clean enough to need only mild filtering.
