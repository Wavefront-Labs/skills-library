---
id: computing-software.ar-vr-development.openxr.haptic-output
name: haptic-output
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, haptic-output]
level: practitioner
status: docs-checked
description: "Trigger vibration through a VIBRATION_OUTPUT action."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Send haptic feedback
**Goal:** Trigger vibration through a VIBRATION_OUTPUT action.

- Create the action, bind to `/user/hand/left/output/haptic`, and call `xrApplyHapticFeedback` with `XrHapticVibration` (duration, frequency, amplitude).
- Use `xrStopHapticFeedback` to cancel; `XR_FREQUENCY_UNSPECIFIED` leaves the frequency to the runtime.

## Gotchas
- Amplitude is between 0.0 and 1.0.

## Self-check
Controller vibrates on grab.

## Checked

Date: 2026-11-02. Confirmed in the input and semantic path chapters. Removed: the battery-drain claim.

Method: documentation only; no commands were run.
