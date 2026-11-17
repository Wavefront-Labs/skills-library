---
id: computing-software.database-administration.memcached.bind-interfaces-and-ports
name: bind-interfaces-and-ports
category: computing-software
field: database-administration
product: memcached
tags: [networking, listen, bind, l, tcp]
level: practitioner
status: docs-checked
description: "Choose which interfaces and ports memcached listens on (-l, -p, -U) and why it must never face the internet."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://docs.memcached.org/advisories/ddos/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Since 1.5.6 memcached listens on TCP only by default.

- `-l <addr>` binds specific interfaces or IPs. Use `-l 127.0.0.1` for local-only, or a private IP for an internal network.
- `-p <port>` sets the TCP port (UDP follows it).
- `-U <port>` sets the UDP port; off by default since 1.5.6; `-U 0` disables it.

Security rule from the docs: memcached spends little effort defending itself against random connections. Do not expose it directly to the internet or to untrusted users. SASL helps but should not be fully trusted. Add firewalls to block external traffic.

Debian/Ubuntu packages bind 127.0.0.1 by default. In /etc/memcached.conf:
```
--listen 127.0.0.1
```

## Checked

2026-11-04. Confirmed against the Configuring page (-l, -p, -U, 1.5.6 default, do not expose to the internet) and the UDP DDoS advisory (Debian/Ubuntu default, /etc/memcached.conf). Removed: the closing Verify tip.

Method: documentation only; no commands were run.
