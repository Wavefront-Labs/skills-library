---
id: computing-software.ar-vr-development.openxr.locate-space-views
name: locate-space-views
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, locate-space-views]
level: practitioner
status: docs-checked
description: "Get head and eye poses for rendering with xrLocateViews."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locate spaces and views
**Goal:** Get head and eye poses for rendering with xrLocateViews.

- `xrLocateViews` with `XrViewLocateInfo` (view configuration type, display time, space) gives per-eye pose and fov.
- Check `viewStateFlags` for the POSITION_VALID and ORIENTATION_VALID bits before using poses.
- Build view and projection matrices from each view's pose and `XrFovf`.

## Self-check
Both eyes render with correct stereo disparity on a test cube.

## Checked

Date: 2026-11-02. Confirmed in the view configurations chapter. Removed: the symmetric-frustum and IPD remarks and the 1 m test distance.

Method: documentation only; no commands were run.
