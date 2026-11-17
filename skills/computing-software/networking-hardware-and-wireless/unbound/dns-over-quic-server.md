---
id: computing-software.networking-hardware-and-wireless.unbound.dns-over-quic-server
name: dns-over-quic-server
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dns-over-quic, doq, ngtcp2, quic-port, openssl]
level: advanced
status: docs-checked
description: "Enable downstream DNS-over-QUIC in Unbound: library requirements, quic-port and quic-size, testing with doqclient and metrics."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/privacy/dns-over-quic.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns over quic server
Needs libngtcp2 (minimum 1.13.0) with OpenSSL 3.5.0 or later; build with `./configure --with-libngtcp2`.

Example options from the page:
```
interface: 127.0.0.1@2853
quic-port: 2853
tls-service-key: "privatefile.key"
tls-service-pem: "publicfile.pem"
quic-size: 8m
```
`quic-port` defaults to 853 (0 disables QUIC); `quic-size` limits resources and queries beyond it are refused.

Test: `make doqclient`, start `./unbound -dd -c theconfig.conf`, then `./doqclient -s 127.0.0.1 -p 2853 www.example.com A IN` (`-v` for more output). For server-side detail use a log file with verbosity 4 or higher, which also logs libngtcp2 internals.

Metrics: `num.query.quic` and `mem.quic`.

## Checked
2026-11-04. Confirmed against the DNS-over-QUIC topic page and the unbound.conf manual (quic-port default 853 and 0 disables, quic-size default 8m, library minimums, test steps, metrics). Removed the 1.22.0 and 1.24.0 version statements, which the pages do not state.
Method: documentation only; no commands were run.
