---
id: computing-software.systems-network-administration.coredns.coredns-pprof-plugin
name: coredns-pprof-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, pprof, profiling, debugging, performance]
level: practitioner
status: docs-checked
description: "Publish Go runtime profiling data under /debug/pprof with pprof, change its address and enable block profiling."
sources:
  - https://coredns.io/plugins/pprof/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: profile a live CoreDNS process.

Syntax:

```
pprof [ADDRESS] {
    block [RATE]
}
```

The default address is `localhost:6053`, and endpoints live under `/debug/pprof` (visit it for an index). The plugin can be used once per server block. `block` enables block profiling; RATE defaults to 1 and must be positive.

This is a debugging tool. Some requests, such as collecting execution traces, can be slow. On a live server restrict access or enable it only temporarily.

Examples:

```
. {
    pprof
}
. {
    pprof 10.9.8.7:6060
}
. {
    pprof :6060 {
        block
    }
}
```

The first listens on the default; the second on a specific address; the third on all addresses at port 6060 with block profiling.

Use the Go tool against the endpoint: `go tool pprof http://localhost:6053`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/pprof/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the debug plugin remark and the operational-notes paragraph (repeated content and unsourced overhead claim).

Method: documentation only; no commands were run.
