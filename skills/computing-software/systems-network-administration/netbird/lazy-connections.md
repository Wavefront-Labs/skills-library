---
id: computing-software.systems-network-administration.netbird.lazy-connections
name: lazy-connections
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, lazy-connections, inactivity-threshold, dns-warmup, nb-lazy-conn]
level: advanced
status: docs-checked
description: "Enable NetBird lazy connections so peer links open on demand and close after inactivity: settings, env vars, DNS warm-up, signal outage behaviour and caveats."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/lazy-connection.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lazy connections open peer connections only when traffic needs them and close idle ones. Needs v0.50.1+ on clients and, if self-hosted, on Management and Signal.

Enable: Settings > Clients > Enable Lazy Connections (on by default for accounts created on v0.74.0+).

Client override:
```
sudo netbird service reconfigure --service-env NB_LAZY_CONN=on
```
Values `on`/`off`, `true`/`false`, `1`/`0`; unset follows Management. For MDM-managed clients the `lazyConnection` policy key does the same, but `NB_LAZY_CONN` wins.

Tuning:
- `NB_LAZY_CONN_INACTIVITY_THRESHOLD`: Go duration, default 15m, minimum 1m.
- `NB_DNS_LAZY_WARMUP_TIMEOUT`: daemon env, default 2s. When a lookup returns two or more A/AAAA records for idle peers, they are woken before the first packet. Applies to custom DNS zones and private-service zones, not peer names.

Verify with `netbird status` (Lazy connection line).

Caveats:
- New connections need Signal; existing direct ones stay up. Relayed ones persist only if Relay runs separately from Signal.
- A connection stays closed only when both peers are lazy; otherwise it cycles.
- Rosenpass clients keep permanent connections.
- Since v0.74.1 `netbird up --enable-lazy-connection` does nothing.

## Checked

2026-11-04: read the lazy-connection page in full and the CLI page's deprecation note. Confirmed versions, defaults (15m, minimum 1m, 2s), env var values, MDM key and precedence, Signal-outage behaviour and the both-ends-lazy caveat. Nothing removed.

Method: documentation only; no commands were run.
