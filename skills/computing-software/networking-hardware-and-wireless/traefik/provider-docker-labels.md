---
id: computing-software.networking-hardware-and-wireless.traefik.provider-docker-labels
name: provider-docker-labels
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, docker-provider, labels, exposedbydefault, defaultrule, socket]
level: practitioner
status: docs-checked
description: "Route to Docker containers with Traefik labels, exposedByDefault, network selection and defaultRule, and handle docker socket risk."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/docker.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/other-providers/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# provider docker labels
The Docker provider watches containers and builds routing from labels. Install options: `endpoint` (default is the local unix socket), `username`, `password`, `useBindPortIP`, `exposedByDefault`, `network`, `defaultRule`, `httpClientTimeout`, `watch`, `constraints`, `allowEmptyServices` and `tls.*` for remote TLS endpoints.

```yaml
providers:
  docker:
    exposedByDefault: false
    network: proxy
```
```yaml
# compose service labels
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.whoami.rule=Host(`whoami.example.com`)"
  - "traefik.http.services.whoami.loadbalancer.server.port=80"
```
Gotchas: the reference's security note says accessing the Docker API without restriction is a security concern, because if Traefik is attacked the attacker might get access to the underlying host. `exposedByDefault` defaults to true; with `false`, containers without a `traefik.enable=true` label are ignored. A container linked to several networks needs the provider `network` option or the `traefik.docker.network` label, otherwise Traefik picks one at random. When a container exposes several ports, or none, set `traefik.http.services.<name>.loadbalancer.server.port`. Dollar signs in label values, such as password hashes, must be doubled in docker-compose.yml.

## Checked
2026-11-03. Confirmed against the Traefik Docker provider install reference and the Docker routing labels reference: install options and defaults, `traefik.enable`, `traefik.docker.network`, the port label and the Docker API security note, and the dollar-doubling rule shown in the Compose examples. Removed: the specific read-only mount and socket proxy advice and the log Verify step.
Method: documentation only; no commands were run.


