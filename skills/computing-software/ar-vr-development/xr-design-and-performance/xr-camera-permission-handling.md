---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-camera-permission-handling
name: xr-camera-permission-handling
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-camera-permission-handling]
level: practitioner
status: draft
description: "Request camera and spatial-data permissions with clear justification."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handle camera and environment-mapping permissions
**Goal:** Request camera and spatial-data permissions with clear justification.

- Request at the point of use with a purpose string; handle denial by offering a non-camera mode.
- Do not store passthrough images or room scans without consent; delete when no longer needed.
- Protect bystanders: avoid recording others in AR.

## Gotchas
- Platform review rejects apps with missing usage descriptions.

## Self-check
App behaves correctly with each permission denied and revoked.
