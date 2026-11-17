---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.paging-tooling-and-escalation-configuration
name: paging-tooling-and-escalation-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [paging-tooling, pager-escalation-config, pagerduty, opsgenie, grafana-oncall, escalation-policy, alertmanager]
level: practitioner
status: draft
description: "Configure paging: services, escalation policies, urgency rules and Alertmanager integration in PagerDuty (Terraform) or Grafana OnCall, and test that a page reaches a phone."
sources: ["https://registry.terraform.io/providers/PagerDuty/pagerduty/latest/docs", "https://prometheus.io/docs/alerting/latest/configuration/#pagerduty_config", "https://grafana.com/docs/oncall/latest/configure/escalation-chains-and-routes/", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paging tooling and escalation configuration

## Model
Service (what is broken) -> escalation policy (who, in what order, after how long) -> schedules (who is on
now) -> notification rules (how each person is reached). Alerts arrive through an integration key per
service.

## PagerDuty via Terraform
```hcl
resource "pagerduty_schedule" "primary" {
  name      = "api-primary"
  time_zone = "Europe/London"
  layer {
    name                         = "weekly"
    start                        = "2026-10-21T10:00:00+01:00"
    rotation_virtual_start       = "2026-10-21T10:00:00+01:00"
    rotation_turn_length_seconds = 604800
    users                        = [for u in data.pagerduty_user.team : u.id]
  }
}
resource "pagerduty_escalation_policy" "api" {
  name      = "api"
  num_loops = 2
  rule {
    escalation_delay_in_minutes = 10
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.primary.id
    }
  }
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.secondary.id
    }
  }
}
resource "pagerduty_service" "api" {
  name                    = "api"
  escalation_policy       = pagerduty_escalation_policy.api.id
  acknowledgement_timeout = 1800
  auto_resolve_timeout    = "null"
  incident_urgency_rule {
    type    = "constant"
    urgency = "high"
  }
}
resource "pagerduty_service_integration" "am" {
  name    = "alertmanager"
  service = pagerduty_service.api.id
  vendor  = data.pagerduty_vendor.prometheus.id
}
```

## Alertmanager receiver
```yaml
receivers:
- name: api-page
  pagerduty_configs:
  - routing_key: <events-v2 integration key>   # use routing_key (Events API v2), not service_key
    severity: '{{ .CommonLabels.severity }}'
    description: '{{ .CommonAnnotations.summary }}'
    links: [{ href: '{{ .CommonAnnotations.runbook_url }}', text: runbook }]
route:
  routes:
  - matchers: [severity="page", team="api"]
    receiver: api-page
```

## Grafana OnCall equivalent
Integration (Alertmanager) -> route (Jinja2 routing template on labels) -> escalation chain: "Notify users
from on-call schedule" -> "Wait 10m" -> "Notify schedule secondary" -> "Notify whole channel".

## Policy rules
- Only SLO-burn and imminent-harm alerts page; everything else goes to tickets (low urgency).
- Each person: push + phone call + SMS for high urgency; at least two methods.
- Escalation reaches a human with authority within 30 min.

## Test
```bash
amtool alert add alertname=PagingTest severity=page team=api --annotation=summary="test page" \
  --alertmanager.url=http://alertmanager:9093
```
Confirm the phone rings, ack works, escalation fires if unacked.

## Gotchas
- `auto_resolve_timeout` closes incidents still burning; leave it off for paging services.
- Integration keys are secrets; store in a secret manager, not in Git.
- Re-test after paging-tool user changes; deactivated users silently break escalation.

## Verify
- [ ] Monthly test page reaches primary and escalates to secondary.
- [ ] Config in Terraform, applied from CI.
