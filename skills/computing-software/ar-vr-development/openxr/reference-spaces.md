---
id: computing-software.ar-vr-development.openxr.reference-spaces
name: reference-spaces
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-spaces-and-poses, reference-spaces]
level: practitioner
status: docs-checked
description: "Choose VIEW, LOCAL or STAGE and create the matching XrSpace."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create reference spaces
**Goal:** Choose VIEW, LOCAL, LOCAL_FLOOR or STAGE and create the matching XrSpace.

- `XR_REFERENCE_SPACE_TYPE_VIEW` tracks the viewer and is not gravity-aligned; use it for small head-locked content, and `xrLocateViews` for rendering.
- `LOCAL` is a world-locked, gravity-aligned origin; `STAGE` is a runtime-defined flat rectangular space with its origin on the floor.
- OpenXR 1.1 adds `XR_REFERENCE_SPACE_TYPE_LOCAL_FLOOR`.
- Create with `xrCreateReferenceSpace`, passing a `poseInReferenceSpace`.

## Gotchas
- Some systems support no STAGE space; fall back to LOCAL or LOCAL_FLOOR.

## Self-check
Floor-height objects line up in both LOCAL_FLOOR and STAGE.

## Checked

Date: 2026-11-02. Confirmed in the spaces chapter and registry. Removed: 'seated origin' wording, the identity-pose rule and the manual height-offset advice.

Method: documentation only; no commands were run.
