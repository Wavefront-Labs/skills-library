---
id: computing-software.ar-vr-development.openxr.begin-end-session
name: begin-end-session
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, begin-end-session]
level: practitioner
status: docs-checked
description: "Create an XrSession whose next chain carries the graphics API binding."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a session with a graphics binding
**Goal:** Create an XrSession whose next chain carries the graphics API binding.

- Call the extension's graphics requirements function first (for example `xrGetVulkanGraphicsRequirements2KHR`), then create your device to meet it.
- Chain the binding struct (such as `XrGraphicsBindingVulkan2KHR`) into the `next` chain of `XrSessionCreateInfo`.
- Destroying a session destroys its child handles; `xrDestroySession` can be called in any session state.

## Gotchas
- Skipping the requirements call makes `xrCreateSession` fail with `XR_ERROR_GRAPHICS_REQUIREMENTS_CALL_MISSING`.

## Self-check
Session creation succeeds, and the first state event is IDLE, followed by READY when the runtime is ready.

## Checked

Date: 2026-11-02. Confirmed in the session chapter, the Vulkan enable2 extension page and the registry error codes. Fixed: the self-check said the first state event is READY; the spec says the first event is IDLE. Removed: the 'destroy swapchains and spaces first' rule (child handles are destroyed with the session).

Method: documentation only; no commands were run.
