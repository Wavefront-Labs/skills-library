---
id: computing-software.erp-crm-administration.salesforce-administration.sf-flow-fault-handling
name: sf-flow-fault-handling
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-flow-fault-handling]
level: advanced
status: draft
description: "Catch failures and notify admins instead of silent errors."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handle faults in flows
**Goal:** Catch failures and notify admins instead of silent errors.

- Add fault connectors to DML, action and subflow elements; log `{!$Flow.FaultMessage}` to a custom log object or send an email.
- Use Roll Back Records for screen flows to avoid partial commits.
- Monitor flow errors through the failed-flow-interview emails and Paused and Failed Flow Interviews.

## Gotchas
- Unhandled faults abort the transaction and roll back everything.

## Self-check
Forced failure writes a log record.
