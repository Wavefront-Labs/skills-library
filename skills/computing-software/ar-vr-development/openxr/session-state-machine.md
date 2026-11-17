---
id: computing-software.ar-vr-development.openxr.session-state-machine
name: session-state-machine
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-session-lifecycle, session-state-machine]
level: practitioner
status: docs-checked
description: "Drive begin and end of the session from xrPollEvent state changes."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handle the session state machine
**Goal:** Drive begin and end of the session from xrPollEvent state changes.

- Poll `xrPollEvent` and handle `XrEventDataSessionStateChanged`.
- States: IDLE, READY, SYNCHRONIZED, VISIBLE, FOCUSED, STOPPING, LOSS_PENDING, EXITING.
- On READY call `xrBeginSession` with the primary view configuration type; on STOPPING stop the frame loop and call `xrEndSession`; on EXITING release resources and call `xrDestroySession`; on LOSS_PENDING call `xrDestroySession` and optionally poll `xrGetSystem` and create a new session.
- Keep submitting frames while VISIBLE (unfocused but visible) and FOCUSED; only FOCUSED sessions receive input.

## Gotchas
- Calling xrBeginSession before READY returns `XR_ERROR_SESSION_NOT_READY`.

## Self-check
The first state event for a new session is IDLE, then READY; after xrEndSession the state returns to IDLE.

## Checked

Date: 2026-11-02. Confirmed in the session chapter. Removed: 're-create the instance on loss' (spec says create a new session), and the headset-removal self-check, which is runtime-dependent.

Method: documentation only; no commands were run.
