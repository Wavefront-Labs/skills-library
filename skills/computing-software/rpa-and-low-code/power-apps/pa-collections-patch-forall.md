---
id: computing-software.rpa-and-low-code.power-apps.pa-collections-patch-forall
name: pa-collections-patch-forall
category: computing-software
field: rpa-and-low-code
product: power-apps
tags: [power-apps, pa-collections-patch-forall]
level: practitioner
status: draft
description: "Hold and write data in formulas."
sources: ['https://learn.microsoft.com/en-us/power-apps/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use collections, Patch and ForAll
**Goal:** Hold and write data in formulas.

- ClearCollect/Collect for local data; Patch to create or update; ForAll over a table, with Patch inside carefully.
- Prefer SubmitForm for forms and batch Patch with a table argument.
- Handle errors via IfError and Errors().

## Gotchas
- ForAll is not a loop with sequential guarantees.

## Self-check
Records saved and errors displayed to the user.
