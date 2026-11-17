---
id: computing-software.cybersecurity-defensive.zitadel.audit-trail-and-event-viewer
name: audit-trail-and-event-viewer
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, audit-log, eventstore, events, siem, compliance]
level: practitioner
status: docs-checked
description: "Read ZITADEL's append-only audit trail through last changes, the console event viewer or the events API, and feed it to external systems."
sources:
  - https://zitadel.com/docs/concepts/features/audit-trail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL stores changes in an eventstore that only ever appends. Current state is computed from past events, so the audit trail is identical to the state rather than a separate log kept beside it. You can view past data in the context of the whole system at one point in time, which helps when tracing an incident from months ago.

Three ways to access it:

- Last changes: most objects in the console, such as users, organizations and projects, show their recent changes.
- Event viewer: administrators see all events across the instance and can filter them. Open the Events tab in default settings, or browse to `$CUSTOM_DOMAIN/ui/console/events`.
- Events API: everything available in the console is available through the APIs, so you can read events using a service account and process them in your own logic.

For a SOC or SIEM, ZITADEL has a guide on streaming events and audit logs to external systems.

Self-hosters can cap how far back the events APIs return data with the audit log retention limit, described in the usage control skill. A value of 0s means all events stay available.

## Checked

2026-11-08. Read the audit trail page and the usage control page (retention) in full.

Method: documentation only; no commands were run.
