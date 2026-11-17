---
id: computing-software.cloud-infrastructure-engineering.docker.traefik-and-caddy-reverse-proxy-via-compose-labels
name: traefik-and-caddy-reverse-proxy-via-compose-labels
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-reverse-proxy, traefik-compose, traefik, caddy-docker-proxy, lets-encrypt, docker-labels, tls, socket-proxy, compose-production]
level: practitioner
status: gated
description: "Route HTTPS to Compose services with Traefik or caddy-docker-proxy labels: entrypoints, routers, ACME, the docker network setting, $$ escaping, and debugging 404/502."
sources: ["https://doc.traefik.io/traefik/providers/docker/", "https://doc.traefik.io/traefik/routing/providers/docker/", "https://doc.traefik.io/traefik/https/acme/", "https://github.com/lucaslorentz/caddy-docker-proxy", "https://docs.docker.com/reference/compose-file/services/#labels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy via Compose labels (Traefik / Caddy)

**Goal:** one proxy container terminates TLS for many services on a host; each service
declares its own hostname with labels and no proxy config file needs editing.

## Traefik v3
```yaml
services:
  traefik:
    image: traefik:v3.1
    command:
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --providers.docker.network=web
      - --entrypoints.web.address=:80
      - --entrypoints.web.http.redirections.entrypoint.to=websecure
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.le.acme.tlschallenge=true
      - --certificatesresolvers.le.acme.email=ops@example.com
      - --certificatesresolvers.le.acme.storage=/letsencrypt/acme.json
    ports: ["80:80", "443:443"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt
    networks: [web]
    restart: unless-stopped

  api:
    image: ghcr.io/org/api:1.4.2
    networks: [web, backend]
    labels:
      - traefik.enable=true
      - traefik.http.routers.api.rule=Host(`api.example.com`)
      - traefik.http.routers.api.entrypoints=websecure
      - traefik.http.routers.api.tls.certresolver=le
      - traefik.http.services.api.loadbalancer.server.port=8080
      - traefik.http.routers.api.middlewares=api-auth
      - traefik.http.middlewares.api-auth.basicauth.users=admin:$$apr1$$H6uskkkW$$IgXLP6ewTrSuBkTrqE8wj/

networks:
  web: { name: web }        # shared across Compose projects on the host
  backend: {}
volumes: { letsencrypt: {} }
```
Key points:
- `exposedbydefault=false` + `traefik.enable=true` per service, or every container gets a route.
- `providers.docker.network` (or label `traefik.docker.network=web`) is required when a
  service is on several networks; otherwise Traefik may pick an unreachable IP → **502/504**.
- `loadbalancer.server.port` is needed when the image exposes several ports or none.
- Compose interpolates `$`: bcrypt/apr1 hashes in labels need `$$`.
- Backticks in `Host(...)` are required syntax.
- Containers with a `healthcheck` are routed only while **healthy**; a failing healthcheck
  looks like a 404 "no route".
- ACME `acme.json` must be mode 600; persist it or you hit Let's Encrypt rate limits on
  every restart.

## Caddy (caddy-docker-proxy)
```yaml
services:
  caddy:
    image: lucaslorentz/caddy-docker-proxy:2.9
    ports: ["80:80", "443:443"]
    environment: { CADDY_INGRESS_NETWORKS: web }
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - caddy-data:/data
    networks: [web]
  api:
    networks: [web]
    labels:
      caddy: api.example.com
      caddy.reverse_proxy: "{{upstreams 8080}}"
```
Caddy gets certificates automatically; labels render into a Caddyfile
(`docker logs caddy` shows the generated config).

## Socket exposure
Both read the Docker socket; a compromised proxy is root on the host. Put a socket proxy
(`tecnativa/docker-socket-proxy` with `CONTAINERS=1` only) in between and point Traefik at
`--providers.docker.endpoint=tcp://socket-proxy:2375`.

## Debugging
- Traefik dashboard: `--api.dashboard=true` with a router on `api@internal` behind auth;
  `--log.level=DEBUG` shows label parse errors.
- 404: no router matched (wrong Host, `traefik.enable` missing, unhealthy container).
- 502: router matched, backend unreachable (wrong network/port).

## Verify
```bash
curl -sI https://api.example.com | head -1
curl -s --resolve api.example.com:443:127.0.0.1 -k https://api.example.com/healthz   # before DNS
docker logs traefik 2>&1 | grep -i acme | tail
```

## Checked

- Date: 2026-11-02.
- Confirmed against: caddy-docker-proxy labels caddy.reverse_proxy, {{upstreams 8080}} and CADDY_INGRESS_NETWORKS (caddy-docker-proxy README).
- Not confirmed: every Traefik flag and label name: the Traefik docs pages are JavaScript-only and returned stubs (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
