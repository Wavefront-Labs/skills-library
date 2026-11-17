---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.plugin-scoping-precedence
name: plugin-scoping-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, plugin-scope, plugin-precedence, global-plugin, plugins, instance-name]
level: practitioner
status: docs-checked
description: "Where a Kong plugin can be applied (global, Service, Route, Consumer, Consumer Group) and the 12-level precedence order deciding which instance runs."
sources:
  - https://developer.konghq.com/gateway/entities/plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin scoping and precedence

A plugin is global, or scoped to any combination of Services, Routes, Consumers and Consumer Groups. A global plugin runs on every request; in open source "global" covers the whole environment. Each plugin supports only some scopes.

A plugin runs once per request, using the configuration that matches the most specific entities. Precedence, highest to lowest:

1. Consumer + Route + Service
2. Consumer Group + Service + Route
3. Consumer + Route
4. Consumer + Service
5. Consumer Group + Route
6. Consumer Group + Service
7. Route + Service
8. Consumer
9. Consumer Group
10. Route
11. Service
12. Global

If a Consumer is in two groups with scoped instances of the same plugin, only the alphabetically first group name applies.

Fields: `config` (shape defined by the plugin's `schema.lua`) and `instance_name`, a unique label that does not affect processing.

In the supported-scopes table, authentication plugins such as Basic Auth, Key Auth, HMAC Auth, JWT and OpenID Connect are not supported at Consumer or Consumer Group scope; they are supported on Route, Service and global.

## Checked

2026-11-04. Confirmed against the Plugins entity page: the five scopes, global scope per edition, the 12-entry precedence order, one run per request, alphabetical Consumer Group rule, the instance name label, and the Not supported entries for the listed authentication plugins. Replaced the blanket authentication claim with the listed plugins and removed the Route-versus-Service rate limit sentence, which the page does not state.
Method: documentation only; no commands were run.
