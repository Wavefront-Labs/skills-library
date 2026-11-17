---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.audit-log-search
name: audit-log-search
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [audit-log-search, pv-audit]
level: practitioner
status: draft
description: Search audit data in portal or PowerShell.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Search the unified audit log
**Goal:** Search audit data in portal or PowerShell.

- Purview > Audit > New search with date range, activities and users.
- PowerShell: `Search-UnifiedAuditLog -StartDate ... -EndDate ... -Operations FileDeleted -ResultSize 5000`; or the Graph audit log query API.
- Audit (Standard) retains 180 days by default; Audit (Premium) up to a year or more (confirm).
- Verify auditing is on: `Get-AdminAuditLogConfig | fl UnifiedAuditLogIngestionEnabled`.

## Gotchas
- Events can take hours to appear.
- Mailbox auditing is on by default; verify per mailbox if in doubt.

## Self-check
Search for the action you just performed and find the row.
