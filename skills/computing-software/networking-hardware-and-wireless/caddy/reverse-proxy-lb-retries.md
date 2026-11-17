---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-lb-retries
name: reverse-proxy-lb-retries
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [lb-retries, lb-try-duration, lb-try-interval, lb-retry-match, failover, reverse-proxy]
level: practitioner
status: docs-checked
description: "Make reverse_proxy hold and retry requests while backends are down with lb_retries, lb_try_duration, lb_try_interval and lb_retry_match."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ride out restarts and brief outages without surfacing errors.

Load balancing is on by default, retries are off. Retries also help with a single upstream: they hold the request until a healthy one can be selected, for instance during a reboot or redeploy.

- `lb_retries <n>`: retry selection this many times if the next host is down; default 0. If `lb_try_duration` is set, the duration wins and may stop retries early.
- `lb_try_duration <duration>`: how long clients wait while Caddy tries to find an available host; default 0 (off). The page suggests starting near `5s`, since the HTTP transport's default dial timeout is `3s`, which leaves room for at least one retry.
- `lb_try_interval <interval>`: pause between selections; default `250ms`, relevant only after failures. Setting `0` with a non-zero try duration can spin the CPU when all backends are down and latency is very low.
- `lb_retry_match <request-matcher>`: which requests may be retried when the connection succeeded but the round trip failed; failed connections are always retryable. By default only `GET` is retried. The syntax matches named request matchers without the `@name`; one matcher fits on the same line, several need a block.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
