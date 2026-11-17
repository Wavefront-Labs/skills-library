---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-tls-reverse-proxy
name: woodpecker-tls-reverse-proxy
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [tls, reverse-proxy, nginx, grpc]
level: advanced
status: docs-checked
description: "Terminate TLS for Woodpecker directly or behind Nginx, Apache, Caddy or Traefik, including gRPC."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker TLS and reverse proxy

Built-in TLS: mount a certificate and key and set

```ini
WOODPECKER_SERVER_CERT=/etc/certs/woodpecker.example.com/server.crt
WOODPECKER_SERVER_KEY=/etc/certs/woodpecker.example.com/server.key
```

The HTTPS listener defaults to `:443` (`WOODPECKER_SERVER_ADDR_TLS`), so expose that port. TLS uses Go's ListenAndServeTLS.

Reverse proxy: the HTTP server listens on `:8000` (`WOODPECKER_SERVER_ADDR`) and gRPC on `:9000` (`WOODPECKER_GRPC_ADDR`). The proxy must send `X-Forwarded-Proto`; Nginx example headers: `X-Forwarded-For $remote_addr`, `X-Forwarded-Proto $scheme`, `Host $http_host`, with `proxy_http_version 1.1`, `proxy_buffering off` and `chunked_transfer_encoding off`.

Apache needs modules `proxy` and `proxy_http`, plus `ProxyPreserveHost On` and `RequestHeader set X-Forwarded-Proto "https"`.

Caddy exposes UI and gRPC separately:

```caddy
woodpecker.example.com {
  reverse_proxy woodpecker-server:8000
}
woodpecker-agent.example.com {
  reverse_proxy h2c://woodpecker-server:9000
}
```

Traefik needs both the HTTP and gRPC services; the docs' example uses `loadbalancer.server.scheme=h2c` for the gRPC service on port 9000.

Agents then use `WOODPECKER_GRPC_SECURE=true`. The server serves gRPC without TLS, so put it behind a TLS proxy or use a unix socket for same-host agents. For tunnels such as ngrok or Tunnelmole, set `WOODPECKER_HOST` to the tunnel URL.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed the TLS and proxy related server settings described in the skill. Nothing removed. 

Method: documentation only; no commands were run.
