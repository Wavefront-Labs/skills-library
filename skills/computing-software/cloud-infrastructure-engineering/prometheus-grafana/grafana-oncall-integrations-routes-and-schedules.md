---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oncall-integrations-routes-and-schedules
name: grafana-oncall-integrations-routes-and-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-oncall, grafana-irm, oncall-alert-templates, jinja2-templates, oncall-routes, escalation-chain-steps, escalation-wait-step, schedule-rotations-web, schedule-layers, oncall-overrides, oncall-terraform-schedules, outgoing-webhooks, oncall-maintenance-mode]
level: practitioner
status: docs-checked
description: "Grafana OnCall integrations and templates, routes, escalation chain steps, schedule types (web, iCal, Terraform) and shift types."
sources: ["https://github.com/grafana/oncall/blob/dev/docs/sources/configure/integrations/_index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/configure/escalation-chains-and-routes/index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/manage/on-call-schedules/_index.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_on_call_shift.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana OnCall / IRM

## Integrations and templates
An integration is the entry point for alerts: a unique URL that accepts an HTTP POST with a JSON payload (or inbound
email), interpreted with Jinja2 templates for that monitoring system. Template kinds: routing (conditional, must output
True), appearance (title, message, image per web, Slack, MS Teams, Telegram, SMS, phone, email, push), behavioral
(grouping ID, autoresolution, auto acknowledge, source link), and integration templates (the defaults for a given
system; use a Webhook integration for systems without one). Edit them in the integration page under Templates.

## Routes and escalation chains
The first matching route wins; reorder with the arrows. A route's routing template must evaluate to True and selects an
escalation chain; Publish to ChatOps sets the channels. Chain steps: Wait, Notify users, Notify users from on-call
schedule, Notify all team members, Resolve incident automatically, Notify Slack channel members, Notify Slack user
group, Trigger outgoing webhook, Round robin, Time-based escalation, Threshold-based escalation, Repeat escalation
(loops the chain up to five times), Declare incident (Cloud only). Steps use the Default or Important personal
notification rules. Chain names are unique per organisation.

## Schedules
- Admin and Editor roles manage schedules; Viewers cannot be on call.
- Web schedules: rotations, a live preview, teammates' time zones and overrides; override events take precedence over
  rotations.
- iCal import: imported schedules are read-only in OnCall.
- Terraform: schedules and shifts managed as code are read-only in the UI. Shift `type` is `rolling_users`,
  `recurrent_event` or `single_event`; `level` sets priority (higher value, higher priority); a shift's `time_zone`
  overrides the schedule's. See grafana-oncall-terraform-integrations-and-escalation-chains for the resources.
- Shift swap requests let teammates take your shifts for a period.

## Verify
- [ ] A test alert creates one alert group, routes to the intended chain and notifies the on-call user.
- [ ] The schedule quality report shows no uncovered time.

## Checked

2026-11-08. Confirmed against the raw OnCall docs (configure/integrations, configure/jinja2-templating,
configure/escalation-chains-and-routes, manage/on-call-schedules) and the Terraform provider's oncall_on_call_shift
page. The grafana.com and registry URLs were unreadable, so repository files replaced them. Removed as unconfirmed:
example templates, the example chain with minute values, layer-precedence wording, the hand-written Terraform
example, outgoing-webhook event list, and the maintenance mode description.
Method: documentation only; no commands were run.
