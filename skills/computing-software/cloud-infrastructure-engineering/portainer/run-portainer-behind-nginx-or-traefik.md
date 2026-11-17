---
id: computing-software.cloud-infrastructure-engineering.portainer.run-portainer-behind-nginx-or-traefik
name: run-portainer-behind-nginx-or-traefik
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [reverse-proxy, nginx, traefik, lets-encrypt, docker-compose]
level: practitioner
status: docs-checked
description: "Deploy Portainer behind an nginx-proxy or Traefik reverse proxy using Docker Compose, and the flags needed behind a proxy."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/reverse-proxy/nginx.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/reverse-proxy/traefik.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both proxy recipes use Docker Compose on Docker Standalone.

nginx: the example uses the `nginxproxy/nginx-proxy` image, which needs no extra configuration beyond two environment variables on the Portainer service: `VIRTUAL_HOST` (your domain) and `VIRTUAL_PORT=9000`. The proxy publishes port 80 and mounts the Docker socket read-only at `/tmp/docker.sock`. The Portainer service keeps port 8000 for the Edge tunnel, mounts the Docker socket and `portainer_data`, and uses `-H unix:///var/run/docker.sock`. Change `VIRTUAL_HOST`, then bring the stack up with Compose.

Traefik: the Compose file runs Traefik with entrypoints on 80 and 443, the Docker provider, and a Let's Encrypt ACME resolver using the HTTP challenge (set your email and create an `acme.json` file with permission 600 for storage). A catch-all router redirects HTTP to HTTPS, and Portainer gets labels with `traefik.enable=true` and its router rule.

Behind any proxy, the CLI options `--base-url` (when serving under a subpath such as `/portainer`) and `--trusted-origins` (to fix Origin invalid errors) are relevant.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Added the acme.json permission requirement.

Method: documentation only; no commands were run.
