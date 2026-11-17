---
id: computing-software.systems-network-administration.coredns.coredns-bind-plugin
name: coredns-bind-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, bind, interface, listener, ipv6]
level: practitioner
status: docs-checked
description: "Restrict CoreDNS listeners to chosen IP addresses or interfaces with bind, including the except option and consolidation of multiple bind lines."
sources:
  - https://coredns.io/plugins/bind/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop binding to the wildcard address.

By default a listener binds to the wildcard host. Syntax:

```
bind ADDRESS|IFACE ... {
    except ADDRESS|IFACE ...
}
```

Behaviour:
- Each argument is an IP address or an interface name. If several are given, a listener opens on each.
- An interface name binds to all IPs on that interface (IPv4 and IPv6) at startup or reload; a reload happens on SIGHUP or when the config file changes.
- Several bind lines in one server block are consolidated: `bind 127.0.0.1` plus `bind ::1` equals `bind 127.0.0.1 ::1`.
- `bind lo` listens on both 127.0.0.1 and ::1. `bind lo { except 127.0.0.1 }` leaves only ::1 (or whatever else is on lo).
- `except` only affects the bind directive it is inside when several are used.

Listener contention bug: if one server block on a port uses bind, then every server block on that port must use bind, or none may. Mixing creates two listeners for the same address, so requests are randomly served by either, with unpredictable results.

## Checked

2026-11-08. Checked in full against the bind plugin README. Removed an unsupported claim about CoreDNS 1.8.4 serving the same zone and port twice.

Method: documentation only; no commands were run.
