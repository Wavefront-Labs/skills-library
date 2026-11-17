---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ssl-session-cache-and-tickets
name: ssl-session-cache-and-tickets
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, tls, mod-ssl, sslsessioncache, session-tickets, shmcb, forward-secrecy]
level: advanced
status: docs-checked
description: "Configure SSLSessionCache backends, SSLSessionCacheTimeout, SSLSessionTickets and ticket key files, and the perfect-forward-secrecy trade-off."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS session cache and tickets
## SSLSessionCache
Server config only; default `none`. Types: `none`, `nonenotnull`, `dbm:/path`, `shmcb:/path[(size)]` (recommended), `dc:UNIX:/path`, `dc:IP:host:port`. Access is serialised by the `ssl-cache` mutex.
```apache
SSLSessionCache "shmcb:/usr/local/apache/logs/ssl_gcache_data(512000)"
```

## SSLSessionCacheTimeout
Default 300 seconds; also covers RFC 5077 resumption (2.4.10+). Can be as low as 15 for testing.

## Tickets
- `SSLSessionTickets` default `on` (2.4.11+, OpenSSL 0.9.8f+).
- Running tickets without restarting the server regularly (e.g. daily) compromises perfect forward secrecy.
- `SSLSessionTicketKeyFile` needs a 48-byte random key file, for clusters; single instances should rely on the keys generated at startup.

## Related
- `SSLStaplingCache` accepts the same storage types except `none` and `nonenotnull`.

## Checked
2026-11-04. Confirmed against the mod_ssl reference: SSLSessionCache types, shmcb recommendation and ssl-cache mutex, SSLSessionCacheTimeout default and RFC 5077 note, SSLSessionTickets default and forward-secrecy warning, 48-byte ticket key file, SSLStaplingCache types. Corrected: the stapling cache exclusion list (none and nonenotnull). Removed: the claim about sharing cache backends with mod_cache.
Method: documentation only; no commands were run.
