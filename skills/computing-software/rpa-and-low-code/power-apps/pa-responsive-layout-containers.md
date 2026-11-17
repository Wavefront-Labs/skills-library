---
id: computing-software.rpa-and-low-code.power-apps.pa-responsive-layout-containers
name: pa-responsive-layout-containers
category: computing-software
field: rpa-and-low-code
product: power-apps
tags: [power-apps, pa-responsive-layout-containers]
level: practitioner
status: draft
description: "Use containers instead of absolute positions."
sources: ['https://learn.microsoft.com/en-us/power-apps/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build responsive layouts
**Goal:** Use containers instead of absolute positions.

- Horizontal and vertical containers with flexible width/height and fill portions; set app Scale-to-fit off for responsiveness.
- Use Parent.Width and Parent.Height in formulas.
- Test on phone and tablet sizes.

## Gotchas
- Mixing absolute X/Y with containers breaks layout.

## Self-check
Layout reflows correctly in the preview sizes.
