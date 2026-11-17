---
id: computing-software.systems-network-administration.healthchecks.notification-integrations
name: notification-integrations
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, integrations, notification-channels, sms-quota, per-project-integrations]
level: practitioner
status: docs-checked
description: "Plan Healthchecks notification integrations: redundancy, urgency-based routing, per-project scope, per-check toggles and monthly SMS, WhatsApp and call quotas."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_notifications.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An integration is a delivery method for state-change alerts. Reasons to configure several:
- Redundancy: use two channels (for example email and Slack) so one failing does not hide the alert.
- Urgency: lighter channels for low-priority checks, more channels for critical services.
- Routing: send alerts to the right people.

Scope: each integration belongs to one project. To use it in several projects, set it up in each.

Per-check toggles: the Checks page shows which methods are active per check; click the icons to switch them. On the check details page click the "ON" / "OFF" labels.

SMS, WhatsApp and phone calls have a monthly cap that depends on the billing plan. It resets at the start of each month and unused sends do not carry over. When exceeded, a warning goes to the account's primary email and appears on the Integrations page.

Via the Management API: `GET /api/v3/channels/` lists integrations (`id`, `name`, `kind`); a check's `channels` field accepts `*` for all, comma-separated UUIDs or exact names, and on update `""` to unassign all.

Self-hosted integration settings are in config-integration-settings.

## Checked

2026-11-04. Confirmed against the Healthchecks Configuring Notifications page and the Management API v3 page: redundancy, urgency and routing reasons, per-project scope, per-check toggles, the monthly SMS, WhatsApp and call quota behaviour (resets monthly, no carry-over, warning email and Integrations page notice), the channels listing endpoint and the channels field values. Nothing removed.

Method: documentation only; no commands were run.
