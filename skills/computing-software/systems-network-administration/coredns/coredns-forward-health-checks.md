---
id: computing-software.systems-network-administration.coredns.coredns-forward-health-checks
name: coredns-forward-health-checks
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, health-check, max-fails, upstream]
level: advanced
status: docs-checked
description: "Tune forward in-band health checking: max_fails, health_check interval, no_rec, custom domain, and what happens when all upstreams are down."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control when an upstream is considered down.

forward does health checking in band. After an error it runs a check in a loop, every 0.5s while the upstream reports unhealthy, then stops until the next error. The check is a recursive query for `. IN NS` over the same protocol as TO. Any response that is not a network error (REFUSED, NOTIMPL, SERVFAIL and so on) counts as healthy.

Options:
- `max_fails INTEGER`: consecutive failed checks before an upstream is down. Default 2. With 0, the upstream is never marked down or checked.
- `health_check DURATION [no_rec] [domain FQDN]`: change the interval (default 0.5s); `no_rec` clears the recursion desired flag (default true); `domain` sets the name queried (default `.`).
- `failfast_all_unhealthy_upstreams`: when every upstream is unhealthy, return SERVFAIL immediately.

Default when all upstreams are down: forward assumes health checking itself failed and tries a random upstream, which may or may not work. Always the random policy then, counted by `coredns_forward_healthcheck_broken_total`.

Example for DoT that avoids swamping the provider:

```
forward . tls://9.9.9.9 {
    tls_servername dns.quad9.net
    health_check 5s
}
```

Per-upstream failures are exported as `coredns_proxy_healthcheck_failures_total`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: corrected NOTIMP to NOTIMPL as written on the page.

Method: documentation only; no commands were run.
