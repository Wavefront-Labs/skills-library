---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-matching-and-continue
name: route-matching-and-continue
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, routing-tree, continue, root-route]
level: practitioner
status: docs-checked
description: "How an alert traverses the Alertmanager route tree: root route rules, inheritance, first-match behaviour and the continue flag."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Route tree traversal and continue

A `route` block is a node in the routing tree. Optional parameters not set on a node are inherited from its parent.

Every alert enters at the top-level route, which must match all alerts, so it must not have any matchers. It then traverses child nodes:
- If `continue` is `false` (default), traversal stops after the first matching child.
- If `continue` is `true` on a matching node, the alert keeps matching against subsequent siblings.
- If an alert matches no child of a node (none match, or none exist), it is handled with the configuration of the current node.

```yaml
route:
  receiver: default-receiver
  group_by: [cluster, alertname]
  routes:
  - receiver: database-pager
    group_wait: 10s
    matchers:
    - service=~"mysql|cassandra"
  - receiver: frontend-pager
    group_by: [product, environment]
    matchers:
    - team="frontend"
```

Alerts matching neither child stay at the root and go to `default-receiver`.

Route fields: `receiver`, `group_by`, `continue`, `matchers`, `labels`, `group_wait`, `group_interval`, `repeat_interval`, `mute_time_intervals`, `active_time_intervals` and nested `routes`. The `match` and `match_re` fields are deprecated in favour of `matchers`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): route tree traversal, inheritance, continue, deprecated match fields.

Method: documentation only; no commands were run.
