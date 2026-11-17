---
id: languages-linguistics.linguistics.praat.formant-pitch-measurement-and-textgrid-scripting
name: formant-pitch-measurement-and-textgrid-scripting
category: languages-linguistics
field: linguistics
product: praat
tags: [praat, acoustic-phonetics, phonetics, spectrogram, wideband, narrowband, formants, f1, f2, formant-tracking, burg, maximum-formant, pitch, f0, pitch-floor, pitch-ceiling, octave-jumps, intensity, duration, vot, textgrid, annotation, segmentation, praat-scripting, batch-measurement, vowel-space, mfa, forced-alignment]
level: practitioner
status: draft
description: "Measure formants, pitch and duration in Praat: spectrogram settings, formant and pitch-range calibration to avoid tracking errors, TextGrid annotation, and a script to batch-extract measurements."
sources: ["Boersma & Weenink, Praat manual (praat.org)", "Styler, Using Praat for Linguistic Research (open guide)", "Ladefoged, Phonetic Data Analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Praat — formants, pitch and TextGrid scripting

**Goal:** get trustworthy acoustic measurements (vowel formants, F0, durations) from
recordings, annotated in TextGrids and extracted by script so the numbers are
reproducible.

## 1. Open and view
- `Open › Read from file…` → select the Sound → **View & Edit**.
- Spectrogram settings (`Spectrogram › Spectrogram settings…`): view range
  **0–5000 Hz** for vowels (raise to 8000+ for fricatives); window length
  **0.005 s** (wideband, shows formants and glottal pulses) vs ~0.03 s (narrowband,
  shows harmonics).
- Turn on `Formants › Show formants` and `Pitch › Show pitch` to see the trackers.

## 2. Calibrate the formant tracker (the main gotcha)
`Formants › Formant settings…`:
- **Maximum formant**: common defaults are **5000 Hz** for adult male voices and
  **5500 Hz** for adult female voices; children higher. Number of formants: **5**.
- Wrong settings produce tracks that jump between F1/F2 or merge F2/F3. Look at the red
  dots: if they don't sit in the dark bands, change the ceiling (try ±500 Hz) or the
  number of formants (4–6) **per speaker**, and record the setting you used.
- Measure at a **stable point** (vowel midpoint, or 20/50/80% for diphthongs and
  dynamic analysis), not at transitions.

## 3. Calibrate pitch
`Pitch › Pitch settings…`: set a **floor and ceiling** around the speaker's range —
e.g. 75–300 Hz for many male voices, 100–500 Hz for many female voices (rough
starting points; inspect the data). Wrong ranges cause **octave jumps** (halving or
doubling). Creaky voice gives unreliable F0 — exclude or flag.

## 4. Annotate with a TextGrid
- Select the Sound → `Annotate › To TextGrid…`; tier names e.g. `word segment`;
  point tiers for events (e.g. burst).
- Select Sound + TextGrid → View & Edit; click to place boundaries at zero crossings
  (`Boundary › Move to nearest zero crossing`) — consistent criteria matter more than
  the exact criterion. Write down your segmentation rules (e.g. vowel onset = first
  regular periodic cycle with F2 visible).
- For large datasets, forced alignment (e.g. Montreal Forced Aligner) produces
  TextGrids you then hand-correct.

## 5. Batch-measure by script
`Praat › New Praat script`, then (modern syntax, Praat 6.x):
```praat
sound = Read from file: "speaker01.wav"
tg = Read from file: "speaker01.TextGrid"
selectObject: sound
formant = To Formant (burg): 0, 5, 5500, 0.025, 50
writeFileLine: "out.csv", "label,start,end,dur,F1,F2"
selectObject: tg
n = Get number of intervals: 2
for i to n
    selectObject: tg
    label$ = Get label of interval: 2, i
    if label$ <> ""
        t1 = Get start time of interval: 2, i
        t2 = Get end time of interval: 2, i
        mid = (t1 + t2) / 2
        selectObject: formant
        f1 = Get value at time: 1, mid, "hertz", "linear"
        f2 = Get value at time: 2, mid, "hertz", "linear"
        appendFileLine: "out.csv", label$, ",", t1, ",", t2, ",", t2 - t1, ",", f1, ",", f2
    endif
endfor
```
- Tier 2 = segment tier here; change to match yours. `undefined` values mean the
  tracker found no formant — inspect those tokens.
- For pitch, use `To Pitch: 0, floor, ceiling` then `Get value at time: t, "Hertz",
  "linear"`. *Uncertainty:* recent Praat versions add newer pitch-command variants
  (e.g. filtered autocorrelation); check the manual for your version.
- Loop over files with `Create Strings as file list` for whole folders.

## 6. Report
State Praat version, formant ceiling and number per speaker, pitch range, measurement
point, segmentation criteria, and normalisation if comparing speakers (e.g. Lobanov
z-scores) — raw Hz differ by vocal-tract size.

## Verify
- [ ] Formant tracks visually sit on the formant bands for each speaker's settings.
- [ ] No octave jumps in pitch tracks (spot-check outliers).
- [ ] Segmentation rules written down and applied consistently.
- [ ] Script output spot-checked against manual measurements for a few tokens.
- [ ] `undefined` values investigated, not silently dropped.
