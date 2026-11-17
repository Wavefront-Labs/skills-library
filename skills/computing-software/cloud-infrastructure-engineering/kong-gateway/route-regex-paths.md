---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.route-regex-paths
name: route-regex-paths
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, regex-paths, strip-path-regex, regex-priority, routes, paths]
level: advanced
status: docs-checked
description: "Regex paths in Kong Routes: a version-number regex example, how strip_path removes the whole regex match, cost of regex, and regex_priority."
sources:
  - https://developer.konghq.com/gateway/entities/route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex paths in Routes

Routes accept regex in `paths`, for example `/version/\d+/service`.

With `strip_path: true`, the entire regex-matched portion is removed before proxying. Request `/version/1/service/path/to/resource` reaches the upstream as `/path/to/resource`.

Regex is more expensive to evaluate than simple prefixes. In large deployments prefer plain prefixes, or use the expressions router when you need exact-match regex.

`regex_priority` (default `0`, meaning unset) orders regex-based Routes in the traditional flavor. It cannot be set alongside a non-empty `expression`.

Captured URI groups are available to request-transformer templates as `$(uri_captures.{GROUP})`. Kubernetes Ingress v1beta1 does not support named capture groups, so use unnamed groups there, such as `$(uri_captures[1])`.

## Checked

2026-11-04. Confirmed against the Route entity page (regex example and full-match stripping, regex cost and expressions-router advice) and routes.lua (regex_priority default 0 and its exclusion with expression). The uri_captures and Kubernetes v1beta1 note is stated on the request-transformer page.

Method: documentation only; no commands were run.
