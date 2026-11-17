---
id: computing-software.rpa-and-low-code.uipath.uipath-assets-types-folders
name: uipath-assets-types-folders
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-orchestrator-assets-credentials, uipath-assets-types-folders]
level: practitioner
status: draft
description: "Store configuration outside code."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use assets by type and folder
**Goal:** Store configuration outside code.

- Asset types: Text, Integer, Boolean, Credential, Secret (confirm current type list); scope per folder or per robot.
- Use Get Asset / Get Credential in workflows.
- Name consistently by environment.

## Gotchas
- Per-robot assets override defaults; check which one is read.

## Self-check
Changing the asset changes the next run with no republish.
