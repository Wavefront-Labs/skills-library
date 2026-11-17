---
id: computing-software.systems-network-administration.immich.reverse-proxy-traefik
name: reverse-proxy-traefik
category: computing-software
field: systems-network-administration
product: immich
tags: [traefik, respondingtimeouts, error-499, labels, entrypoint]
level: practitioner
status: docs-checked
description: "Configure Traefik v3 for Immich: raise entrypoint respondingTimeouts so long video uploads stop failing with 499, and set the router labels."
sources:
  - https://docs.immich.app/administration/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop video uploads dying after one minute behind Traefik.

Traefik's default entrypoint `respondingTimeouts` is 60 seconds, which makes video uploads stop after one minute with Error Code 499. Raise them on the entrypoint Immich uses (here `websecure` on port 443). The example below is for Traefik version 3.

`traefik.yaml`:

```yaml
entryPoints:
  websecure:
    address: :443
    transport:
      respondingTimeouts:
        readTimeout: 600s
        idleTimeout: 600s
```

With this, a transfer fails only after ten minutes, which the docs consider enough in most cases; increase it if needed.

Then add labels to `immich-server` in `docker-compose.yml`:

```yaml
services:
  immich-server:
    labels:
      traefik.enable: true
      traefik.http.routers.immich.entrypoints: websecure
      traefik.http.routers.immich.rule: Host(`immich.example.com`)
      traefik.http.services.immich.loadbalancer.server.port: 2283
```

Traefik must be able to reach the network Immich runs in; usually that means adding the Traefik network to the `immich-server` service.

As with any proxy, forward the `Host`, `X-Real-IP`, `X-Forwarded-Proto` and `X-Forwarded-For` headers and serve Immich from the root of a domain, not a sub-path.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/reverse-proxy (Traefik Proxy example config).
Removed or reworded: the slower-links wording.
Method: documentation only; no commands were run.
