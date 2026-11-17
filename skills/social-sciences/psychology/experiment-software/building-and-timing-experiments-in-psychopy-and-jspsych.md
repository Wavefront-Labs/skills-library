---
id: social-sciences.psychology.experiment-software.building-and-timing-experiments-in-psychopy-and-jspsych
name: building-and-timing-experiments-in-psychopy-and-jspsych
category: social-sciences
field: psychology
product: experiment-software
tags: [experiment-software, psychology, psychopy, psychopy-builder, psychopy-coder, jspsych, e-prime, opensesame, gorilla, pavlovia, jatos, cognition-run, inquisit, labjs, online-experiments, timing-accuracy, frame-rate, refresh-rate, photodiode, black-box-toolkit, response-box, conditions-file, csv-data, prolific-integration, javascript, python]
level: practitioner
status: docs-checked
description: "Build computerised experiments in PsychoPy or jsPsych, deploy online via Pavlovia or JATOS, and verify stimulus and response timing instead of trusting it."
sources:
  - https://www.psychopy.org/api/visual/window.html
  - https://www.psychopy.org/api/hardware/keyboard.html
  - https://www.jspsych.org/latest/overview/timeline/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and timing experiments in PsychoPy and jsPsych

**Goal:** a task that presents the right stimuli for the right durations, records
every response with its context, and saves data you can analyse without detective work.

## 1. Pick the tool
| Tool | Strength | Notes |
|---|---|---|
| PsychoPy (Builder/Coder) | Python; Builder for most tasks, Code components for logic | Check the docs for what runs online |
| jsPsych | JavaScript library, browser-native | Host on a server or an experiment-hosting service |
| E-Prime, OpenSesame, Gorilla | Other packages | Check each vendor's licence terms |

Choose based on where it will run and who maintains it. Check early whether every
component you need works in the online version if online deployment is planned.

## 2. Structure: drive the task from a conditions file
- One CSV/XLSX row per trial type: stimulus, condition, correct response.
- PsychoPy: a `Loop` around the trial routine driven by a conditions file. jsPsych: a `timeline` with `timeline_variables` and `randomize_order: true`.
- Never hard-code stimulus lists in code; counterbalancing lists become separate files
  chosen by participant number.

## 3. Timing: specify in frames, verify with hardware
- Screens update at the refresh rate (60 Hz → 16.67 ms per frame). Durations should be
  whole frames: a 50 ms stimulus on 60 Hz is 3 frames, but 40 ms is impossible.
- Check for **dropped frames**: PsychoPy's `Window.recordFrameIntervals` records the time
  between flips so you can see whether frames are being dropped (`saveFrameIntervals()`
  saves them).
- Laboratory gold standard: a **photodiode** on the screen plus a response-timing device
  or oscilloscope. Do it once per hardware setup. Browsers add more variability than lab
  setups; test your own configuration.
- PsychoPy's `Keyboard` class supersedes `event.getKeys`: its polling is timestamped
  asynchronously from the main thread, and it uses the Psychtoolbox backend only on
  64-bit Python 3.

## 4. Data saving
- Save **every trial** immediately (e.g. to a server from your trial callbacks). Don't
  hold data only in memory until the end.
- Include participant ID, session, condition list, trial index, stimulus, onset time,
  response, RT, correctness, software version and frame rate.
- Online: pass the recruitment platform's participant ID through URL parameters and
  store it; redirect to the completion URL at the end.

## 5. Online deployment checklist
- Fullscreen request, browser check (block mobile if needed), screen-size/viewing-
  distance calibration when stimulus size matters.
- Preload media; large videos/audio stall on slow connections.
- Pilot on Chrome, Firefox, Safari and on a slow machine.
- Hosting services have licence and pricing terms: check the current ones.

## 6. Piloting
Run yourself through every condition, then 3–5 naive pilots. Analyse pilot data with the
real analysis script — that's when you discover the missing column.

## Gotchas
- PsychoPy versions change behaviour; pin the version and record it.
- Audio onset latency is worse and more variable than visual — measure it.
- Variable names in conditions files are case-sensitive and must be valid identifiers.

## Checked
2026-11-01. Confirmed: `Window.recordFrameIntervals` and `saveFrameIntervals()` (PsychoPy Window API); `Keyboard` supersedes `event.getKeys`, async timestamping, Psychtoolbox on 64-bit Python 3 (PsychoPy keyboard API); jsPsych `timeline_variables` and `randomize_order` (timeline overview). Removed: Bridges et al. timing figures, Black Box ToolKit, ExperimentHandler and jsPsych callback names, Prolific parameter names, Pavlovia/Gorilla/E-Prime licence statements, `useVersion`, loop parameter names, credit-card method.
Method: documentation only; no commands were run.

## Verify
- [ ] Stimulus durations are whole frames at the measured refresh rate.
- [ ] Timing validated with a photodiode or published benchmark matching your setup.
- [ ] Data saved per trial with all identifying and context columns.
- [ ] Pilot data run through the full analysis script.
- [ ] Software version pinned and reported.
