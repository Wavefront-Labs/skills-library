---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.route-matching-priority
name: route-matching-priority
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, route-priority, route-matching, hosts-headers, routes, expressions]
level: advanced
status: docs-checked
description: "How Kong picks among matching Routes: highest priority wins, more matching criteria rank higher, route_match_calculation strict, and the hosts, paths, snis fields."
sources:
  - https://developer.konghq.com/gateway/entities/route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route matching priority

The router sends each request to the highest-priority matching Route.

Fields a Route can match on:
- `paths`: URL paths, including regex, e.g. `["/service"]`
- `hosts`: domains, including wildcards, e.g. `["service.com"]` or `*.example.com`
- `methods`: HTTP methods
- `headers`: expected request header values
- `snis`: the TLS server name, e.g. `["my-sni"]`

With `router_flavor` set to `traditional_compatible` or `expressions`, priority is calculated from the criteria a Route uses. A Route specifying both `hosts` and `headers` ranks above one specifying only `hosts`.

If a lower-priority Route matches unexpectedly, set `route_match_calculation` to `strict` in `kong.conf`.

In expressions mode, give frequently matched Routes higher priority for better performance.

For regex Routes in the traditional flavor, `regex_priority` adjusts order among regex-based Routes.

CORS warning: browser preflight requests cannot carry a custom Host header, so the CORS plugin should only be used with Routes that match on paths or methods, not Routes that match only on `hosts`.

## Checked

2026-11-04. Confirmed against the Route entity page (highest-priority match wins, priority calculated from criteria so hosts plus headers outranks hosts alone, route_match_calculation strict, expressions-mode ordering advice) and the CORS plugin page (preflight Host header limitation). The Route page spells the flavor traditional_compat; kong.conf.default spells it traditional_compatible, which this skill uses.

Method: documentation only; no commands were run.
