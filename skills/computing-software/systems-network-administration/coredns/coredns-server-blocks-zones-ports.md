---
id: computing-software.systems-network-administration.coredns.coredns-server-blocks-zones-ports
name: coredns-server-blocks-zones-ports
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, server-block, zones, port, corefile]
level: intro
status: docs-checked
description: "Declare which zones a CoreDNS server is authoritative for, set the listening port per block, and avoid the duplicate zone and port startup error."
sources:
  - https://coredns.io/manual/configuration/
  - https://coredns.io/2017/06/08/how-queries-are-processed-in-coredns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map zones to listening ports with server block headers.

A server block starts with the zones the server is responsible for, separated by spaces, followed by an opening brace. The block `. { }` handles every possible query because `.` is the root zone.

A port is added after the zone with a colon. The default is port 53:

```
.:1053 {
    whoami
}
```

Rules and failure modes:
- A port written in the block header cannot be overruled with the `-dns.port` option.
- Two server blocks that assign the same zone to the same port are an error at startup. The manual's example is two `.:1054` blocks. Changing the second to 1055 makes them two separate servers.
- Since CoreDNS 1.8.4 the same zone and port may appear twice if each block uses the bind plugin to attach to a different interface or IP address.
- Blocks sharing a port are folded into one server internally. The server multiplexes queries to the plugin chain of the most specific matching zone, and if no block matches, the answer is SERVFAIL.

A single query goes through exactly one plugin chain, the one of the best matching block.

## Checked

2026-11-08. Read the configuration manual page and the cited how-queries blog post in full. Added the blog as a source for the port-folding and SERVFAIL claims.

Method: documentation only; no commands were run.
