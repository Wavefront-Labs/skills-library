---
id: computing-software.systems-network-administration.coredns.coredns-bufsize-plugin
name: coredns-bufsize-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, bufsize, edns0, fragmentation, udp]
level: practitioner
status: docs-checked
description: "Cap the EDNS0 UDP payload size with bufsize to avoid IP fragmentation, knowing the 512 to 4096 range and 1232 default."
sources:
  - https://coredns.io/plugins/bufsize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop clients from advertising a UDP size that fragments.

Syntax: `bufsize [SIZE]`. The default is 1232 and the value must be between 512 and 4096. Only one argument is accepted and it applies to both IPv4 and IPv6.

Behaviour:
- If a request has an OPT RR advertising a buffer size larger than the limit, the request's size is reduced. Otherwise it is untouched.
- It cannot raise a client's size, only reduce it.
- Only queries with an OPT RR (EDNS0) are affected.
- It mitigates certain DNS vulnerabilities by preventing IP fragmentation.

Examples from the docs:

```
. {
    bufsize 1100
    forward . 172.31.0.10
    log
}
. {
    bufsize 1220
    file db.example.org
    log
}
```

The first limits the size of the outgoing query to the resolver; the second limits it for an authoritative server.

Consideration: 1232 bytes avoids fragmentation on the majority of networks today, but the right value depends on the MTU of the physical links in your path.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/bufsize/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
