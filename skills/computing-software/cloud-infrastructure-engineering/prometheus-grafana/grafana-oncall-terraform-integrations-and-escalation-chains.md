---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oncall-terraform-integrations-and-escalation-chains
name: grafana-oncall-terraform-integrations-and-escalation-chains
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-oncall, oncall-terraform-integrations, terraform, escalation-chains, grafana-irm]
level: advanced
status: docs-checked
description: "Manage Grafana OnCall integrations, routes, escalation chains, shifts and schedules with the Grafana Terraform provider."
sources: ["https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_integration.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_escalation.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_route.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_schedule.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/oncall_on_call_shift.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana OnCall as code with Terraform

**Goal:** reproducible on-call configuration reviewed in PRs.

## Provider
With `url` and `auth` set (a Grafana service account token), the OnCall URL is derived from the IRM plugin settings.
Set `oncall_url` (or `GRAFANA_ONCALL_URL`) only when the derived URL is unreachable from where Terraform runs or when
`url`/`auth` are unset; without them the provider falls back to the us-central OnCall backend. `oncall_access_token`
(or `GRAFANA_ONCALL_ACCESS_TOKEN`) is required only for `grafana_oncall_user_notification_rule`.
```hcl
provider "grafana" {
  url  = "<GRAFANA_URL>"
  auth = var.grafana_sa_token
}
```

## Resources
```hcl
data "grafana_oncall_user" "alex" { username = "alex" }          # Grafana login, not email
data "grafana_oncall_team" "my_team" { name = "my team" }         # optional team_id on most resources

resource "grafana_oncall_on_call_shift" "weekly" {
  name          = "weekly-rotation"
  type          = "rolling_users"            # or recurrent_event, single_event
  start         = "2026-10-19T09:00:00"      # yyyy-MM-ddTHH:mm:ss
  duration      = 604800                     # seconds
  frequency     = "weekly"
  week_start    = "MO"
  rolling_users = [[data.grafana_oncall_user.alex.id]]
  time_zone     = "UTC"                      # overrides the schedule time zone
}

resource "grafana_oncall_schedule" "primary" {
  name      = "primary"
  type      = "calendar"                     # or web, ical
  time_zone = "UTC"
  shifts    = [grafana_oncall_on_call_shift.weekly.id]
}

resource "grafana_oncall_escalation_chain" "default" { name = "default" }

resource "grafana_oncall_escalation" "notify_oncall" {
  escalation_chain_id          = grafana_oncall_escalation_chain.default.id
  type                         = "notify_on_call_from_schedule"
  notify_on_call_from_schedule = grafana_oncall_schedule.primary.id
  position                     = 0         # starts from 0
}
resource "grafana_oncall_escalation" "wait" {
  escalation_chain_id = grafana_oncall_escalation_chain.default.id
  type                = "wait"
  duration            = 300                # 60-86400 seconds
  position            = 1
}

resource "grafana_oncall_integration" "am" {
  name = "alertmanager"
  type = "alertmanager"
  default_route { escalation_chain_id = grafana_oncall_escalation_chain.default.id }
}

resource "grafana_oncall_route" "critical" {
  integration_id      = grafana_oncall_integration.am.id
  escalation_chain_id = grafana_oncall_escalation_chain.default.id
  routing_type        = "jinja2"             # default is regex
  routing_regex       = "{{ payload.commonLabels.severity == 'critical' }}"
  position            = 0
}
```
`grafana_oncall_integration.am.link` is the URL to configure in the monitoring tool.

## Notes
- `routing_regex` is a Python regex by default; use `routing_type = "jinja2"` for a Jinja template.
- `important = true` on an escalation step activates the important personal notification rules (valid for the notify
  step types only).
- Escalation `type` values include wait, notify_persons, notify_person_next_each_time, notify_on_call_from_schedule,
  notify_next_on_call_from_schedule, trigger_webhook, notify_user_group, resolve, notify_whole_channel,
  notify_if_time_from_to, notify_if_num_alerts_in_window, repeat_escalation, notify_team_members, declare_incident.
- `grafana_oncall_integration` accepts a `templates` block (for example `grouping_key`, `resolve_signal`,
  `acknowledge_signal`, `source_link`, and per-channel `slack`/`web`/`sms` blocks), plus `labels` and `dynamic_labels`.
- The `web` schedule type has no shifts; `enable_web_overrides` enables UI overrides and ignores `ical_url_overrides`.
- Every OnCall resource page documents `terraform import <resource>.name "{{ id }}"`.

## Verify
- [ ] `terraform plan` is clean after apply; a test alert to the integration `link` follows the chain.

## Checked

2026-11-08. Confirmed against the provider docs in the terraform-provider-grafana repository (docs/index.md and the
oncall_integration, oncall_escalation, oncall_escalation_chain, oncall_route, oncall_schedule, oncall_on_call_shift
resources, oncall_user and oncall_team data sources). Registry URLs returned empty pages, so the repository files
replaced them in `sources`. Fixed: the route example needed `routing_type = "jinja2"`; removed the invented
`oncall_access_token` as general auth requirement, the fixed OnCall URL, the SSO/SCIM and notification-rule practices.
Method: documentation only; no commands were run.
