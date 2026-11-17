---
id: computing-software.systems-network-administration.coredns.coredns-forward-limits-and-metrics
name: coredns-forward-limits-and-metrics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, max-concurrent, connections, metrics]
level: advanced
status: docs-checked
description: "Cap forward concurrency and idle connections, tune timeouts and read forward and proxy Prometheus metrics."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect CoreDNS and upstreams under load.

Options:
- `max_concurrent MAX`: limit concurrent queries. A query that would exceed MAX gets REFUSED, which does not count as a health failure. Pick MAX above the expected upstream query rate times upstream latency. Each concurrent query uses about 2kb of memory, which gives an upper bound.
- `expire DURATION`: drop cached connections after this time; default 10s.
- `max_idle_conns INTEGER`: idle connections cached per upstream; default 0 means unlimited.
- `read_timeout`: default 2s per upstream.
- `resolver IP[:PORT]...`: DNS servers used to resolve hostname TO endpoints at startup. If unset, the system resolver (/etc/resolv.conf) is used. A bare IP assumes port 53.

Timeouts per endpoint: the dial timeout is 30s by default and can decrease automatically down to 1s based on early results; the read timeout is a static 2s.

Metrics (with the prometheus plugin):
- `coredns_forward_healthcheck_broken_total`
- `coredns_forward_max_concurrent_rejects_total`
- `coredns_proxy_request_duration_seconds{proxy_name="forward", to, rcode}`
- `coredns_proxy_healthcheck_failures_total`
- `coredns_proxy_conn_cache_hits_total` and `..._misses_total`

The older `coredns_forward_requests_total`, `..._responses_total`, `..._request_duration_seconds` and `..._healthcheck_failures_total` are deprecated in favour of the proxy metrics. With the metadata plugin, forward publishes `forward/upstream`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
