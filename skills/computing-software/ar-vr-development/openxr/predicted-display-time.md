---
id: computing-software.ar-vr-development.openxr.predicted-display-time
name: predicted-display-time
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, predicted-display-time]
level: practitioner
status: docs-checked
description: "Locate spaces and views at the predicted display time, not the current time."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use predictedDisplayTime for poses
**Goal:** Locate spaces and views at the predicted display time, not the current time.

- Pass `frameState.predictedDisplayTime` to `xrLocateSpace` and `xrLocateViews`.
- Convert runtime time with `XR_KHR_win32_convert_performance_counter_time` or `XR_KHR_convert_timespec_time` when you need clock times.

## Self-check
A head-locked object appears stable while turning your head quickly.

## Checked

Date: 2026-11-02. Confirmed: predictedDisplayTime in XrFrameState, both time conversion extensions exist. Removed: 'run simulation after xrWaitFrame' and the judder claim.

Method: documentation only; no commands were run.
