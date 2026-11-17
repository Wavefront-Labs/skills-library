---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.acl
name: acl
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, acl, consumer-groups-header, hide-groups-header, plugins, authorization]
level: practitioner
status: docs-checked
description: "acl plugin config: allow or deny group names (exactly one), hide_groups_header for X-Consumer-Groups, and always_use_authenticated_groups behaviour."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/acl/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acl

Config:

| Field | Default | Meaning |
|---|---|---|
| `allow` | none | group names allowed to consume the Service or Route |
| `deny` | none | group names blocked |
| `hide_groups_header` | `false` | when `true`, the `X-Consumer-Groups` header is not sent upstream |
| `always_use_authenticated_groups` | `false` | see below |

Exactly one of `allow` or `deny` must be set.

`always_use_authenticated_groups`: when `false`, authenticated groups are used only when there is no Consumer or the Consumer is anonymous. When `true`, authenticated groups are always used, falling back to the Consumer's groups if there are none.

## Checked

2026-11-04. Confirmed against the acl plugin schema.lua: allow, deny, hide_groups_header (default false), always_use_authenticated_groups (default false), the only-one-of and at-least-one-of entity checks, and the X-Consumer-Groups wording.

Method: documentation only; no commands were run.
