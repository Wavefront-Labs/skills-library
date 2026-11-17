---
id: computing-software.networking-hardware-and-wireless.powerdns.secondary-refresh-and-retry
name: secondary-refresh-and-retry
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, secondary, axfr, refresh, xfr-cycle-interval, soa-retry-default, retrieve]
level: practitioner
status: docs-checked
description: "How a PowerDNS secondary refreshes zones: freshness checks, SOA signature check, xfr-cycle-interval back-off, queue priority, multiple primaries."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondary refresh and retry

Enable with `secondary` (off by default). Only zones of type `SECONDARY` (or `SLAVE`) are handled. In SQL set `domains.type` to `SLAVE` and put comma-separated primary IPs in the `master` column.

- Freshness is checked at startup and every SOA `refresh`; a higher primary serial triggers a transfer.
- With equal serials on a presigned zone, the SOA RRSIG is compared too (uses the DO flag); disable with `secondary-check-signature-freshness` only if you must, since expired signatures can result when the primary is PowerDNS.
- Failures retry after `xfr-cycle-interval`; back-off is failures times that interval, capped at `soa-retry-default` (60 minutes by default). The same applies to refused transfers.
- A NOTIFY clears the back-off immediately. A transfer that fails after a NOTIFY is not retried until a new NOTIFY or the refresh timer.
- Queue priority since 4.5.0, highest first: `pdns_control`, API, NOTIFY, serial change at refresh, signature change at refresh; FIFO within a level.
- Force a transfer now: `pdns_control retrieve <zone>`.
- Multiple primaries: a random one serves freshness checks; a NOTIFY's source is used for that check and the following transfer. Keep all available.
- NOTIFY must be signed since 4.0.0; `allow-unsigned-notify` permits unsigned ones.
- The backend must support transactions so zones are never half-written. Under systemd, `ProtectSystem=full` blocks writes to `/etc` and `/home`, which can break AXFR into zone files.

## Checked

2026-11-08. Read docs/modes-of-operation.rst in full. Confirmed secondary being off by default, SECONDARY or SLAVE types, refresh and freshness checks, the SOA RRSIG comparison and secondary-check-signature-freshness, the back-off to a 60 minute maximum with default settings, NOTIFY clearing back-off, the 4.5.0 queue priorities, retrieve, multiple primary selection, signed NOTIFY since 4.0.0 and allow-unsigned-notify, transactions and the systemd ProtectSystem note. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
