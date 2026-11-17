---
id: computing-software.ar-vr-development.webxr.webxr-controllers-gamepad
name: webxr-controllers-gamepad
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-input-sources, webxr-controllers-gamepad]
level: practitioner
status: draft
description: "Use inputSources, target ray and the xr-standard gamepad mapping."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read controllers and gamepad buttons
**Goal:** Use inputSources, target ray and the xr-standard gamepad mapping.

- `session.inputSources`; `inputSource.targetRaySpace` for pointing, `gripSpace` for held objects.
- `inputSource.gamepad.buttons[0]` is trigger and `[1]` squeeze in the xr-standard mapping.
- Listen to `selectstart`, `select`, `selectend`.

## Gotchas
- Check `gamepad.mapping === 'xr-standard'`.

## Self-check
Trigger events fire for each hand.
