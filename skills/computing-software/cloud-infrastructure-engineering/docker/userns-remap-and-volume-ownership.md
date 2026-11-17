---
id: computing-software.cloud-infrastructure-engineering.docker.userns-remap-and-volume-ownership
name: userns-remap-and-volume-ownership
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-namespaces, userns-remap, userns, userns-remap-config, dockremap, subuid-ranges, subordinate-ids, userns-host, remapped-volume-ownership, userns-permissions, remapped-ownership, userns-limitations, rootless-permissions, subuid-mapping]
level: advanced
description: "Enable userns-remap with dockremap and subuid/subgid ranges, fix bind-mount ownership under remapping or rootless mode, opt out with --userns=host, and know the limits."
sources: ["https://docs.docker.com/engine/security/userns-remap/", "https://docs.docker.com/engine/security/rootless/uid-gid-mapping/", "https://docs.docker.com/reference/compose-file/services/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# userns-remap and volume ownership

## Enable remapping
```json
{ "userns-remap": "default" }
```
`default` creates user/group `dockremap` and entries like:
```
# /etc/subuid and /etc/subgid
dockremap:231072:65536
```
Container UID 0 -> host UID 231072, container 1000 -> host 232072 (first subuid + n). A process
escaping the namespace runs as an unprivileged high-numbered host UID. Use a named user instead (`"userns-remap": "svc-docker"`)
with your own ranges; ranges must not overlap other users'.

Restart dockerd (or use `dockerd --userns-remap`; `daemon.json` is the recommended method). Data-root moves to `/var/lib/docker/231072.231072/` - **existing images and
containers disappear** from view (they're under the old root). Re-pull; plan it as a migration.

## Ownership on volumes and bind mounts
Files written by container root appear on the host owned by 231072. Bind-mounting a host
directory owned by 1000 gives container processes "permission denied" because inside it
shows as `nobody` (65534 - unmapped).

Fix the host side to the shifted IDs:
```sh
sudo chown -R 232072:232072 /srv/appdata     # container uid/gid 1000 with the 231072 range above
```
From a security standpoint the docs advise avoiding host paths that the remapped user cannot write to.

**Rootless Docker** uses the same mechanism per user: container root = your UID, container
UID n>=1 = your subuid start + (n - 1). Files owned by your host user appear as owned by `root`
inside the container.

## Opting out per container
```sh
docker run --userns=host --privileged ...       # needed for --privileged, host PID/net with some tools
```
`--userns=host` (accepted by `docker container create`, `run` and `exec`) disables remapping for that
container - it's root on the host again. Because read-only image layers are shared, the container
filesystem then still belongs to the remap user (231072 here), which can surprise programs inside.
Compose: `userns_mode: "host"`.

## Limitations
- `--pid=host` and `--network=host` are incompatible with a user-namespaced daemon; `--privileged`
  needs `--userns=host`.
- External volume or storage drivers that do not understand the daemon's mappings are incompatible.
- Root inside the namespace cannot `mknod` (device creation is denied).
- Sharing volumes between remapped containers and non-remapped processes needs the offset math.

## Verify
```sh
sudo ls -ld /var/lib/docker/231072.231072/                             # owned by 231072:231072, mode drwx------
docker inspect -f '{{.HostConfig.UsernsMode}}' t                       # per-container mode (host when opted out)
docker info -f '{{.SecurityOptions}}'                                  # includes name=userns
```

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: userns-remap page, UID/GID mapping page, Compose services reference), Docker Engine API (HostConfig.UsernsMode, SecurityOptions).
- Confirmed `userns-remap` values (`default` creates `dockremap`; named user, `user:group`, IDs), `/etc/subuid` entry format and the `dockremap:231072:65536` example, the `/var/lib/docker/231072.231072/` directory and the masking of existing images, the `--userns=host` opt-out and its shared-layer side effect, and the listed incompatibilities.
- Confirmed rootless mapping (container root = host user, UID n = subuid + (n - 1)) and Compose `userns_mode`.
- Removed the `awk` offset script, `rootlesskit chown`/Podman commands, NFS, `docker cp` and per-container-range claims, none of which a checked source covers.
Method: documentation only; no commands were run.
