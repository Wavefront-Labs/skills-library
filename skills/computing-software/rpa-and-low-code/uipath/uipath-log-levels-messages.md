---
id: computing-software.rpa-and-low-code.uipath.uipath-log-levels-messages
name: uipath-log-levels-messages
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-logging-monitoring, uipath-log-levels-messages]
level: practitioner
status: draft
description: "Write useful logs."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log with levels and fields
**Goal:** Write useful logs.

- Log Message activity with Trace, Info, Warn, Error and Fatal levels; Orchestrator stores Robot logs and exports to Elasticsearch or similar.
- Add custom log fields for transaction IDs.
- Never log personal data or secrets.

## Gotchas
- Verbose logging slows jobs and fills storage.

## Self-check
A failed run can be traced from logs by transaction ID.
