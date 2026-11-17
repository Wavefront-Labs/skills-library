---
id: creative-arts.game-design.playtesting-and-balance.eye-tracking-and-biometrics
name: eye-tracking-and-biometrics
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, eye-tracking, biometrics, gaze, physiological-measures, games-user-research, heatmaps]
level: practitioner
status: draft
description: "Use eye tracking and biometrics in games user research: what gaze, heart rate and skin conductance can and cannot tell you, session setup, and pairing them with interviews."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eye tracking and biometrics

**Goal:** add objective signals (where players look, how aroused they are) to observation and interviews, without over-reading them.

## What the signals are
- **Eye tracking:** fixations (where gaze rests), saccades (jumps), dwell time on areas of interest, gaze paths and aggregated heatmaps. Good for HUD readability, signposting, and whether players ever see an objective marker.
- **Biometrics:** electrodermal activity (skin conductance), heart rate and variability, facial EMG, sometimes EEG. These indicate arousal or workload, not which emotion.

## Procedure
1. **Ask a specific question** ("do players notice the exit sign before the door closes?"). Gaze data without a question is a heatmap nobody can act on.
2. **Define areas of interest** on the screen in advance and the time window to analyse.
3. **Calibrate for every participant** and re-check mid-session; glasses, makeup, posture and head movement degrade quality. Discard bad-calibration sessions rather than averaging them in.
4. **Record a baseline** for biometrics (rest period) because individuals differ widely.
5. **Sync everything** to one timeline: screen capture, gaze, events, and a think-aloud or observer notes.
6. **Interview with the evidence:** replay a gaze clip and ask the player what they were doing (retrospective review).
7. **Report with caution:** small samples, state what was not measured.

## Gotchas
- Looking is not seeing, and not looking is not missing: peripheral vision exists.
- Arousal spikes are ambiguous (fear, excitement, frustration, surprise); interpret with context.
- Equipment is costly and slow to analyse; use it for specific questions, not routine tests.

## Verify
- [ ] Question and areas of interest set before sessions.
- [ ] Calibration quality checked per participant.
- [ ] Signals interpreted alongside observation or interviews.
