---
id: computing-software.networking-hardware-and-wireless.unbound.listening-interfaces-and-ports
name: listening-interfaces-and-ports
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, interface, port, interface-automatic, outgoing-interface, systemd-resolved]
level: practitioner
status: docs-checked
description: "Choose where Unbound listens and which source addresses it uses: interface, port, interface-automatic, outgoing-interface and binding to nonlocal addresses."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# listening interfaces and ports
- `port` (default 53) is the port queries are answered on.
- `interface` takes an IP address or interface name, optionally `@port`. With none given it listens on localhost. Reloads do not change it; only a restart does. `ip-address` is a synonym.
- `interface-automatic: yes` listens on all current and future interfaces and replies from the source interface (experimental); `interface-automatic-ports` lists the ports it uses.
- `outgoing-interface` sets source addresses for queries to authoritative servers (default: all); an IPv6 netblock enables randomised sources.
- `ip-transparent` lets Unbound bind to non-local or not-yet-existing addresses (useful for failover setups; it needs root at start on some systems); `ip-freebind` does the same on Linux only.

A bind error on `0.0.0.0` usually means systemd-resolved holds the port; the getting-started guide's workaround is `interface: 127.0.0.1`.

Use `access-control` to say which clients may use the listeners.

## Checked

2026-11-08. Read port, interface, interface-automatic, outgoing-interface, ip-transparent and ip-freebind in the unbound.conf manual and the getting-started guide. Added that ip-transparent may need root at start on some systems.

Method: documentation only; no commands were run.
