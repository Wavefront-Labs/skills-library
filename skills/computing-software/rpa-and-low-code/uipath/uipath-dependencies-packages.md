---
id: computing-software.rpa-and-low-code.uipath.uipath-dependencies-packages
name: uipath-dependencies-packages
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-dependencies-packages]
level: practitioner
status: draft
description: "Control activity package versions."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manage dependencies and package feeds
**Goal:** Control activity package versions.

- Manage Packages shows official, Marketplace and custom feeds; pin versions in project.json and avoid auto-upgrade in production.
- Publish libraries to a feed in Orchestrator or to a local folder.
- Check conflicts when updating.

## Gotchas
- Updating activity packages can change selector behaviour; retest.

## Self-check
project.json lists the pinned versions.
