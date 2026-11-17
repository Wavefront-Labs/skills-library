---
id: computing-software.cloud-infrastructure-engineering.zot.docker-pull-through-cache
name: docker-pull-through-cache
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, pull-through-cache, registry-mirrors, docker-daemon, hosts-toml, docker-hub-mirror]
level: practitioner
status: docs-checked
description: "Use Zot as a Docker pull-through cache: daemon registry-mirrors, the containerd image store hosts.toml per upstream, and the required sync and compat settings."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot side: the `sync` extension needs `onDemand: true` and `http.compat: ["docker2s2"]` must be enabled.

Docker daemon (`/etc/docker/daemon.json` on each host), then `sudo systemctl restart docker`:

```json
{ "registry-mirrors": ["https://myreg.example.com"] }
```

Docker Engine 25+ with the containerd image store: check `docker info | grep "Storage Driver"`; `overlayfs` means `hosts.toml` applies. Create a directory per upstream under `/etc/docker/certs.d/`, each with a `hosts.toml`. The guide covers `docker.io`, `gcr.io`, `ghcr.io`, `mcr.microsoft.com`, `public.ecr.aws`, `quay.io`, `registry.gitlab.com` and `registry.k8s.io`.

quay.io (Zot syncs to the `/quay` prefix), file `/etc/docker/certs.d/quay.io/hosts.toml`:

```toml
server = "https://quay.io"

[host."https://myreg.example.com/v2/quay"]
  capabilities = ["pull", "resolve"]
  override_path = true
```

docker.io uses `server = "https://registry-1.docker.io"` and the `/v2/docker` prefix.

No daemon restart is needed after editing `hosts.toml`. Add `push` to `capabilities` only if `docker push` should go to Zot.

## Checked

2026-11-04. Read against the zot Docker users guide (pull-through cache and containerd image store sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
