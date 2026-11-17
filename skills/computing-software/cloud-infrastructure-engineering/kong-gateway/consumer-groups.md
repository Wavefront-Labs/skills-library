---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.consumer-groups
name: consumer-groups
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, consumer-groups, group-precedence, consumer-group-scoping, plugins, consumers]
level: practitioner
status: docs-checked
description: "Kong Consumer Groups: a core entity since 3.4, create via /consumer_groups/, scope plugins to a group, and alphabetical precedence when a Consumer is in several groups."
sources:
  - https://developer.konghq.com/gateway/entities/consumer-group/
  - https://developer.konghq.com/gateway/entities/plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer groups

Consumer Groups organise Consumers so one configuration (such as a rate limit or transformation) applies to the whole group.

Create one:

```bash
curl -i -X POST http://localhost:8001/consumer_groups/ \
  --header "Content-Type: application/json" \
  --data '{"name": "<GROUP_NAME>"}'
```

A Consumer can belong to multiple groups.

Plugin scoping: a plugin instance can be scoped to a Consumer Group, and a separate instance is created for each group. Not every plugin supports this scope, so check the plugin's scope table.

Precedence: if a Consumer is in two groups that each have an instance of the same plugin, only the group whose name sorts first alphabetically applies. The docs note this rule may change.

In the plugin precedence list, Consumer group + Service + Route ranks second overall, and a plugin scoped only to a Consumer Group ranks below one scoped only to a Consumer and above Route-only, Service-only and global plugins.

Since 3.4, groups are a core entity, so the older override-based rate-limiting configuration is no longer needed.

## Checked

2026-11-04. Confirmed against the Consumer Groups and Plugins entity pages: creation at `/consumer_groups/`, per-group plugin instances, 3.4 core entity and overrides FAQ, alphabetical group-name precedence (rules not defined and may change), and the precedence order. Removed the field list (the schema section of the page is empty).
Method: documentation only; no commands were run.
