---
id: computing-software.qa-testing-engineering.exploratory-testing.exploratory-session-recording-and-annotation
name: exploratory-session-recording-and-annotation
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [session-recording, screen-recording, exploratory-testing, bug-evidence, test-notes]
level: practitioner
status: docs-checked
description: "Capture exploratory sessions with recording and annotation: desktop recorders, Android adb screenrecord, timestamped notes and privacy rules."
sources:
  - https://www.satisfice.com/download/session-based-test-management
  - https://developer.android.com/tools/adb#screenrecord
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing sessions with recording and annotation tools

**Goal:** never lose the steps to a hard-to-reproduce bug, and make session notes faster and richer. Session-based test management (James and Jon Bach) manages testing by activity (sessions) rather than by artifacts; recordings and timestamped notes are the evidence a session leaves behind.

## Recording options
- **Desktop:** use a screen recorder that can run for the whole session (OBS Studio is a free option; its Quick Start Guide advises running a test recording for a few minutes to check settings before the real one, and settings live under Settings > Output). The operating system's built-in screen capture also works.
- **Browser:** capture video plus console and network logs with the bug report where your tooling allows it, or reproduce with a scripted trace afterwards.
- **Android:** `adb shell screenrecord /sdcard/demo.mp4` records the display on Android 4.4 (API level 19) and higher to an MPEG-4 file. Stop with Control+C; otherwise it stops automatically at three minutes, the default and maximum of `--time-limit` (180 seconds). Then `adb pull` the file to the host. For longer sessions record in several files.
- **iOS:** use the built-in screen recording, or a cabled device with a desktop recorder for long sessions.

## Annotation and notes
- Use a note template with timestamps so entries line up with the recording.
- Mark moments: say or type "BUG" with the time; take annotated screenshots.
- Attach short clipped segments to bug reports, not the whole session.

## Privacy and storage
- Do not record real customer data or credentials; use test accounts and silence notifications.
- Store recordings with retention rules; delete raw session videos after the bug is resolved unless needed for audit.

## Verify
Bugs found in sessions carry a short clip or trace showing the reproduction, and session notes have timestamps that match the recording.

## Checked
2026-11-09. Confirmed in the Android adb page (screenrecord: Android 4.4/API 19+, MPEG-4, Control+C, three-minute default and maximum, --time-limit 180), the OBS Quick Start Guide (test recording advice, Settings > Output) and the satisfice SBTM page (activity-based management). Removed: OBS replay-buffer instructions, Windows/macOS shortcuts, named browser extensions and note tools, the "Show taps" tip, 10-60 s clip length, Playwright trace claim (not read this batch).
Method: documentation only; no commands were run.
