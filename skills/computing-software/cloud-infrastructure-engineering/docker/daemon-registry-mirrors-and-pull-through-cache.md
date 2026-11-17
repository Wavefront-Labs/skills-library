---
id: computing-software.cloud-infrastructure-engineering.docker.daemon-registry-mirrors-and-pull-through-cache
name: daemon-registry-mirrors-and-pull-through-cache
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, registry-mirror, pull-through-cache, mirror, registry-mirrors-config, mirror-daemon-json, proxy-remoteurl, pull-through-registry, rate-limits]
level: practitioner
description: "Run distribution as a Docker Hub pull-through cache with proxy.remoteurl and point daemons at it via registry-mirrors, knowing it only mirrors Docker Hub."
sources: ["https://distribution.github.io/distribution/recipes/mirror/", "https://docs.docker.com/docker-hub/image-library/mirror/", "https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# registry-mirrors and a pull-through cache

## The cache
```yaml
# config.yml for the registry image
version: 0.1
proxy:
  remoteurl: https://registry-1.docker.io
  username: hubuser            # optional: authenticated pulls get the higher rate limit
  password: <hub access token>
  ttl: 168h                    # how long cached content is kept
storage:
  filesystem: { rootdirectory: /var/lib/registry }
  delete: { enabled: true }   # needed for TTL eviction
http:
  addr: :5000
  tls: { certificate: /certs/mirror.crt, key: /certs/mirror.key }
```
```sh
docker run -d --name hub-mirror --restart always -p 443:5000 \
  -v "$PWD/config.yml:/etc/distribution/config.yml:ro" -v mirror-data:/var/lib/registry \
  -v "$PWD/certs:/certs:ro" registry:3
```
The Docker mirror guide says to set `proxy.remoteurl` in `/etc/docker/registry/config.yml` (registry:2 era);
the distribution docs use `/etc/distribution/config.yml` (registry:3). Use the path matching your image.
A registry cannot mirror another private registry: only Docker Hub can be mirrored.

## Point daemons at it
```json
{ "registry-mirrors": ["https://mirror.example.com"] }
```
Put it in `/etc/docker/daemon.json` (or pass `--registry-mirror`), then reload or restart the daemon:
`registry-mirrors` is in the list of options that can be reloaded with SIGHUP. Docker Desktop: Settings -> Docker Engine.

## Critical limitation
`registry-mirrors` applies **only to Docker Hub** images (`nginx`, `library/*`, `org/app`
without a registry host); the Docker guide states that only the central Hub can be mirrored.
`ghcr.io/...`, `quay.io/...` go direct. For those, use
containerd `hosts.toml` mirrors (Kubernetes nodes), Harbor proxy-cache projects, or
rewrite image references.

## Behaviour
- The daemon source lists configured mirrors first, in configuration order, then the canonical Docker Hub
  endpoint, and moves on to the next endpoint after a mirror error: a broken mirror is a slowdown, not
  an outage.
- If you give the cache Hub credentials, the private resources that account can reach become available on
  your mirror; secure the mirror with authentication.
- Mirror URLs in `daemon.json` must include a scheme (`https://` or `http://`) and no credentials, query or fragment.
- `docker-container` and `kubernetes` buildx builders use a BuildKit configuration file: set
  `[registry."docker.io"] mirrors = ["mirror.example.com"]` in `buildkitd.toml` (`debug = true` logs mirror use).
- With Registry Access Management restrictions, pulls of Hub images are blocked even via a mirror; pull
  from the mirror host directly and retag.

## Verify
```sh
docker info | grep -A2 'Registry Mirrors'
docker pull alpine:3.20 && curl -s https://mirror.example.com/v2/_catalog
```

## Checked

2026-10-26. Documentation release: docker/docs main (Docker Hub mirror guide, BuildKit configuration), docker/cli dockerd reference, distribution/distribution recipes/mirror and configuration, moby/moby daemon source (registry config and pull endpoint logic) on 2026-10-26. Confirmed: proxy.remoteurl/username/password/ttl keys, delete.enabled requirement for TTL cleanup, Hub-only mirroring, registry-mirrors daemon.json key and reload via SIGHUP, mirror URL validation rules, mirror-before-Hub endpoint order and next-endpoint fallback, buildkitd.toml mirrors syntax, Registry Access Management caveat. Removed unconfirmed claims: the "mirror pulls are anonymous" wording, that buildx docker-container builders never read daemon.json, and a catalogue listing detail.

Method: documentation only; no commands were run.
