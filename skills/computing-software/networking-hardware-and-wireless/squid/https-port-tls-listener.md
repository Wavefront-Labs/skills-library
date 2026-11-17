---
id: computing-software.networking-hardware-and-wireless.squid.https-port-tls-listener
name: https-port-tls-listener
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, https-port, tls-cert, tls, accelerator]
level: practitioner
status: docs-checked
description: "Accept TLS-encrypted client connections with https_port, which needs tls-cert and shares http_port options."
sources:
  - https://www.squid-cache.org/Doc/config/https_port/
  - https://www.squid-cache.org/Doc/config/http_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# https_port TLS listener
Usage: `[ip:]port [mode] tls-cert=certificate.pem [options]`.

- `tls-cert` is mandatory.
- Squid must be built with GnuTLS or OpenSSL support.
- Modes and options are the ones documented for `http_port`.
- Most useful in accelerator mode, where the accelerator handles TLS.
- Several `https_port` lines may exist, each with its own certificate and options.

## Checked

2026-11-04. Read the https_port directive page and confirmed the GnuTLS or OpenSSL build requirement and that tls-cert is mandatory. Nothing was removed.

Method: documentation only; no commands were run.
