---
id: computing-software.systems-network-administration.linux.podman-named-volumes
name: podman-named-volumes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, podman, podman-volumes, container-volumes, named-volumes, bind-mounts, selinux-volume-labels, volume-export, quadlet-volume, rootless, sysadmin]
level: practitioner
status: docs-checked
description: "Manage persistent data for Podman containers: named volumes vs bind mounts, SELinux :z/:Z and :U options, rootless storage paths, backup via volume export/import, and Quadlet .volume units."
sources:
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-volume-create.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-volume-export.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-volume-import.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-volume-prune.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/options/volume.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-systemd.unit.5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Podman volumes

**Goal:** container data that survives container replacement, has the right ownership
and SELinux labels, and can be backed up and restored.

## 1. Named volume vs bind mount
| | Named volume | Bind mount |
|---|---|---|
| Created by | `podman volume create` / first use | you (`mkdir`) |
| Location | under Podman's graph root (rootless default `${XDG_DATA_HOME}/containers/storage`); `podman volume inspect` shows the Mountpoint | anywhere |
| Initial content | copied from the image path on first use when the `copy` volume option applies (only at initial creation) | hides the image path |
| Ownership/SELinux | handled by Podman | your job (`:Z`, `:U`) |
Use named volumes for app data (databases); bind mounts for config you edit from the host.

## 2. Commands
```bash
podman volume create pgdata
podman run -d --name db -v pgdata:/var/lib/postgresql/data docker.io/library/postgres:16
podman volume ls; podman volume inspect pgdata          # Mountpoint
podman volume rm pgdata                                  # fails while in use
podman volume prune                                      # by default removes only unused ANONYMOUS volumes
podman volume prune --all --dry-run                      # --all includes named volumes; --dry-run lists what would go
podman run -v /srv/app/config:/etc/app:ro,Z ...          # bind mount, read-only, private SELinux label
podman run -v ./data:/data:U ...                         # relative host paths are allowed; :U chowns the source to the container's UID/GID
podman run --mount type=volume,src=pgdata,dst=/var/lib/postgresql/data ...
podman run --tmpfs /run:rw,size=64m ...
```
Volume options use `--opt`/`-o` key=value pairs, for example a size-limited tmpfs volume: `podman volume create --opt device=tmpfs --opt type=tmpfs --opt o=size=256m cache` (`size` is supported on tmpfs and xfs). Other filesystem types follow the same `type`/`device`/`o` pattern; see podman-volume-create(1).

## 3. Backup and restore
```bash
podman stop db                                   # consistent copy (or use the DB's dump tool live)
podman volume export pgdata --output pgdata-$(date +%F).tar     # -o is the short form; default is stdout
podman volume create pgdata-restored && podman volume import pgdata-restored pgdata-2026-10-16.tar
```
`volume import` needs the volume to exist already and merges the tarball over existing content (the tarball wins); `-` reads from stdin, so `podman volume export old | podman volume import new -` copies a volume. Rootless volume files are owned by mapped subuids on the host, so prefer `volume export`/`import` or `podman unshare` over plain host tools.

## 4. Quadlet
```ini
# ~/.config/containers/systemd/pgdata.volume
[Volume]
VolumeName=pgdata
# db.container
[Container]
Volume=pgdata.volume:/var/lib/postgresql/data
```
Quadlet generates `pgdata-volume.service`, and a container whose `Volume=` source ends in `.volume` depends on it. Without `VolumeName=` the Podman volume is named `systemd-<name>`.

## Gotchas
- `:Z` gives the content a private label for that container and relabelling walks the whole tree; use `:z` when several containers share the content, and never relabel system directories.
- `podman volume prune --all`, `volume rm` and `podman system reset` delete data.
- The `copy` option copies image content only at the volume's initial creation; it is not repeated when the volume is later used by other containers, and it has no effect on bind mounts.

## Verify
- [ ] `podman rm -f db && podman run ... -v pgdata:...` brings back the same data.
- [ ] A restore from `volume export` into a new volume starts the app with the expected data.

## Checked
Checked 2026-10-25 against the Podman documentation source on GitHub (containers/podman docs/, main, last commit 2026-10-23; latest release v5.8.9 of 2026-10-12): `podman volume create --opt device/type/o` with `size` support on tmpfs and xfs, `volume export --output/-o`, `volume import` semantics (volume must exist, tarball precedence, `-` for stdin), `volume prune` default (anonymous only) with `--all` and `--dry-run`, `-v` syntax including `:ro`, `:z`/`:Z`, `:U`, relative host paths and the `copy` option, `--mount type=volume`, `--tmpfs`, Quadlet `.volume` units with `VolumeName=`, `systemd-` default names and the `<name>-volume.service` dependency. Fixed: the skill said `volume prune` removes all unused volumes; by default it removes only anonymous ones. Removed unconfirmed claims: the exact on-disk volume path, the NFS option example and the copy-up-when-empty rule.

Method: documentation only; no commands were run.
