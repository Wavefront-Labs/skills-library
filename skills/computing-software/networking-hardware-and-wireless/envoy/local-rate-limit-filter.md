---
id: computing-software.networking-hardware-and-wireless.envoy.local-rate-limit-filter
name: local-rate-limit-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, local-ratelimit, token-bucket, rate-limit, 429, x-envoy-ratelimited, descriptors, enable-retry-after-header]
level: practitioner
status: docs-checked
description: "Apply an in-proxy token bucket rate limit with the Envoy local rate limit filter, per route descriptors, enforcement ratios and Retry-After."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/local_rate_limit_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local rate limit filter
The HTTP local rate limit filter applies a `token_bucket` when the route or virtual host has per-filter local rate limit config. With no tokens it returns 429 (configurable), sets `x-envoy-ratelimited` and can add more response headers. By default limits are per Envoy process; `local_rate_limit_per_downstream_connection` switches to per connection buckets.

```yaml
stat_prefix: local_rate_limiter
token_bucket: { max_tokens: 100, tokens_per_fill: 100, fill_interval: 60s }
filter_enabled:  { default_value: { numerator: 100, denominator: HUNDRED } }
filter_enforced: { default_value: { numerator: 100, denominator: HUNDRED } }
enable_retry_after_header: true
```
- `filter_enabled` with `filter_enforced` lower lets you shadow a limit first; unenforced mode can add request headers upstream.
- `enable_retry_after_header` emits `Retry-After` (delay-seconds, at least 1) for enforced 429s only, and does not overwrite a `Retry-After` set in `response_headers_to_add`.
- `descriptors` with route `rate_limits` actions (for example `request_headers` with a `descriptor_key`) give separate buckets per client or path.
- `local_cluster_rate_limit` divides each bucket across local cluster members by scaling token cost; if scaled cost exceeds `max_tokens` the request is still admitted at a full bucket and the bucket goes negative (runtime guard `envoy.reloadable_features.local_ratelimit_local_cluster_preserve_one_request` can revert).

Gotcha: by default the bucket is shared across workers and applies per Envoy process, so each Envoy enforces its own limit. Stats are under `<stat_prefix>.http_local_rate_limit.` (for example `rate_limited`, which counts responses without an available token even when not enforced); 429s are emitted to the normal cluster HTTP stats.

## Checked
2026-11-03. Confirmed against local_rate_limit_filter.rst and the local_rate_limit.proto reference. Removed or corrected: the per-worker wording and the stats/curl verify step.
Method: documentation only; no commands were run.
