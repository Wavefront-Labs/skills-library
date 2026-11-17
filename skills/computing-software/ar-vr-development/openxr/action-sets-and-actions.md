---
id: computing-software.ar-vr-development.openxr.action-sets-and-actions
name: action-sets-and-actions
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-actions-and-bindings, action-sets-and-actions]
level: practitioner
status: docs-checked
description: "Describe input semantically with action sets and typed actions."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define action sets and actions
**Goal:** Describe input semantically with action sets and typed actions.

- `xrCreateActionSet`, then `xrCreateAction` with type BOOLEAN_INPUT, FLOAT_INPUT, VECTOR2F_INPUT, POSE_INPUT or VIBRATION_OUTPUT.
- Use `subactionPaths` such as `/user/hand/left` and `/user/hand/right` for one action per hand.
- Attach sets with `xrAttachSessionActionSets`; each frame call `xrSyncActions` then read state with `xrGetActionState*`.

## Gotchas
- After attach, `xrCreateAction` on an attached set and suggested bindings for its actions fail with `XR_ERROR_ACTIONSETS_ALREADY_ATTACHED`.

## Self-check
Squeezing the trigger toggles the boolean action state.

## Checked

Date: 2026-11-02. Names, action types, subaction paths and the ACTIONSETS_ALREADY_ATTACHED error confirmed in the input chapter. Reworded the post-attach rule to the documented errors.

Method: documentation only; no commands were run.
