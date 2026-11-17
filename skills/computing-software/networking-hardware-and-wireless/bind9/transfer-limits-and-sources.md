---
id: computing-software.networking-hardware-and-wireless.bind9.transfer-limits-and-sources
name: transfer-limits-and-sources
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, transfers-in, transfers-out, transfer-source]
level: practitioner
status: docs-checked
description: "BIND 9 zone transfer limits and source addresses: transfers-in, transfers-out, transfers-per-ns, serial-query-rate, transfer-source."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# transfer limits and sources
Limits (all in `options`):

- `transfers-in`: concurrent inbound transfers, default 10.
- `transfers-out`: concurrent outbound transfers, default 10; excess requests are refused.
- `transfers-per-ns`: inbound transfers from one remote server, default 2; override per server with the `transfers` phrase of `server`.
- `max-transfer-time-in`: terminate inbound transfers after this many minutes; default 120, maximum 40320.
- `serial-query-rate`: cap on SOA serial queries per second.

`transfer-source` binds the local IPv4 address for inbound transfers; it also sets the source for refresh queries and forwarded dynamic updates. That address must appear in the remote server's configuration, for example in its `allow-transfer`.

## Checked

2026-11-04. Read the Administrator Reference Manual entries for transfers-in, transfers-out, transfers-per-ns, max-transfer-time-in, serial-query-rate and transfer-source; defaults, the 40320-minute maximum and the allow-transfer note confirmed. Nothing was removed.

Method: documentation only; no commands were run.
