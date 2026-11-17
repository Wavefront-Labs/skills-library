---
id: computing-software.rpa-and-low-code.uipath.uipath-in-out-arguments
name: uipath-in-out-arguments
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-in-out-arguments]
level: practitioner
status: draft
description: "Reuse workflows with typed arguments."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pass data with In, Out and In/Out arguments
**Goal:** Reuse workflows with typed arguments.

- Invoke Workflow File with the Import Arguments dialog; direction In, Out or In/Out.
- Prefer dictionaries or small typed arguments over many scalars; do not mutate In arguments.
- Unit-test the workflow with a test case.

## Gotchas
- Argument names are case-sensitive in the invoke mapping.

## Self-check
The called workflow returns the expected Out values.
