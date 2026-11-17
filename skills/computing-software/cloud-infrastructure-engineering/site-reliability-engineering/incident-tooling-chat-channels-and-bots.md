---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-tooling-chat-channels-and-bots
name: incident-tooling-chat-channels-and-bots
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, incident-management, incident-tooling, slack-incident-bot, status-page, war-room]
level: practitioner
status: draft
description: "Set up incident tooling: per-incident chat channels created by a bot, role assignment, timeline capture, status page updates, video bridge and ticket links."
sources: ["https://response.pagerduty.com/during/during_an_incident/", "https://sre.google/workbook/incident-response/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/", "https://incident.io/guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident tooling

**Goal:** declaring and running an incident takes one command, and the record builds itself.

## Components
| Need | Tool pattern |
|---|---|
| Declare | `/incident declare` slash command or button on an alert (Slack/Teams bot: Grafana IRM, PagerDuty, incident.io, FireHydrant, Rootly, or homegrown) |
| Dedicated channel | Bot creates `#inc-2026-10-18-checkout-errors`, invites on-call, posts severity, IC, links |
| Roles | Commands to assign IC, comms lead, ops lead; shown in channel topic |
| Bridge | Auto-created video link for SEV1/2 |
| Timeline | Bot captures key messages (pinned or emoji-tagged), role changes, severity changes, alerts and deploys |
| Status page | Command to post/update public status (Statuspage, Instatus) with templates |
| Stakeholder updates | Scheduled reminders for the comms lead per severity cadence |
| Follow-up | Bot creates postmortem doc from template with timeline pre-filled, tickets for action items |

## Conventions
- One channel per incident; announce in a central `#incidents` channel.
- Keep the incident channel for responders; stakeholders read the announcement/updates channel.
- Use a pinned "current status" message updated by the comms lead.
- Tag important messages (for example with a timeline emoji) to feed the postmortem.

## Readiness
- Practice the tooling in drills (Wheel of Misfortune, game days); a tool nobody has used fails at 3am.
- Ensure the tooling does not depend on the systems it monitors (separate SaaS or region; backup comms if Slack is down).

## Verify
- [ ] Test declaration in a drill creates channel, roles, bridge and postmortem doc automatically; fallback comms path documented.
