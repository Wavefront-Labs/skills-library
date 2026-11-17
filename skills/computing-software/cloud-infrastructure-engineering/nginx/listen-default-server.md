---
id: computing-software.cloud-infrastructure-engineering.nginx.listen-default-server
name: listen-default-server
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, default-server, listen, catch-all, reuseport]
level: practitioner
status: docs-checked
description: "Using nginx listen parameters (default_server, ssl, reuseport, backlog, ipv6only) and ssl_reject_handshake for a catch-all server."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`listen` (context `server`) sets the address and port, or a `unix:` path, that the server accepts requests on. The default is `*:80` when nginx runs with superuser privileges and `*:8000` otherwise. If only an address is given, port 80 is used.

- `default_server` makes the server the default for that address:port pair. If no `listen` for the pair has it, the first server defined for the pair is the default.
- `ssl` makes all connections on that port work in SSL mode. The `http2` and `quic` parameters exist, but the `http2` parameter is deprecated: use the `http2` directive instead.
- Socket-related parameters (`backlog`, `reuseport`, `ipv6only`, `so_keepalive`, `fastopen` and others) can be given in any `listen` but only once for a given address:port pair.
- `backlog=number` defaults to `-1` on FreeBSD, DragonFly BSD and macOS and to `511` on other platforms.
- `reuseport` (1.9.1) creates a listening socket per worker so the kernel distributes connections; it works on Linux 3.9+, DragonFly BSD and FreeBSD 12+, and the page warns that inappropriate use may have security implications.
- `ipv6only=on|off` decides whether an IPv6 socket on `[::]` accepts only IPv6 or also IPv4 connections. It is on by default and can only be set once at start.

Catch-all that refuses handshakes for unknown names (`ssl_reject_handshake`, 1.19.4, default `off`, contexts `http`, `server`):

```nginx
server {
    listen 443 ssl default_server;
    ssl_reject_handshake on;
}

server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate     example.com.crt;
    ssl_certificate_key example.com.key;
}
```

SSL handshakes for server names other than `example.com` are rejected.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page (`listen` and parameters) and `ngx_http_ssl_module` (`ssl_reject_handshake`). Fixed: the draft said `[::]:443` also takes IPv4 unless `ipv6only=on` is set; the page says `ipv6only` is on by default. Removed: the "repeating reuseport is a startup error" claim (the page says only "once for a given address:port pair"), hostname-leak claims, the http2 version guess and its confirm markers, and the ss/openssl Verify step.
Method: documentation only; no commands were run.
