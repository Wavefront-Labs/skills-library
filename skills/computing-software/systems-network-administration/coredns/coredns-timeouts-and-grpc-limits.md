---
id: computing-software.systems-network-administration.coredns.coredns-timeouts-and-grpc-limits
name: coredns-timeouts-and-grpc-limits
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, timeouts, doh, doq, connections]
level: advanced
status: docs-checked
description: "Tune server read, write and idle timeouts for TCP, TLS, DoH and DoQ servers with the timeouts plugin."
sources:
  - https://coredns.io/plugins/timeouts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: harden or relax encrypted DNS listeners.

timeouts:

```
timeouts {
    read DURATION
    write DURATION
    idle DURATION
}
```

Unset values use defaults that vary by server type; at least one must be given or the block should be omitted. TCP, TLS and DoH servers use read, write and idle. DoQ servers use read to bound receiving a query on an open QUIC stream and idle to bound idle QUIC connections. Longer idle timeouts help with routers that hold open DoT or DoH connections, and slow mobile links may need longer timeouts.

```
tls://.:5553 {
    tls /path/to/cert.pem /path/to/key.pem /path/to/ca.pem
    timeouts {
        read 10s
        write 20s
        idle 60s
    }
}
```

## Checked

2026-11-03. Page read: https://coredns.io/plugins/timeouts/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the grpc_server section (max_streams, max_connections, v1.14.0 behaviour), which the timeouts page does not document.

Method: documentation only; no commands were run.
