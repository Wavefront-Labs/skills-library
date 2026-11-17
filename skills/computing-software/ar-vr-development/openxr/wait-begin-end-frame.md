---
id: computing-software.ar-vr-development.openxr.wait-begin-end-frame
name: wait-begin-end-frame
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-frame-loop, wait-begin-end-frame]
level: practitioner
status: docs-checked
description: "Structure each frame as wait, begin, render, end."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run the xrWaitFrame/BeginFrame/EndFrame loop
**Goal:** Structure each frame as wait, begin, render, end.

- `xrWaitFrame` returns `XrFrameState` with `predictedDisplayTime`, `predictedDisplayPeriod` and `shouldRender`.
- Call `xrBeginFrame`, then `xrEndFrame` with the layer list; call `xrBeginFrame` before `xrEndFrame`.
- If `shouldRender` is false, avoid heavy GPU work, skip layer rendering and omit those layers from `xrEndFrame`.

## Gotchas
- Calling `xrEndFrame` without a prior `xrBeginFrame` returns `XR_ERROR_CALL_ORDER_INVALID`; a second `xrBeginFrame` without `xrEndFrame` returns `XR_FRAME_DISCARDED`.
- A later `xrWaitFrame` blocks until the previous frame has been begun with `xrBeginFrame`.

## Self-check
Frame rate matches the display period reported by the runtime.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter. Fixed: the skill said a missing xrEndFrame stalls the next xrWaitFrame; the spec says xrWaitFrame blocks until the previous xrBeginFrame and unblocks independently of xrEndFrame. Removed: 'same display time' for xrEndFrame.

Method: documentation only; no commands were run.
