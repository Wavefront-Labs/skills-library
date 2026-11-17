---
id: computing-software.cloud-infrastructure-engineering.datadog.incident-management
name: incident-management
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, incident-management, incidents, oncall, postmortems]
level: practitioner
status: docs-checked
description: "Declare and manage incidents in Datadog with severity, commander, timeline, tasks and postmortems."
sources: ["https://docs.datadoghq.com/incident_response/incident_management/", "https://docs.datadoghq.com/incident_response/incident_management/investigate/declare/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident Management
Goal: run incidents consistently.

```
# Declare from Slack (Datadog Slack integration enabled)
/datadog incident

# Declare automatically from a monitor
Monitor > Configure notifications and automations > Add Incident > pick an @incident-<name> option
```

- Declaration modal: title (required), severity (required; SEV-1 most severe to SEV-5 least by default, customisable in Incident Settings) and incident commander. Settings can add or require more fields.
- Ways to declare: the Incidents page (Declare Incident), a monitor, a security signal, a Synthetic test, a graph, a Datadog On-Call page, Slack, and others.
- A monitor can create an incident when it moves to `warn`, `alert` or `no data`. Admins create the `@incident-` options in Incident Settings. Incidents created this way inherit field values from the monitor's tags, which also lets notification rules match them.
- Slack declaration creates an incident channel. If the declarer has connected Slack to their Datadog account they become incident commander; otherwise it is a generic `Slack app user` that can be reassigned.
- Search syntax examples: `severity:SEV-1`, `severity:(SEV-1 OR SEV-2) state:active`, `teams:platform`.
- Incident Analytics tracks measures such as time to resolution and customer impact, queried in dashboards and notebooks.
- Integrations: Datadog On-Call, Status Pages, Notebooks for postmortems, Workflow Automation; third party Slack, Microsoft Teams, Jira, ServiceNow, PagerDuty, OpsGenie, Confluence, Atlassian Statuspage and webhooks.

Gotcha: a monitor that auto-declares on every `warn` or `no data` transition will create incidents for each; choose which monitors carry an `@incident-` option deliberately.

## Verify
- Declare a test incident and confirm the severity, commander and (from Slack) the incident channel appear.

## Checked
2026-11-09. Confirmed against the Incident Management overview and Declare an incident pages (modal fields, default severities, declaration sources, monitor automatic declaration states and Add Incident path, tag inheritance, Slack command and commander rules, search examples, analytics, integrations list). Removed: the `{{#is_alert}}` message wrapper and the example handle name, "timeline gathers monitors, graphs and notes" and task assignment (not read on these pages), postmortem template detail, the On-Call availability hedge, and the game-day, severity-definition, status-update and follow-up-owner advice.
Method: documentation only; no commands were run.
