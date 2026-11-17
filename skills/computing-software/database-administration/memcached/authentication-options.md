---
id: computing-software.database-administration.memcached.authentication-options
name: authentication-options
category: computing-software
field: database-administration
product: memcached
tags: [authentication, sasl, password, y, tls-client-certs]
level: practitioner
status: docs-checked
description: "Choose an authentication method: ASCII username/password file auth (-Y), binary SASL (-S), or TLS with client certificates."
sources:
  - https://docs.memcached.org/userguide/faq/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/binarysasl/
  - https://docs.memcached.org/serverguide/configuring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

FAQ: limited password based authentication is available in the basic protocol; you can also enable TLS and authenticate by certificate verification (see the enable-tls skill).

Text protocol token auth (optional username/password, see the `-Y` option): send a fake `set` with any key.
```
set <key> <flags> <exptime> <bytes>\r\n
username password\r\n
```
key, flags and exptime are ignored; bytes is the length of the username/password payload. `STORED` means success, after which any command should work normally. On failure the server returns `CLIENT_ERROR [message]`. Stats: `auth_cmds`, `auth_errors`.

Binary SASL: needs a server built with SASL support (1.4.3 or greater, `--enable-sasl`) and is enabled with `-S`, which enables the SASL commands, requires the binary protocol only, and requires successful authentication before commands may be issued. Protocol: command 0x20 lists mechanisms, 0x21 starts authentication, 0x22 is an authentication step; status 0x20 is unauthorized, 0x21 means further steps are needed, 0x81 (unknown command) means the server likely does not support authentication. It provides authentication but no encryption; the docs say not to run it over the internet at large, but to use it to protect from neighbours and accidents within large mostly trusted networks.

The Configuring page: do not expose memcached directly to the internet or untrusted users; SASL helps but should not be totally trusted. `stats settings` shows `auth_enabled_sasl`.

## Checked

2026-11-04. Confirmed against the FAQ, protocol.txt "Authentication" and settings statistics, the Binary SASL page (status and op codes, -S behaviour, 1.4.3, no encryption) and the Configuring page. Removed: the TLS verify-mode option value (not on a cited page) and the unstated "hardening always includes firewalls" claim.

Method: documentation only; no commands were run.
