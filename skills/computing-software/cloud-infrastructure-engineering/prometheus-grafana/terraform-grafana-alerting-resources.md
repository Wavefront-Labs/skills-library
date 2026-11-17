---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.terraform-grafana-alerting-resources
name: terraform-grafana-alerting-resources
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [terraform-grafana-alerting, grafana-rule-group-terraform, grafana-terraform-provider, grafana-alerting, alerting-provisioning-files]
level: practitioner
status: docs-checked
description: "Manage Grafana-managed alert rules, contact points, notification policy tree, mute timings and templates with the Terraform provider."
sources: ["https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/terraform-provisioning/", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/rule_group.md", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/notification_policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform for Grafana alerting

Resources: alert rules `grafana_rule_group`, contact points `grafana_contact_point`, notification templates
`grafana_message_template`, the policy tree `grafana_notification_policy`, mute timings `grafana_mute_timing`. Auth with
a service account token that has the Alerting provisioning role (`fixed:alerting.provisioning.*`); the guide uses
provider version `>= 4.47.0`. `grafana_rule_group` requires Grafana 9.1.0 or later.

## Rule group
```hcl
resource "grafana_rule_group" "api" {
  name             = "api-alerts"
  folder_uid       = grafana_folder.alerts.uid
  interval_seconds = 60                       # all rules in the group evaluate sequentially at this interval
  rule {
    name      = "API error ratio high"
    condition = "C"                           # ref_id of the node used as the condition
    for       = "5m"
    labels      = { severity = "page" }
    annotations = { summary = "Error ratio high" }
    data {
      ref_id         = "A"
      datasource_uid = var.prometheus_uid
      relative_time_range { from = 600, to = 0 }
      model = jsonencode({ expr = "<PROMQL>", refId = "A" })
    }
    data {
      ref_id         = "B"
      datasource_uid = "__expr__"             # expression stage
      relative_time_range { from = 0, to = 0 }
      model = jsonencode({ type = "reduce", expression = "A", reducer = "last", refId = "B" })
    }
    data {
      ref_id         = "C"
      datasource_uid = "__expr__"
      relative_time_range { from = 0, to = 0 }
      model = jsonencode({ type = "math", expression = "$B > 0.05", refId = "C" })
    }
  }
}
```
Rule options from the schema: `no_data_state` (OK, NoData, KeepLast, Alerting; default NoData), `exec_err_state` (OK,
Error, KeepLast, Alerting; default Alerting), `keep_firing_for`, `is_paused`. `notification_settings` (Grafana 10.4+,
needs the `alertingSimplifiedRouting` feature flag) overrides the policy tree: exactly one of `contact_point` or
`policy`; with `policy`, set it to a routing tree's `metadata.uid`.

## Notification resources
- `grafana_notification_policy` is a single resource for the whole tree: provisioning it overwrites all policies in the
  tree (not the internal policies created when a rule selects a contact point directly). Do not manage it from two
  stacks.
- Multiple trees: one `grafana_apps_notifications_routingtree_v1beta1` per scope; rules opt in via
  `notification_settings.policy`, others use the default tree.
- Templates: `grafana_message_template` defines `{{ define "name" }}` blocks that a contact point uses, for example
  `message = "{{ template \"custom_email.message\" .}}"`.

## Export existing
Export a rule group, contact point, template, mute timing or the policy tree in Terraform format from Grafana, edit the
generated resource, and prefer it to writing `model` JSON by hand (the `model` blob differs per data source).

## Gotchas
- Provisioned resources are not editable in the Grafana UI unless `disable_provenance = true` on the resource.
- Resources link through `uid` values, which are generated at provisioning time: reference them, do not hard-code.

## Verify
- [ ] `terraform plan` is empty after `terraform apply`.

## Checked

2026-11-08. Confirmed against the Grafana "Use Terraform to provision alerting resources" page and the provider's
rule_group resource page (raw from terraform-provider-grafana; the registry pages were unreadable). Removed as
unconfirmed: the example PromQL and threshold-conditions model, the provisioning API export URL, and the claim that
a contact point is one resource with multiple integration blocks. The notification_policy page was not read; the
policy-tree claims come from the Grafana guide.
Method: documentation only; no commands were run.
