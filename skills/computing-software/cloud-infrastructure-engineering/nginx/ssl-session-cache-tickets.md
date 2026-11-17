---
id: computing-software.cloud-infrastructure-engineering.nginx.ssl-session-cache-tickets
name: ssl-session-cache-tickets
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-session-cache, ssl-session-tickets, resumption, tls-performance]
level: practitioner
status: docs-checked
description: "Tuning TLS session resumption in nginx: shared session cache, timeout, session ticket keys and rotation."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/server_names.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults: `ssl_session_cache none`, `ssl_session_timeout 5m`, `ssl_session_tickets on`.

```nginx
ssl_session_cache   shared:SSL:10m;
ssl_session_timeout 10m;
ssl_session_ticket_key current.key;
ssl_session_ticket_key previous.key;
```

- `shared:name:size` is shared by all workers, sized in bytes; one megabyte stores about 4000 sessions (so `10m` is about 40000). The same name can be used in several virtual servers.
- `builtin[:size]` is used by one worker only (default 20480 sessions) and can cause memory fragmentation. The docs say a shared cache alone is more efficient than combining both.
- `none` tells the client sessions may be reused but stores nothing; `off` tells the client sessions may not be reused.
- A `shared` cache also generates, stores and periodically rotates TLS session ticket keys (1.23.2) unless `ssl_session_ticket_key` is set.
- `ssl_session_ticket_key file` is needed if the same key must be shared between servers; by default a randomly generated key is used. With several keys only the first encrypts, which allows rotation (newest first). The file must hold 80 or 48 random bytes (`openssl rand 80 > ticket.key`): AES256 for 80 bytes, AES128 for 48.
- `ssl_session_tickets off` disables resumption through tickets.
- Session directives apply from the default server (sessions are always resumed from the default server context), so specify them there.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_ssl_module page: defaults, cache types and sizes, ticket key behaviour, key file sizes. Confirmed in the server_names page: default-server rule.
Removed as unconfirmed: the forward-secrecy discussion, "new random key at every reload", the 1h timeout, and the openssl s_client -reconnect verify step.
Method: documentation only; no commands were run.
