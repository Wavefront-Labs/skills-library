---
id: computing-software.systems-network-administration.coredns.coredns-forward-policy-and-failover
name: coredns-forward-policy-and-failover
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, policy, failover, next]
level: advanced
status: docs-checked
description: "Select upstreams with random, round_robin or sequential policy and retry on chosen RCODEs using failover or next."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control upstream order and retry behaviour.

`policy random|round_robin|sequential` chooses the upstream; default is random.

`failover RCODE...`: by default forward tries the next upstream only when no DNS response arrives (such as a timeout). With failover, any response whose code matches, for example SERVFAIL or REFUSED, also moves on. NOERROR cannot be used. If all upstreams are tried, the response from the last attempt is returned.

```
forward . 1.2.3.4 5.6.7.8 9.0.1.2 {
    policy sequential
    failover SERVFAIL REFUSED
}
```

`next RCODE...` works across plugin instances: if the remote returns that code (e.g. NXDOMAIN), the next forward plugin runs. If there is no next plugin, or it is not forward, the setting is ignored. `next_on_nodata` does the same for NOERROR with an empty answer.

```
forward . 1.2.3.4 { next NXDOMAIN }
forward . 5.6.7.8 { next NXDOMAIN }
forward . 9.0.1.2 { }
```

Other limits:
- `max_connect_attempts` caps connect attempts per request; default 0 is no cap.
- `read_timeout` per upstream defaults to 2s and applies to each upstream individually, so large values leave less time for retries.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
