---
id: computing-software.collaboration-platform-administration.vikunja.docker-traefik-caddy
name: docker-traefik-caddy
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, traefik-labels, caddy-reverse-proxy, compose-proxy, publicurl-https]
level: practitioner
status: docs-checked
description: "Put Vikunja behind Traefik 2 labels or a Caddy v2 container in Docker Compose, with the public URL setting the browser needs to reach the API."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both examples keep the postgres compose stack and set `VIKUNJA_SERVICE_PUBLICURL` to the public `https://` URL. The browser uses that URL for API calls, so it must be reachable from outside.

Traefik 2 (assumes the docker provider is configured, entrypoint `https`, cert resolver `acme`, domain `vikunja.example.com`). Join the vikunja service to an external network `web` plus `default`, no published ports, and add labels:
- `traefik.enable=true`
- `traefik.docker.network=web`
- `traefik.http.routers.vikunja.rule=Host(...)`
- `traefik.http.routers.vikunja.entrypoints=https`
- `traefik.http.routers.vikunja.tls.certResolver=acme`

Adjust entrypoint and resolver names to your setup.

Caddy v2: add a `caddy` service (ports 80 and 443, `depends_on` vikunja) mounting `./Caddyfile:/etc/caddy/Caddyfile:ro` with:

```
vikunja.example.com {
    reverse_proxy vikunja:3456
}
```

In both cases ensure the files directory is writable by UID 1000 before starting.

## Checked

2026-11-04. Confirmed against the Vikunja Full docker example (setup/full-docker-example): the Traefik 2 assumptions, network and labels, the Caddy v2 service, Caddyfile, mounts, the publicurl explanation and the files permission warning. Nothing removed.

Method: documentation only; no commands were run.
