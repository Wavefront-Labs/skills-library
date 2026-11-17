---
id: computing-software.networking-hardware-and-wireless.unbound.dns-over-tls-server
name: dns-over-tls-server
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dns-over-tls, tls-service-key, tls-service-pem, tls-port, dot]
level: practitioner
status: docs-checked
description: "Serve DNS-over-TLS to clients from Unbound: certificate and key, TLS port, extra ports and TLS protocol settings."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns over tls server
Set both `tls-service-key` (private key file) and `tls-service-pem` (matching public certificate); both default to `""` (disabled). `ssl-service-key` and `ssl-service-pem` are aliases.

- `tls-port` (alias `ssl-port`) defaults to 853.
- `tls-additional-port` adds extra ports that provide DNS-over-TLS.
- `tls-protocols` defaults to `"TLSv1.2 TLSv1.3"` (restart required).
- `tls-ciphers` sets the TLS 1.2 cipher list and `tls-ciphersuites` the TLS 1.3 suites; empty means defaults.
- `tls-session-ticket-keys` lists key files for session resumption; the first key encrypts and the rest only decrypt.
- Counters `num.query.tls` and `num.query.tls.resume` show TLS use and resumptions.

The same service key and certificate are used for DoH and DoQ.

## Checked
2026-11-04. Confirmed against the unbound.conf manual: tls-service-key/pem, tls-port default 853, tls-protocols default, cipher and session-ticket options, and the TLS counters. Nothing removed.
Method: documentation only; no commands were run.
