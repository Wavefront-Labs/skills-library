---
id: computing-software.erp-crm-administration.salesforce-administration.sf-event-monitoring-login-history
name: sf-event-monitoring-login-history
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-event-monitoring-login-history]
level: advanced
status: draft
description: "Investigate suspicious access."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Review login history and event logs
**Goal:** Investigate suspicious access.

- Login History shows 6 months of logins; export it; Event Monitoring log files (licensed) add API, report export and login events.
- Use Transaction Security policies (licensed) to alert on risky actions.
- Pipe logs into your SIEM.

## Gotchas
- Event log retention varies; confirm in Help.

## Self-check
Failed login shows in Login History with status.
