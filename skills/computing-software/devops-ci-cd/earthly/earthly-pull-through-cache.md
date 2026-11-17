---
id: computing-software.devops-ci-cd.earthly.earthly-pull-through-cache
name: earthly-pull-through-cache
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, pull-through-cache, registry-mirror, buildkit-additional-config, insecure, htpasswd, docker-hub, rate-limit]
level: advanced
status: docs-checked
description: "Point Earthly at a registry pull-through cache using buildkit_additional_config mirrors, with an insecure Docker Hub registry quick start, auth and TLS tips."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/pull-through-cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pull-through cache for Earthly

Goal: avoid Docker Hub/Quay pull limits and costs by mirroring images through your own registry.

A pull-through cache is a registry mirror holding no images initially: it answers from cache, or pulls from upstream and caches the result.

## Quick start (insecure, trusted network)
On the server (example IP 192.168.0.80) write a registry config such as ~/.docker-registry-config.yml with `storage.filesystem.rootdirectory: /var/lib/registry`, `http.addr: :5000`, and
```yaml
proxy:
  remoteurl: https://registry-1.docker.io
  username: [username]
  password: [password]
```
Start it:
```bash
docker run --rm --network host -d --name docker-registry -v $HOME/.docker-registry-config.yml:/root/config.yml registry.hub.docker.com/library/registry:2 registry serve /root/config.yml
docker logs --follow docker-registry
```
Docker client: add `{"registry-mirrors" : ["http://192.168.0.80:5000"]}` to /etc/docker/daemon.json and restart docker.

## Configure Earthly
Edit ~/.earthly/config.yml:
```yaml
global:
  buildkit_additional_config: |
    [registry."docker.io"]
      mirrors = ["192.168.0.80:5000"]
    [registry."192.168.0.80:5000"]
      insecure = true
```
Earthly detects the change and restarts `earthly-buildkitd`. Force and inspect it:
```bash
earthly bootstrap && docker exec earthly-buildkitd cat /etc/buildkitd.toml
```
By default Earthly expects the mirror to use TLS; `insecure = true` is for unsecured mirrors, the general form being `[registry."<upstream>"] mirrors = ["<mirror>"]` plus `[registry."<mirror>"] insecure = true`.

## Hardening tips
- Mirrors are unsecured by default; add an `htpasswd` auth block (`realm: basic-realm`, `path: /auth/htpasswd`).
- Add TLS (own certs or built-in `letsencrypt` with `cachefile`, `email`, `hosts`). The shipping `library/registry` image does not yet support the DNS-01 challenge.

## Gotcha
To prove the cache is used, block Docker Hub hosts in /etc/hosts; a misconfigured daemon.json then fails with a connection-refused pull error, while a working cache still serves the pull and logs requests on the registry container.

## Checked

2026-11-07. Read docs/ci-integration/pull-through-cache.md in full. The registry config, docker run, daemon.json, buildkit_additional_config mirror and insecure settings, bootstrap command, htpasswd, TLS and DNS-01 notes, and the /etc/hosts check match. The 192.168.0.80 server in the example is not a fetched URL. Nothing removed.
Method: documentation only; no commands were run.
