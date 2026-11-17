---
id: computing-software.cloud-infrastructure-engineering.docker.troubleshooting-userns-remapped-containers
name: troubleshooting-userns-remapped-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-namespaces, userns-troubleshooting, userns-remap, subuid-ranges, remapped-ownership, nfs]
level: advanced
status: docs-checked
description: "Fix problems after enabling userns-remap: images 'disappeared', nobody-owned bind mounts, privileged and host-namespace errors, NFS root squash, and subuid range mistakes."
sources: ["https://docs.docker.com/engine/security/userns-remap/", "https://github.com/moby/moby/blob/master/daemon/daemon_unix.go", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting userns-remapped containers

## Confirm remapping is active
```bash
docker info -f '{{.SecurityOptions}}'          # contains name=userns
docker run --rm alpine cat /proc/self/uid_map  # 0 <first subuid> 65536
grep dockremap /etc/subuid /etc/subgid         # e.g. dockremap:231072:65536
```

## Symptoms and fixes
| Symptom | Cause | Fix |
|---|---|---|
| All images and containers gone after enabling | Remapped daemon uses `/var/lib/docker/231072.231072/` (named after the remap UID/GID) | Expected; re-pull, recreate. Disabling remap hides the remapped ones |
| Bind-mounted files show as an unmapped owner | Host UIDs outside the mapped range | `chown` host dirs to first subuid + container uid, e.g. 232072 for container uid 1000 with a 231072 range |
| Container root cannot write to a bind mount | Host dir not writable by the remap user | `chown` it to the first subuid (231072) or adjust permissions for the remap user |
| `privileged mode is incompatible with user namespaces` | `--privileged` on remapped daemon | Add `--userns=host` for that container |
| `cannot share the host's network namespace when user namespaces are enabled` | `--network host` | `--userns=host` |
| `cannot share the host PID namespace when user namespaces are enabled` | `--pid host` | `--userns=host` |
| `operation not permitted` / permission denied on `mknod` | Kernel restricts device creation for root in a user namespace | Redesign, or `--userns=host` for the trusted container |
| `Error during uid lookup for "<name>"` at daemon start | The named remap user does not exist in /etc/passwd | Create the user, or use `"userns-remap": "default"` so Docker creates `dockremap` |
| Overlapping ranges | Same subuid range given twice | Non-overlapping ranges in `/etc/subuid` and `/etc/subgid` for each user |

## Ownership arithmetic
Host UID = first subuid in the remap range + container UID (container UID 0 maps to the first one).
With `dockremap:231072:65536`, container uid 1000 is host uid 232072:
```bash
sudo chown -R 232072:232072 /srv/app-data
```
Docker uses only the first five mappings if a user has several ranges (kernel limit on `uid_map` entries).

## Gotchas
- External volume or storage drivers that are unaware of the daemon's user mappings are incompatible.
- If you disable `userns-remap` you cannot access resources created while it was enabled; enable it on
  a fresh install where possible.
- A named remap user must already exist; the ranges must not overlap.

## Checked
Date: 2026-10-24. Documentation: Docker docs userns-remap page (docker/docs main), moby/moby `daemon/daemon_unix.go` (master), Docker Engine API (SecurityOptions).
- Confirmed the exact error strings for `--privileged`, `--network=host` and `--pid=host` on a user-namespaced daemon, and the "Error during uid lookup for" message for a missing remap user, in `daemon_unix.go`.
- Confirmed the `dockremap:231072:65536` example, the `/var/lib/docker/<uid>.<gid>/` directory, masking of existing images, the first-five-mappings limit, the `mknod` restriction and the volume-driver limitation in the userns-remap page; `name=userns` in `docker info` SecurityOptions.
- Removed NFS, `docker cp`, awk and range-change claims that no checked source covers; replaced the 100000 example range with the documented 231072.
Method: documentation only; no commands were run.
