---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-timers-and-tcp-tuning
name: bgp-timers-and-tcp-tuning
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, timers, keepalive, hold-time, advertisement-interval, tcp-keepalive, fast-convergence]
level: practitioner
status: docs-checked
description: "Tune FRR BGP keepalive and hold timers, connect retry, DelayOpen, minimum hold time, advertisement interval, TCP keepalive, session DSCP and fast-convergence."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP timers and TCP tuning
- `neighbor PEER timers (0-65535) (0-65535)` sets keepalive and hold timers.
- `neighbor PEER timers connect (1-65535)` sets the connect retry interval.
- `neighbor PEER timers delayopen (1-240)` enables the RFC 4271 DelayOpenTimer (default disabled).
- `bgp minimum-holdtime (1-65535)` refuses sessions with a lower hold time (inactive when unset).
- `neighbor PEER advertisement-interval (0-600)` sets MRAI in seconds (default 0; ignored during conditional advertisement).
- `bgp tcp-keepalive (1-65535) (1-65535) (1-30)` sets TCP keepalive idle time, interval and max probes for new peers (default disabled).
- `bgp session-dscp (0-63)` sets DSCP for outgoing BGP packets.
- `bgp fast-convergence` tears down sessions immediately when a peer becomes unreachable rather than waiting for hold-timer expiry.
- `bgp fast-external-failover` resets eBGP peers on link flap (default on).
- Queue limits: `bgp input-queue-limit` and `bgp output-queue-limit` (1-4294967295); `write-quanta (1-64)` default 64; `read-quanta (1-10)`.

Profile defaults for keepalive/hold/connect: traditional 60 s / 180 s / 30 s; datacenter 3 s / 9 s / 10 s. See the config-versioning skill. BFD can be added with `neighbor PEER bfd` for faster detection.

## Checked

2026-11-04. Confirmed against the FRR BGP page, Basic Commands page (profile table) and BFD page: timers, connect, delayopen, minimum-holdtime, advertisement-interval, tcp-keepalive, session-dscp, fast-convergence, fast-external-failover, queue limits, quanta and profile defaults. Nothing changed.
Method: documentation only; no commands were run.
