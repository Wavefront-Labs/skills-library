---
id: computing-software.ar-vr-development.openxr.eye-gaze-interaction
name: eye-gaze-interaction
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, eye-gaze-interaction]
level: advanced
status: docs-checked
description: "Read gaze as a pose action with XR_EXT_eye_gaze_interaction."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use eye gaze interaction
**Goal:** Read gaze as a pose action with XR_EXT_eye_gaze_interaction.

- Binding path `/user/eyes_ext/input/gaze_ext/pose`; create a pose action and an action space.
- The extension page calls eye tracking data sensitive personal information and says a runtime may have a permission system and a calibration routine; handle an uncalibrated tracker.

## Self-check
The pose action is active and its space can be located.

## Checked

Date: 2026-11-02. Confirmed in the XR_EXT_eye_gaze_interaction page: binding path, sensitivity note, permission system, calibration. Removed: the 'few degrees' accuracy check and the pointer to other skills.

Method: documentation only; no commands were run.
