---
id: computing-software.cloud-infrastructure-engineering.docker.registry-mirror-fallback-behaviour
name: registry-mirror-fallback-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, registry-mirror, mirror-fallback, registry-mirrors-config, daemon-json, pull-through-cache, dockerd-debug]
level: advanced
status: docs-checked
description: "Understand when dockerd uses registry-mirrors and when it falls back to Docker Hub, why non-Hub images bypass mirrors, and how to prove which endpoint served a pull."
sources: ["https://docs.docker.com/docker-hub/image-library/mirror/", "https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://github.com/containerd/containerd/blob/main/docs/hosts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry mirror fallback behaviour

## What dockerd does
```json
{ "registry-mirrors": ["https://mirror-a.example.com", "https://mirror-b.example.com"] }
```
- Mirrors apply **only to Docker Hub** (`docker.io`) images. `ghcr.io/...`, `quay.io/...` and
  private registries are always pulled directly.
- For a Hub image, dockerd (per its source) builds the endpoint list from the configured mirrors in order,
  followed by the canonical Hub endpoint, and tries the next endpoint when a mirror pull fails (registry
  errors from a mirror count as fallback conditions).
- Pushes never go to mirrors.
- Fallback is logged only as `Attempting next endpoint for pull after error` at info level, so a dead mirror
  does not fail pulls: it moves load (and rate-limit hits) back to Hub.

## Prove which endpoint served the pull
```bash
docker info                       # lists Registry Mirrors
# enable debug temporarily: "debug": true in daemon.json, then SIGHUP (debug is reloadable)
sudo kill -HUP $(pidof dockerd)
docker pull alpine:3.20
sudo journalctl -u docker --since -2m
```
With debug on, the daemon logs `Trying to pull <repo> from <endpoint URL>` for each endpoint and
`Attempting next endpoint for pull after error` when it moves on. Also check the mirror's access log for the request.

## Make failures visible
- Monitor the mirror directly (`curl -f https://mirror-a.example.com/v2/`), not via pull success.
- Watch CI logs for Docker Hub rate-limit errors: they indicate pulls reaching Hub.
- For strict environments (no internet), block Docker Hub at the firewall so a mirror outage fails loudly
  instead of leaking traffic.

## Other clients
- **BuildKit** (`docker-container` and `kubernetes` builders) takes a BuildKit config file; configure
  `[registry."docker.io"] mirrors = ["mirror-a.example.com"]` in `buildkitd.toml`.
- **containerd** (Kubernetes nodes) uses `hosts.toml` per registry host namespace and can mirror any
  registry: listed hosts are tried first in order, then `server` is the fallback.
- Docker Desktop: set mirrors in Settings > Docker Engine JSON.

## Gotchas
- `registry-mirrors` entries need a scheme (`https://` or `http://`) and cannot contain credentials,
  a query or a fragment.
- A pull-through cache checks the remote for the latest content on a tag pull, but pinning digests removes
  any doubt about which image you got.

## Checked

2026-10-26. Documentation release: moby/moby daemon source (registry service endpoint lookup, pull fallback loop, mirror validation), docker/docs main (Hub mirror guide, BuildKit configuration), docker/cli dockerd reference (reload list), containerd docs/hosts.md main, checked 2026-10-26. Confirmed: mirrors apply to the Docker Hub namespace only, mirror-then-Hub endpoint order, fallback conditions for mirror errors, the two log messages, debug and registry-mirrors being SIGHUP-reloadable, mirror URL validation rules, buildkitd.toml syntax, containerd host ordering and server fallback. Removed unconfirmed claims: 5xx and not-found being listed as fallback triggers verbatim, the toomanyrequests error string, the claim that mirror URLs cannot contain a path, and stale-TTL behaviour.

Method: documentation only; no commands were run.
