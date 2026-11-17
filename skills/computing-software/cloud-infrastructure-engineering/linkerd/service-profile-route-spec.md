---
id: computing-software.cloud-infrastructure-engineering.linkerd.service-profile-route-spec
name: service-profile-route-spec
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, serviceprofile, routes, retry-budget, legacy]
level: advanced
status: docs-checked
description: "Write a ServiceProfile with routes, conditions, timeouts and a retry budget, and know it is superseded by Gateway API types."
sources:
  - https://linkerd.io/2.19/reference/service-profiles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Linkerd 2.16 ServiceProfiles are supplanted by Gateway API types for per-route metrics, timeouts and retries. They remain supported for backward compatibility but get no more feature development.

A ServiceProfile spec has top-level fields `routes` (a list) and `retryBudget`, the maximum total retries as a ratio of original request volume.

Each route contains:

- `name`: how the route appears in the route label
- `condition`: a request match
- `responseClasses`: optional list of response classes
- `isRetryable`: marks the route as always safe to retry, so the proxy retries failed requests whenever possible
- `timeout`: the maximum time to wait for a response, including retries

A request match must contain exactly one of:

- `pathRegex`: a regular expression for the path, such as `'/authors/\d+'`
- `method`: one of GET, POST, PUT, DELETE, OPTION, HEAD, TRACE
- `all`: a list of matches that must all match
- `any`: a list where at least one must match
- `not`: a match that must not match

Setting more than one condition field in a single object is equivalent to using `all`.

A `retryBudget` has `retryRatio` (the maximum ratio of retry requests to original requests), `minRetriesPerSecond` (an allowance in addition to the ratio) and `ttl` (how long requests count towards the ratio).

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/reference/service-profiles/. Supplanted-by-Gateway-API warning, spec fields, route fields, request match options, the all-equivalence rule, the retry budget fields.

Removed or reworded: The claim that circuit breaking and retry annotations are ignored when a profile exists (the cited page does not say it).

Method: documentation only; no commands were run.
