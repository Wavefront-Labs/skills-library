---
id: computing-software.collaboration-platform-administration.google-workspace-admin.audit-investigation-tool
name: audit-investigation-tool
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [audit-investigation-tool, gws-reporting-audit]
level: advanced
status: draft
description: Search logs and act on findings.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audit logs and security investigation tool
**Goal:** Search logs and act on findings.

- Reporting > Audit and investigation: Drive, Gmail, Login, Token, Admin logs.
- Security investigation tool (Enterprise, confirm) allows actions like deleting a message or revoking a token.
- Export to BigQuery for long retention (setup in Reporting > Data integration).
- Log retention in console is limited (commonly 6 months, confirm).

## Gotchas
- Gmail log search depends on edition.
- Time ranges are in UTC for exported data.

## Self-check
Search a known login and find the log row.
