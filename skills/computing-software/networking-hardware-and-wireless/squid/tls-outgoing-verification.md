---
id: computing-software.networking-hardware-and-wireless.squid.tls-outgoing-verification
name: tls-outgoing-verification
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, tls-outgoing-options, certificate-verification, cafile, min-version]
level: advanced
status: docs-checked
description: "Control how Squid verifies origin servers with tls_outgoing_options: CA files, minimum TLS version, ciphers and verify flags."
sources:
  - https://www.squid-cache.org/Doc/config/tls_outgoing_options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls_outgoing_options
Needs GnuTLS or OpenSSL. Default: `min-version=1.0`.

Options:
- `cafile=` PEM CA file (repeatable); `capath=` CA directory (OpenSSL or LibreSSL)
- `min-version=1.N`: 1.0, 1.1, 1.2 or 1.3
- `cipher=` permitted ciphers
- `default-ca[=off]` system trusted CAs, on by default
- `cert=`, `key=`, `crlfile=`, `domain=`, `options=`
- `flags=DONT_VERIFY_PEER` and `flags=DONT_VERIFY_DOMAIN`

`disable` stops Squid supporting https:// URLs. Without DONT_VERIFY_PEER the peer certificate must verify; without DONT_VERIFY_DOMAIN its name must match the server name or `domain=`. DONT_VERIFY_PEER weakens security.

## Checked

2026-11-04. Read the tls_outgoing_options directive page and confirmed the build requirement, the min-version default and values, and the cafile, capath, cipher, default-ca, cert, key, crlfile, domain, options, disable and flags options. Nothing was removed.

Method: documentation only; no commands were run.
