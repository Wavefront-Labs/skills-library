---
id: computing-software.ar-vr-development.openxr.ext-hand-tracking
name: ext-hand-tracking
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-hand-and-eye-tracking, ext-hand-tracking]
level: advanced
status: docs-checked
description: "Track 26 joints per hand."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read hand joints with XR_EXT_hand_tracking
**Goal:** Track 26 joints per hand.

- Enable `XR_EXT_hand_tracking`, check `XrSystemHandTrackingPropertiesEXT::supportsHandTracking`.
- `xrCreateHandTrackerEXT` per hand, then `xrLocateHandJointsEXT` each frame with the display time and base space.
- Check each joint's `locationFlags` before use.

## Self-check
26 joints are returned.

## Checked

Date: 2026-11-02. Confirmed in the XR_EXT_hand_tracking page (26 joints, supportsHandTracking, locationFlags, create/locate functions). Removed: tracking-cone fade advice and the palm/tips self-check.

Method: documentation only; no commands were run.
