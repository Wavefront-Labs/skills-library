---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.bot-detection
name: bot-detection
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, bot-detection, user-agent, bot-allow-deny, plugins, security]
level: intro
status: docs-checked
description: "bot-detection plugin: allow and deny arrays of regular expressions matched against the User-Agent header, both empty by default, HTTP protocols only."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/bot-detection/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bot-detection

Two config fields, both arrays of regular expressions matched against the `User-Agent` request header:

| Field | Default | Meaning |
|---|---|---|
| `allow` | `{}` | patterns for user agents to allow |
| `deny` | `{}` | patterns for user agents to deny |

The plugin cannot be scoped to a Consumer and applies to HTTP protocols only.

With both lists empty there are no custom patterns. For restrictions by address use ip-restriction instead.

## Checked

2026-11-04. Confirmed against the bot-detection schema.lua: allow and deny are arrays of regex strings with default {}, matched against User-Agent, no Consumer scoping, HTTP protocols.

Method: documentation only; no commands were run.
