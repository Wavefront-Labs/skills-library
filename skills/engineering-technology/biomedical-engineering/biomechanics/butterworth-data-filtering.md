---
id: engineering-technology.biomedical-engineering.biomechanics.butterworth-data-filtering
name: butterworth-data-filtering
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [butterworth-filtering, inverse-dynamics, joint-moments, zero-lag-filter, filtfilt, residual-analysis, cutoff-frequency, motion-capture]
level: practitioner
status: gated
description: "Filter motion and force data with zero-lag Butterworth filters: cutoff selection by residual analysis, order and pass correction, padding, and consistency between signals."
sources: ["Winter, Biomechanics and Motor Control of Human Movement (signal processing chapter)", "Robertson and Dowling, Design and responses of Butterworth and critically damped digital filters (J Electromyogr Kinesiol 2003)", "Kristianslund, Krosshaug and van den Bogert, Effect of low-pass filtering on joint moments from inverse dynamics (J Biomech 2012)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Butterworth filtering of biomechanical data

**Goal:** remove noise without distorting the signal, and filter all channels consistently before inverse dynamics.

## Method
1. Use a low-pass Butterworth (maximally flat) of 2nd to 4th order applied **forwards and backwards** for zero phase lag. Two passes square the magnitude response, so the effective cutoff is lower than the design cutoff; correct for it or specify the effective cutoff. Computed with SciPy: a 2nd-order design run forwards and backwards (effective 4th order) has its -3 dB point at about 0.80 of the design cutoff; a 4th-order design run twice has it at about 0.90 (analytic (sqrt2 - 1)^(1/2N): 0.802 for N=2, 0.896 for N=4).
2. **Cutoff selection:** residual analysis (Winter): filter at many cutoffs, plot the RMS residual versus cutoff, extrapolate the linear noise region back to zero frequency to find the cutoff where the residual equals the noise.
3. Typical cutoffs for walking: markers 6-10 Hz; force plates often similar or higher; running requires higher (about 12-20 Hz or more) (literature conventions (gated: unconfirmed, source is paywalled or blocked)).
4. **Same cutoff** for kinematics and force in inverse dynamics, as unequal filtering creates artificial impact peaks (see Kristianslund et al.).
5. **Padding** the ends (reflection or extrapolation) to reduce edge transients, then trim.
6. Sampling rate at least 2 times the highest frequency of interest (for gait, 100 Hz for markers; 1000 Hz for force plates and EMG are common practice (gated: unconfirmed, source is paywalled or blocked)).

## Python example
```python
from scipy.signal import butter, filtfilt
fs, fc, order = 100.0, 6.0, 2          # filtfilt doubles the effective order
b, a = butter(order, fc/(fs/2), btype='low')
y = filtfilt(b, a, x, padtype='odd', axis=0)
```
SciPy's `filtfilt` is two-pass, so the effective -3 dB cutoff is below `fc`; confirm with the frequency response.

## Gotchas
- Do not filter data with gaps; fill with spline interpolation first and flag it.
- Low-pass filtering reduces peak values (impact peaks); report the filter.
- Filtering Euler angles that wrap by 360 degrees.

## Verify
- [ ] Plot raw and filtered signals; check peak change.
- [ ] Residual analysis plot saved.
- [ ] Filter specification recorded in the methods.
