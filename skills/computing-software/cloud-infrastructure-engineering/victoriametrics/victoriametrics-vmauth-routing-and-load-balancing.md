---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmauth-routing-and-load-balancing
name: victoriametrics-vmauth-routing-and-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmauth, reverse-proxy, url-map, load-balancing, retry-status-codes, rate-limiting, auth-config]
level: practitioner
status: docs-checked
description: "Configure vmauth users, bearer tokens, url_map routing, load balancing, failover and concurrency limits."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmauth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmauth routing and load balancing

vmauth is an auth proxy and load balancer in front of VictoriaMetrics components. Start it with `vmauth -auth.config=/path/to/config.yml -httpListenAddr=0.0.0.0:8427`.

```yaml
users:
  - username: "foo"
    password: "bar"
    url_prefix: "http://victoria-metrics:8428/"
  - bearer_token: "ABCDEF"
    url_prefix: "http://victoria-metrics:8428/"
unauthorized_user:
  url_map:
    - src_paths: ["/app1/.*"]
      drop_src_path_prefix_parts: 1
      url_prefix: "http://app1-backend/"
  default_url: "http://some-backend/404-page.html"
```

Matchers in `url_map`: `src_paths`, `src_hosts`, `src_query_args`, `src_headers`, plus `deny_paths` to block endpoints such as `/select/[^/]+/prometheus/api/v1/status/active_queries`.

Load balancing: give `url_prefix` a list of backends for least-loaded round robin with `retry_status_codes: [500, 502]`. For HA use `load_balancing_policy: first_available` with a main and standby backend (also settable with `-loadBalancingPolicy`).

Limits: per-user `max_concurrent_requests`, global `-maxConcurrentRequests` and `-maxConcurrentPerUserRequests`, `-maxQueueDuration`, `-requestBufferSize`. Debug failures with `dump_request_on_errors: true` (may log sensitive data).

Other flags: `-httpAuthHeader` for custom auth headers (for example Firehose), `-mergeQueryArgs=extra_filters`, `-discoverBackendIPs=true`. Enterprise: `ip_filters` allow and deny lists.

Reload the config with `SIGHUP`, `GET /-/reload` (protect with `-reloadAuthKey`) or `-configCheckInterval`.

After editing the config, confirm that the reload succeeded and test each user's routing with a real request.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
