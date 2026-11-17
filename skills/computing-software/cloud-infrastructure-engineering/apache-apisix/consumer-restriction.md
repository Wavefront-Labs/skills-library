---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.consumer-restriction
name: consumer-restriction
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, consumer-restriction, authorization, whitelist, blacklist, allowed-by-methods, plugin]
level: practitioner
status: docs-checked
description: "Restrict which consumers, services, routes or consumer groups may call an APISIX route with consumer-restriction, including per-consumer method lists and rejection codes."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/consumer-restriction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# consumer-restriction

Attributes:
- `type`: what is checked; `consumer_name` (default), `service_id`, `route_id` or `consumer_group_id`.
- `whitelist`, `blacklist`: arrays of allowed or denied values.
- `allowed_by_methods`: array of objects with `user` (consumer name) and `methods` (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, CONNECT, TRACE, PURGE).
- `rejected_code`: 403 by default (>= 200); `rejected_msg` optional.

At least one of `whitelist`, `blacklist` or `allowed_by_methods` must be set.

It needs an authentication plugin on the route so a consumer is identified. Allow only consumer JaneDoe:

```json
{
  "plugins": {
    "key-auth": {},
    "consumer-restriction": { "whitelist": ["JaneDoe"] }
  }
}
```

A blocked consumer gets `{"message":"The consumer_name is forbidden."}`. For service-ID restrictions the message is `{"message":"The service_id is forbidden."}`.

## Checked

2026-11-04: read the consumer-restriction plugin page; attributes table (type values and default, whitelist, blacklist, allowed_by_methods, methods list, rejected_code 403 and >= 200, rejected_msg), the JaneDoe whitelist example and both forbidden messages match. Nothing removed.

Method: documentation only; no commands were run.
