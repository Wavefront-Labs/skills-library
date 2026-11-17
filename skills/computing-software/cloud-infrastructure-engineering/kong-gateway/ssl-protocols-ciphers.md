---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.ssl-protocols-ciphers
name: ssl-protocols-ciphers
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, ssl-cipher-suite, tls-protocols, ssl-session, tls, kong-conf]
level: practitioner
status: docs-checked
description: "kong.conf TLS tuning: ssl_cipher_suite profiles, ssl_protocols (only with custom), session tickets, timeout and cache size, with defaults."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS protocols and cipher suite

| Setting | Default | Notes |
|---|---|---|
| `ssl_cipher_suite` | `intermediate` | `modern`, `intermediate`, `old`, `fips`, `custom`; TLSv1.1 needs `old` |
| `ssl_protocols` | `TLSv1.2 TLSv1.3` | client-side connections; ignored unless `ssl_cipher_suite = custom` |
| `ssl_session_tickets` | `on` | session resumption through tickets; no impact with TLSv1.3 |
| `ssl_session_timeout` | `1d` | how long clients may reuse session parameters |
| `ssl_session_cache_size` | `10m` | size of the caches that store session parameters |

`ssl_ciphers`, `ssl_protocols` and `ssl_prefer_server_ciphers` are all ignored unless `ssl_cipher_suite` is `custom`. If you use DHE ciphers you must also configure `ssl_dhparam`.

Proxy and Admin API listeners can use different protocol sets through the Nginx namespaces `nginx_proxy_ssl_protocols` and `nginx_admin_ssl_protocols`, which override the `http {}` setting.

`lua_ssl_protocols` (default `TLSv1.2 TLSv1.3`) is separate: it sets the TLS versions for OpenResty TCP cosocket handshakes, such as the database or a logging plugin, and does not affect connections to the upstream Service or from downstream clients.

## Checked

2026-11-04. Confirmed against kong.conf.default: all five defaults, the ignored-unless-custom rule, TLSv1.1 and `old`, the TLSv1.3 ticket note, the proxy and Admin namespace precedence note, and `lua_ssl_protocols`. Removed the custom example block, which only repeated the defaults.
Method: documentation only; no commands were run.
