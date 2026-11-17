---
id: computing-software.rpa-and-low-code.power-apps.pa-connection-sharing
name: pa-connection-sharing
category: computing-software
field: rpa-and-low-code
product: power-apps
tags: [power-apps, pa-connection-sharing]
level: advanced
status: draft
description: "Control whose identity data calls use."
sources: ['https://learn.microsoft.com/en-us/power-apps/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Share connections and credentials
**Goal:** Control whose identity data calls use.

- Implicit (user's own) connections versus shared embedded connections with SQL/other (confirm per connector).
- Review in the app's Data section; avoid embedding highly privileged accounts.
- Use service principals where supported.

## Gotchas
- A shared connection lets users reach data beyond the app UI through the API.

## Self-check
Users without access to the source see the expected failure.
