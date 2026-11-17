---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-device-test-matrix
name: xr-device-test-matrix
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-store-submission-testing, xr-device-test-matrix]
level: practitioner
status: draft
description: "Cover headsets, controllers and tracking conditions."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build a device test matrix
**Goal:** Cover headsets, controllers and tracking conditions.

- List target headsets and controllers, OS versions, tracking space modes and input modes (controllers and hands).
- Test lighting extremes, guardian/boundary resizing, tracking loss and headset sleep/wake.
- Capture performance metrics per device and keep a regression baseline.

## Gotchas
- Hand tracking and passthrough break in low light; test dim rooms.

## Self-check
A matrix with pass/fail per device and per scenario exists for each release.
