---
id: computing-software.systems-network-administration.incus.network-zones-dns
name: network-zones-dns
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network-zone, dns, axfr, tsig, core-dns-address, peers, bind9]
level: advanced
status: docs-checked
description: "Serve DNS for Incus networks with network zones: core.dns_address, AXFR-only built-in server, peers and TSIG key naming, dns.zone.* network keys, auto-generated records."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_zones.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network zones

Supported on `ovn` and `bridge` networks. Zones are globally unique, even across projects.

```
incus network zone create <zone> [options...]
incus network set <network> dns.zone.forward="incus.example.net"
dig @<DNS_server_IP> -p <port> axfr <zone>
```

- Network keys: `dns.zone.forward` (comma-separated, at most one per project), `dns.zone.reverse.ipv4`, `dns.zone.reverse.ipv6`.
- Built-in DNS server: set `core.dns_address` to a local address, avoiding port 53. It supports only AXFR, so pair it with an external server such as bind9 or nsd.
- Peers: `peers.NAME.address` (IP match) and optional TSIG `peers.NAME.key`. Key names follow `<zone_name>_<peer_name>.`, e.g. `incus.example.net_bind9.`.
- Incus sends DNS NOTIFY on change; secondaries re-transfer each SOA refresh (15 minutes).
- Auto records: `<instance>.<zone>`, `<network>.gw.<zone>`, `<project>-<downstream>.uplink.<zone>` and PTR records.
- Project keys: `features.networks.zones` (off by default), `restricted.networks.zones`.

## Checked

2026-11-04: confirmed against the Incus network zones how-to (supported networks, global uniqueness, `dns.zone.*` keys, built-in AXFR-only DNS server and `core.dns_address`, peers and TSIG key naming, NOTIFY and 15-minute SOA refresh, generated record names, project feature keys). Nothing removed.

Method: documentation only; no commands were run.
