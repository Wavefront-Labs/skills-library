---
id: computing-software.networking-hardware-and-wireless.bind9.ixfr-and-axfr
name: ixfr-and-axfr
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, ixfr, axfr, journal]
level: practitioner
status: docs-checked
description: "BIND 9 incremental and full zone transfers: ixfr-from-differences, max-ixfr-ratio, request-ixfr and AXFR fallback."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ixfr and axfr
IXFR sends only changes. A primary that loads a zone from a file can build differences with `ixfr-from-differences yes`, recording them in the zone journal.

- `max-ixfr-ratio` is the percentage of the full zone size above which named answers with AXFR instead. The minimum is 1% and the default is 100%; `unlimited` disables the check.
- `request-ixfr` controls whether a secondary asks for IXFR. Requests to servers that do not support IXFR fall back to AXFR automatically, so there is no need to list which servers support it.

Zone transfers use the TCP and TLS transports. `rndc retransfer zone` retransfers the given secondary zone from the primary.

## Checked

2026-11-04. Confirmed against the ARM entries for `ixfr-from-differences`, `max-ixfr-ratio`, `request-ixfr` and the zone transfer transport text, and the rndc man page for `retransfer`. Removed the unconfirmed TCP port 53 and full re-fetch wording.

Method: documentation only; no commands were run.
