---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.graph-bulk-scripts
name: graph-bulk-scripts
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [graph-bulk-scripts]
level: advanced
status: draft
description: 'Write safe bulk scripts: CSV input, -WhatIf style dry runs, paging and logging.'
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk administration scripts with Graph
**Goal:** Write safe bulk scripts: CSV input, -WhatIf style dry runs, paging and logging.

- Import with `Import-Csv`; validate required columns first.
- Use `Get-MgUser -All` (not default 100 page) and `-Filter` server-side where possible.
- Wrap writes in try/catch and log success/failure to a CSV.
- Dry-run: output the planned change object before executing it.
- Handle throttling (HTTP 429, Retry-After); SDK retries some automatically.

## Gotchas
- `-Filter` on some properties needs `-ConsistencyLevel eventual -CountVariable c`.
- Test on a pilot subset before the full run.

## Self-check
Dry run output matches expectation for 5 sample rows before the full run.
