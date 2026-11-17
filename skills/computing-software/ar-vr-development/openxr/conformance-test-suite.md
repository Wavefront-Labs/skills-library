---
id: computing-software.ar-vr-development.openxr.conformance-test-suite
name: conformance-test-suite
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, conformance-test-suite]
level: advanced
status: draft
description: "Know what conformance means for a runtime and how to run the CTS."
sources: ['https://www.khronos.org/openxr/', 'https://registry.khronos.org/OpenXR/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand the Khronos conformance test suite
**Goal:** Know what conformance means for a runtime and how to run the CTS.

- The OpenXR CTS is published by Khronos; conformant runtimes appear on the Khronos conformant products list.
- Apps can run the CTS against a runtime to isolate runtime bugs from app bugs.
- File runtime bugs with a minimal repro (hello_xr from the OpenXR-SDK-Source is the usual baseline).

## Gotchas
- Conformance is per runtime version and device; do not assume it carries over.

## Self-check
hello_xr runs on the target runtime.
