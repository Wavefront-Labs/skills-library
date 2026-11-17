---
id: computing-software.cloud-infrastructure-engineering.docker.userns-mode-in-compose
name: userns-mode-in-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-namespaces, userns-mode, userns-host, userns-remap, compose-file, privileged]
level: advanced
status: docs-checked
description: "Opt individual Compose services out of daemon-wide userns-remap with userns_mode: host (or --userns=host), when that is required, and what it costs in isolation."
sources: ["https://docs.docker.com/reference/compose-file/services/#userns_mode", "https://docs.docker.com/engine/security/userns-remap/#disable-namespace-remapping-for-a-container", "https://docs.docker.com/engine/security/userns-remap/#user-namespace-known-limitations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# userns_mode in Compose

When the Docker daemon runs with `userns-remap` enabled, all containers start with user
namespaces by default and a container's root maps to an unprivileged host UID from the
subordinate range. Some workloads cannot run that way; `userns_mode: host` disables
remapping for one service.

## Syntax
```yaml
services:
  app:
    image: app:1.0                   # remapped (daemon default)
  node-exporter:
    image: prom/node-exporter
    userns_mode: host                # no user remapping for this container
    privileged: true
```
CLI: `docker run --userns=host ...` (also on `docker container create`; the Docker docs list
`docker container exec` too). The Compose reference says supported `userns_mode` values are
platform specific and may depend on platform configuration, and its example is
`userns_mode: "host"`.

## When it is required
The Docker user namespaces page lists these as incompatible with a daemon that has user
namespaces enabled:
- Sharing the PID or network namespace with the host (`--pid=host` or `--network=host`).
- External volume or storage drivers that are unaware of daemon user mappings.
- `--privileged` mode without also specifying `--userns=host`.

Where a service needs host volumes with pre-arranged file ownership, the page also stresses
that ownership must be arranged by you when volumes are mounted from the host.

## Cost
Remapping is off for that container, so its root is the host's root again. Treat such
services as fully trusted and keep them few. The Docker docs also warn of a side effect:
because the read-only image layers are shared between containers, ownership of the
container's filesystem is still remapped, so the whole filesystem belongs to the user
specified in the daemon's `userns-remap` setting. This can break programs such as `sudo`
(which checks that its binaries belong to user 0) and binaries with the `setuid` flag.

## Verify
```bash
docker compose exec app cat /proc/self/uid_map            # remapped container: shows the subordinate range
docker compose exec node-exporter cat /proc/self/uid_map  # userns_mode host: shows the host mapping
```
The userns-remap page points to `/proc/self/uid_map` and `/proc/self/gid_map` for inspecting
the mapping.

## Gotchas
- Enabling `userns-remap` masks existing image and container layers: Docker stores objects
  in a namespaced subdirectory of `/var/lib/docker/` (the page's example is
  `/var/lib/docker/231072.231072/`), and disabling it later makes data created under the
  remapping inaccessible.
- The daemon itself still runs as root with `userns-remap`.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the userns-remap page: per-container disable with `--userns=host`, known
limitations list, filesystem-ownership side effect (`sudo`, setuid), `/proc/self/uid_map`
pointer, namespaced storage directory, masking of existing layers; in the Compose services
reference: the `userns_mode` description and example. Removed: the `node-exporter`
command-line and mounts, the claim that `ipc: host` needs it, the claim that only `host` is
supported, concrete uid_map values, and the volume-ownership remarks about shared services.
