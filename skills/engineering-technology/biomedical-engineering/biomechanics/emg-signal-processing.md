---
id: engineering-technology.biomedical-engineering.biomechanics.emg-signal-processing
name: emg-signal-processing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [emg-processing, surface-emg, emg-biomechanics, linear-envelope, rms, onset-detection, median-frequency, emg-filter]
level: practitioner
status: gated
description: "Process surface EMG: band-pass, rectification, linear envelope or RMS, onset detection, spectral fatigue measures and reporting settings, with a code recipe."
sources: ["De Luca, The use of surface electromyography in biomechanics (J Appl Biomech 1997)", "Merletti and Farina, Surface Electromyography: Physiology Engineering and Applications", "Hermens et al., SENIAM recommendations (J Electromyogr Kinesiol 2000)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EMG signal processing

**Goal:** turn raw EMG into an amplitude or timing measure that you can interpret and compare.

## Pipeline
The filter corners, window lengths and thresholds below are common conventions, not checked against a primary source (gated: unconfirmed, source is paywalled or blocked).
1. **Acquire** at 1000 Hz or higher with hardware band-pass of roughly 10-500 Hz and anti-alias filtering.
2. **Band-pass** digitally, zero-lag 4th-order Butterworth about 20-450 Hz (the 20 Hz high-pass removes motion artefact; some protocols use 10 Hz). Avoid notch filters unless required, since they remove EMG energy near 50 or 60 Hz.
3. **Remove the offset** (subtract mean).
4. **Full-wave rectify.**
5. **Smooth:**
   - **Linear envelope:** low-pass at about 3-10 Hz, 4th order two-pass.
   - **RMS** over a moving window (about 50-250 ms), preferable for amplitude analysis.
6. **Normalise** (see emg-normalization) for comparing muscles and subjects.
7. **Onset and offset detection:** threshold such as baseline mean plus 3 standard deviations for a minimum duration (for example 25-50 ms); verify visually and with a double-threshold method.
8. **Spectral analysis:** Welch power spectrum; median or mean frequency falls with fatigue in sustained contractions.

## Python sketch
```python
from scipy.signal import butter, filtfilt
import numpy as np
b, a = butter(2, [20/(fs/2), 450/(fs/2)], btype='band')
emg_f = filtfilt(b, a, emg - emg.mean())
env = filtfilt(*butter(2, 6/(fs/2)), np.abs(emg_f))
```

## Gotchas
- Different smoothing changes peak values and timing; report the exact settings.
- Cross-talk and movement artefact can look like activity.
- Sampling below 1 kHz aliases high-frequency content.

## Verify
- [ ] Baseline noise measured (about 1-5 microvolts RMS).
- [ ] Rectified and enveloped signals plotted against the raw signal.
- [ ] Onsets match visual inspection in a sample of trials.
