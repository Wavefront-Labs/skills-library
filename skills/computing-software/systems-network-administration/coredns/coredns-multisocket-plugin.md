---
id: computing-software.systems-network-administration.coredns.coredns-multisocket-plugin
name: coredns-multisocket-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, multisocket, so-reuseport, performance, throughput]
level: advanced
status: docs-checked
description: "Run several listening sockets on one port with multisocket to use more CPU cores, with the NUM_SOCKETS default and sizing advice."
sources:
  - https://coredns.io/plugins/multisocket/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: raise throughput on many-core hosts.

multisocket starts multiple servers that listen on the same port using the SO_REUSEPORT socket option, so the kernel distributes incoming connections between sockets.

Syntax: `multisocket [NUM_SOCKETS]`. The default equals GOMAXPROCS and the maximum is 1024.

Examples:

```
. {
    multisocket 5
    forward . /path/to/resolv.conf
}
. {
    multisocket
    forward . /path/to/resolv.conf
}
```

The first starts five TCP and UDP servers; the second uses the default.

Recommendations from the docs:
- Tests with NUM_SOCKETS from 1 to 10 showed no side effects or degradation, so the default (GOMAXPROCS) is generally usable.
- For best results, test different values while measuring queries per second and system load.
- If testing is hard: measure CoreDNS's maximum CPU use without multisocket, then align NUM_SOCKETS with that use and your CPU limits. For example, if CoreDNS consumes 4 CPUs and 8 are available, set NUM_SOCKETS to 2.

The plugin is documented as a throughput option for environments with a large number of CPU cores.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/multisocket/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
