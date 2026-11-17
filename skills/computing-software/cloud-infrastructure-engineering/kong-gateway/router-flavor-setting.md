---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.router-flavor-setting
name: router-flavor-setting
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, router-flavor, expressions, traditional-compatible, routing, kong-conf]
level: advanced
status: docs-checked
description: "Choose Kong's router engine with router_flavor: traditional_compatible (default), expressions or traditional, and what each accepts for Routes."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/entities/route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# router_flavor

Default in `kong.conf`: `router_flavor = traditional_compatible`. Options are `expressions` and `traditional` (deprecated in 3.0).

What each means for Routes:
- `traditional`: the original JSON-field routing format.
- `traditional_compatible`: accepts only JSON Routes (the DSL expression format is disabled); priority is calculated from the criteria a Route uses.
- `expressions`: recommended for Gateway 3.4+. Accepts both expression Routes and JSON Routes. If an expression Route matches, the JSON router does not run.

Facts to remember:
- Priority under `traditional_compatible` and `expressions` follows the criteria used, so a Route with both `hosts` and `headers` outranks one with only `hosts`.
- `regex_priority` cannot be set together with a non-empty `expression`.
- `path_handling = v1` is not supported in expressions mode.
- In expressions mode, put frequently matched Routes at higher priority for performance.

Related: if a lower-priority Route matches unexpectedly, the Route docs say to set `route_match_calculation` to `strict` in `kong.conf`.

Worker rebuild behaviour: `worker_consistency` defaults to `eventual`, and `worker_state_update_frequency` to `5` seconds.

## Checked

2026-11-04. Confirmed against kong.conf.default (router_flavor default traditional_compatible and the three accepted values, traditional deprecated in 3.0, worker_consistency eventual, worker_state_update_frequency 5) and the Route entity page (expressions recommended for 3.4+, expression Route matching stops the JSON router, route_match_calculation strict).

Method: documentation only; no commands were run.
