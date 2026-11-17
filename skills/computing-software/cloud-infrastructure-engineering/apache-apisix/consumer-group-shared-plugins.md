---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.consumer-group-shared-plugins
name: consumer-group-shared-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, consumer-group, consumer, group-id, shared-quota, admin-api]
level: practitioner
status: docs-checked
description: "Share plugin settings across APISIX consumers with consumer_groups and group_id, a shared limit-count quota via group, and consumer-over-group precedence."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/terminology/consumer-group.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer Group

Create a group with a shared rate limit:

```shell
curl http://127.0.0.1:9180/apisix/admin/consumer_groups/company_a \
-H "X-API-KEY: $admin_key" -X PUT -d '
{
    "plugins": {
        "limit-count": { "count": 200, "time_window": 60, "rejected_code": 503, "group": "grp_company_a" }
    }
}'
```

Put a consumer in it with `group_id`:

```shell
curl http://127.0.0.1:9180/apisix/admin/consumers \
-H "X-API-KEY: $admin_key" -X PUT -d '
{
    "username": "jack",
    "plugins": { "key-auth": { "key": "<API_KEY>" } },
    "group_id": "company_a"
}'
```

Rules:
- A `group_id` that matches no existing group makes the Admin API return 400.
- Group plugins merge with the consumer's own; if both define the same plugin, the consumer's setting wins (a group body "hello" and a consumer body "world" give "world").
- Across objects, the consumer's configuration takes priority over routes, plugin configs and services.

## Checked

2026-11-04: read the Consumer Group page; both curl examples, the 400 on an unknown group_id, merge behaviour, the hello/world example and consumer priority match it. Nothing removed.

Method: documentation only; no commands were run.
