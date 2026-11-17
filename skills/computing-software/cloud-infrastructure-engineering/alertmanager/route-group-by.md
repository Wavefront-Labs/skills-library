---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-group-by
name: route-group-by
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, group-by, aggregation, grouping]
level: practitioner
status: docs-checked
description: "The group_by route field: which labels batch alerts into one notification, and the special value that disables aggregation."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grouping with group_by

`group_by` lists the labels by which incoming alerts are grouped. For example, multiple alerts with `cluster=A` and `alertname=LatencyHigh` are batched into a single group and a single notification.

```yaml
route:
  receiver: team-X-mails
  group_by: ['alertname', 'cluster']
  routes:
  - matchers:
    - service="database"
    receiver: team-DB-pager
    group_by: [alertname, cluster, database]
```

Child routes inherit `group_by` unless they set their own, as the database route does above.

To aggregate by all possible labels, use the special value `...` as the sole label name:

```yaml
group_by: ['...']
```

This effectively disables aggregation entirely and passes through all alerts as-is. The reference says this is unlikely to be what you want, unless you have a very low alert volume or your upstream notification system performs its own grouping.

Route labels (the `labels` field) do not affect grouping, unlike `group_by`.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the group_by definition, the example route, inheritance, the special ... value and the route labels note. Removed: the paragraph on the overview document's cluster and alertname grouping (that page was not read).

Method: documentation only; no commands were run.
