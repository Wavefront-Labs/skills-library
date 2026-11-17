---
id: computing-software.networking-hardware-and-wireless.unbound.infra-host-cache
name: infra-host-cache
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, infra-cache, infra-host-ttl, rtt, infra-keep-probing, dump-infra]
level: advanced
status: docs-checked
description: "Tune and inspect Unbound's infrastructure cache of upstream host RTT, lameness and EDNS data with the infra-* options and unbound-control."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# infra host cache
The infra cache stores per-host RTT, lameness and EDNS support.

- `infra-host-ttl` (900 s) lifetime of host entries.
- `infra-cache-numhosts` (10000) number of hosts cached.
- `infra-cache-slabs` lock-contention slabs (power of 2).
- `infra-cache-min-rtt` (50 ms) and `infra-cache-max-rtt` (120000 ms) bound the dynamic retransmit timeout.
- `infra-keep-probing: yes` (default no) keeps probing hosts marked down, one probe at a time.
- `unknown-server-time-limit` (376 ms) is the wait for a server of unknown responsiveness.

unbound-control:
- `dump_infra` shows contents.
- `flush_infra all` empties it; `flush_infra <IP>` removes one host (EDNS, ping and lameness data).
- `lookup name` shows the nameservers that would be used.

`infra.cache.count` in extended statistics reports entries.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: infra option names and defaults, flush_infra all|IP, dump_infra, lookup and infra.cache.count. Nothing removed.
Method: documentation only; no commands were run.
