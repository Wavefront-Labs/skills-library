---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.global-rule-resource
name: global-rule-resource
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, global-rules, global-plugins, admin-api, plugin-order]
level: practitioner
status: docs-checked
description: "Apply plugins to every APISIX request with a Global Rule: the global_rules Admin API call and the order global and local plugins run in each phase."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/terminology/global-rule.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global Rule

A Global Rule applies plugins to all requests, independent of any Route, Service, Consumer or Plugin Config. Rate limiting and observability plugins are common choices.

```shell
curl -X PUT http://{apisix_listen_address}/apisix/admin/global_rules/1 \
  -H "X-API-KEY: $admin_key" \
  -H 'Content-Type: application/json' \
  -d '{"plugins": {"limit-count": {"time_window": 60, "policy": "local", "count": 2, "key": "remote_addr", "rejected_code": 503}}}'
```

List all rules with `GET /apisix/admin/global_rules`.

Order:
- Global plugins run before locally bound plugins in the same phase: global `rewrite`, local `rewrite`, global `access`, local `access`.
- Inside each phase and scope, plugin priority decides order.
- An early response stops later handlers.

## Checked

2026-11-04: read the Global Rule page; the description, the global/local phase order, the limit-count PUT example and the list request match. Nothing removed.

Method: documentation only; no commands were run.
