---
id: computing-software.ar-vr-development.openxr.interaction-profile-bindings
name: interaction-profile-bindings
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, interaction-profile-bindings]
level: practitioner
status: docs-checked
description: "Suggest bindings per controller type via interaction profiles."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suggest interaction profile bindings
**Goal:** Suggest bindings per controller type via interaction profiles.

- Call `xrSuggestInteractionProfileBindings` per profile path, for example `/interaction_profiles/khr/simple_controller` as a generic profile, plus `/interaction_profiles/oculus/touch_controller` for Touch.
- Binding paths look like `/user/hand/left/input/trigger/value`.
- Read the active profile with `xrGetCurrentInteractionProfile`; the runtime may return a profile that differs from the hardware.

## Self-check
`XrEventDataInteractionProfileChanged` fires when controllers switch.

## Checked

Date: 2026-11-02. Confirmed in the input and semantic path chapters and the Touch controller extension pages. Removed: 'runtime ignores unsuggested profiles' and the per-profile testing advice.

Method: documentation only; no commands were run.
