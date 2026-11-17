---
id: computing-software.networking-hardware-and-wireless.squid.ssl-bump-peek-and-splice
name: ssl-bump-peek-and-splice
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ssl-bump, peek-and-splice, sni, at-step, mimic]
level: sme
status: docs-checked
description: "Use the three SslBump steps to peek at the SNI, splice selected sites and bump the rest, and know the caveats."
sources:
  - https://wiki.squid-cache.org/Features/SslPeekAndSplice
  - https://www.squid-cache.org/Doc/config/ssl_bump/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peek and splice steps
- Step 1: Squid reads TCP-level details; for interception it builds a fake CONNECT from IP and port, then evaluates `ssl_bump`.
- Step 2: only if step 1 matched peek or stare; reads the TLS Client Hello (SNI) and evaluates again.
- Step 3: only if step 2 matched peek or stare; reads the Server Hello and certificate, validates it. Only splice, bump or terminate remain.

Example (peek at SNI and splice):
```
ssl_bump peek step1
ssl_bump splice serverIsBank
ssl_bump stare all
```

Caveats from the page:
- Client data in steps 1 and 2 can be false, for example a misleading SNI.
- Peeking at the server usually prevents bumping; staring usually prevents splicing.
- Resumed sessions have no certificate to examine.
- `dstdomain` matches the CONNECT URI, which may be only an IP; use `ssl::server_name`, which does no DNS lookups.

## Checked

2026-11-04. Read the SslPeekAndSplice wiki page and the ssl_bump directive page and confirmed the three steps, the peek and splice example, the peek and stare limits, session resumption and the dstdomain versus ssl::server_name note. Nothing was removed.

Method: documentation only; no commands were run.
