---
id: computing-software.database-administration.memcached.enable-tls
name: enable-tls
category: computing-software
field: database-administration
product: memcached
tags: [tls, ssl, encryption, enable-ssl, openssl]
level: practitioner
status: docs-checked
description: "Enable TLS in memcached 1.5.13+: build with --enable-tls, start with -Z and ssl_chain_cert/ssl_key, verify with openssl s_client."
sources:
  - https://docs.memcached.org/features/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Requirements: memcached 1.5.13 or newer, OpenSSL 1.1.1+, a TLS-capable client, and a build with `./configure --enable-tls`.

Start:
```
memcached -Z -o ssl_chain_cert=/path/to/cert,ssl_key=/path/to/key
```
`-Z` (`--enable-ssl`) turns it on for all TCP interfaces you specify. If startup fails, add `-v` to print errors.

Test: `openssl s_client -connect host:port`.

Options (see `memcached -h`):
- `ssl_keyformat` integer, default PEM (1).
- `ssl_verify_mode` 0 None (default), 1 Request, 2 Require, 3 Once.
- `ssl_ciphers`, `ssl_ca_cert` (PEM only).
- `ssl_wbuf_size` (KB, default 16): large replies are chunked; memory = value x worker threads.

Plain text on selected interfaces: prefix with `notls:` as in `-l notls:127.0.0.1:11212`.

Check: `stats settings` shows `ssl_` settings.

## Checked

2026-11-04. Confirmed against the TLS feature page (requirements, -Z, ssl_* options, notls:, ssl_wbuf_size, stats settings). Removed: the unconfirmed claim that mode 2 is for client-certificate authentication.

Method: documentation only; no commands were run.
