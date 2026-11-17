---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-service-scale-update-and-registry-auth
name: swarm-service-scale-update-and-registry-auth
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-service, service-scale, with-registry-auth, service-update, image-digest, docker-swarm]
level: practitioner
status: docs-checked
description: "Change running Swarm services: service scale, update --image with --with-registry-auth for private registries, digest pinning, --force redeploys, --detach=false waits."
sources: ["https://docs.docker.com/reference/cli/docker/service/scale/", "https://docs.docker.com/reference/cli/docker/service/update/", "https://docs.docker.com/reference/cli/docker/service/create/", "https://docs.docker.com/reference/cli/docker/stack/deploy/", "https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swarm service scale, update and registry auth

## Scale
```bash
docker service scale web=6 worker=3          # several services at once
docker service update --replicas 6 web       # same for one service
docker service ls --format '{{.Name}} {{.Replicas}}'
```
`docker service scale` cannot be applied to global-mode services.

## Update the image
```bash
docker service update --image reg.example.com/web:1.8.1 --with-registry-auth web
docker stack deploy -c stack.yaml --with-registry-auth shop
```
- `--with-registry-auth` passes the login token from your local client (after `docker login`) to the swarm nodes, so they can log in to the registry and pull private images.
- By default the client queries the registry to resolve the image digest and supported platforms; `--no-resolve-image` skips that.

## Redeploy without changes
```bash
docker service update --force web            # recreate tasks even if nothing changed (rolling restart)
docker service update --force --image reg.example.com/web:latest --with-registry-auth web
```

## Wait for completion in scripts
```bash
docker service update --detach=false --image reg.example.com/web:1.8.1 --with-registry-auth web
docker service inspect web -f '{{.UpdateStatus.State}} {{.UpdateStatus.Message}}'
```
`--detach` defaults to true; `--detach=false` waits for the service to converge.

## Other common update flags
`--env-add/--env-rm`, `--secret-add/--secret-rm`, `--publish-add/--publish-rm`,
`--constraint-add/--constraint-rm`, `--label-add`, `--limit-memory`, `--reserve-cpu`,
`--update-parallelism`, `--rollback`.

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `docker service scale name=N ...` accepts several services and cannot scale global services; `--with-registry-auth` sends the login token to swarm nodes; digest resolution and `--no-resolve-image`; `--force` recreates tasks; `--detach` default true; the listed `--env-add/-rm`, `--secret-add/-rm`, `--publish-add/-rm`, `--constraint-add/-rm`, `--label-add`, `--limit-memory`, `--reserve-cpu`, `--update-parallelism`, `--rollback` flags exist on `docker service update`. Removed: error messages, digest pinning claim, moved-tag behaviour, exit-status claim, token-expiry gotchas.
Method: documentation only; no commands were run.
