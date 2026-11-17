---
id: computing-software.rpa-and-low-code.power-apps.pa-onstart-named-formulas
name: pa-onstart-named-formulas
category: computing-software
field: rpa-and-low-code
product: power-apps
tags: [power-apps, pa-canvas-basics, pa-onstart-named-formulas]
level: practitioner
status: draft
description: "Initialise efficiently with named formulas."
sources: ['https://learn.microsoft.com/en-us/power-apps/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use App.Formulas and OnStart wisely
**Goal:** Initialise efficiently with named formulas.

- App.OnStart runs before the first screen; heavy work delays launch. Prefer App.Formulas (named formulas) which evaluate lazily.
- Use StartScreen to choose the first screen without Navigate in OnStart.
- Keep OnStart short.

## Gotchas
- Long OnStart is a top cause of slow app startup.

## Self-check
App Checker shows no OnStart warnings.
