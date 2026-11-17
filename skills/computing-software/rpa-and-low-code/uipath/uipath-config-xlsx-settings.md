---
id: computing-software.rpa-and-low-code.uipath.uipath-config-xlsx-settings
name: uipath-config-xlsx-settings
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-config-xlsx-settings]
level: advanced
status: draft
description: "Use the Settings, Constants and Assets sheets."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure Config.xlsx
**Goal:** Use the Settings, Constants and Assets sheets.

- Settings for environment-specific values; Constants for fixed values; Assets sheet reads Orchestrator assets by name.
- Store the queue name, retry counts and URLs here.
- Load into a Dictionary at Init.

## Gotchas
- Keeping credentials in the file is a leak risk; use Orchestrator credential assets.

## Self-check
Changing a setting changes behaviour with no code change.
