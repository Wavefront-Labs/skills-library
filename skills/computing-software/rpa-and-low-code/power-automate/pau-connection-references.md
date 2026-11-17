---
id: computing-software.rpa-and-low-code.power-automate.pau-connection-references
name: pau-connection-references
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-connection-references]
level: advanced
status: draft
description: "Move flows across environments cleanly."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use connection references and environment variables
**Goal:** Move flows across environments cleanly.

- Create flows in a solution; replace connections with connection references and parameters with environment variables.
- On import, set references to the target environment's connections.
- Use a service account for production.

## Gotchas
- Personal connections break when the owner leaves.

## Self-check
Imported flow runs under the production connection.
