---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.docker-host-and-container-forensics
name: docker-host-and-container-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [docker-forensics, container-forensics, linux-forensics, overlay2, dfir]
level: advanced
status: docs-checked
description: "Investigate a Docker host from a disk image: overlay2 layer directories, the container upperdir, json-file logs and their rotation, and docker-explorer usage."
sources: ["https://docs.docker.com/engine/storage/drivers/overlayfs-driver/", "https://github.com/google/docker-explorer", "https://docs.docker.com/engine/logging/drivers/json-file/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker host and container forensics

**Goal:** reconstruct what ran in a compromised container by working on the host's Docker data directory, ideally from a mounted disk image.

## overlay2 layout (Docker storage driver page)
- OverlayFS layers two directories and presents them as one: `lowerdir` (lower), `upperdir` (upper), exposed as `merged`.
- Image layers are the read-only lowerdirs. The container gets a new writable directory, the upperdir. Where both contain a file, the upperdir copy wins and hides the image one.
- Layer directories live under `/var/lib/docker/overlay2`. The lowest layer holds `link` (its shortened identifier) and `diff` (its contents). Higher layers hold `diff`, `link`, `lower` (names the parent), `merged` and `work` (used internally by OverlayFS).
- `/var/lib/docker/overlay2/l` holds symlinks from short identifiers to each layer's `diff` directory.
- A running container's mount shows `lowerdir=`, `upperdir=<id>/diff` and `workdir=<id>/work`, so the upperdir `diff` directory is where the container's own changes are.
- Docker warns not to manipulate files under `/var/lib/docker/` directly: work on an image or copy, not the live directory.

## Container logs (json-file driver page)
- By default Docker writes each container's stdout and stderr to a JSON file, one container per file. Each line carries `log`, `stream` (stdout or stderr) and `time`.
- `max-size` (default -1, unlimited) and `max-file` (default 1; only effective with `max-size`) control rotation: when rolled files exceed the limit the oldest is removed, so log history can be incomplete. `compress` optionally compresses rotated logs.
- Daemon-level settings go in `daemon.json` (`log-driver`, `log-opts`) and apply to newly created containers only; a container can override with `--log-driver` / `--log-opt`. Another driver may be in use, so confirm which.

## docker-explorer (README)
- Purpose: explore offline Docker filesystems of a compromised container; supports AuFS and OverlayFS backends.
- With the host disk mounted at `/mnt/root`:
  - `de.py -r /mnt/root/var/lib/docker list running_containers` prints container id, image id, image name, start date.
  - `de.py -r <docker-root> mount <container_id> <mountpoint>` mounts the container filesystem. The README example is for AuFS and needs `aufs-tools`; for other drivers check the tool's own output.
  - `de.py -r <docker-root> history <image_id>` shows the image history (creating commands, sizes).
- README workflow: find the container ID, mount its filesystem (e.g. `/mnt/container`), then run `log2timeline.py` on it or inspect it directly (`ls -lta /mnt/container/tmp`).
- On a live host, `docker ps`, `docker commit` and `docker history` show similar information; `docker commit` creates a new image and so changes host state.

## Analysis approach
- Compare each container's upperdir `diff` against the image layers to list files it added or changed.
- Correlate log timestamps with the container start date from docker-explorer.

## Gotchas
- Rotated logs may be gone; record the logging options in force.
- Container configuration files, volumes, daemon logs and escape indicators are not covered by the cited pages: verify them against Docker documentation for your version.

## Verify
Each relevant container has its upperdir, logs and image history preserved and reviewed.

## Checked
Date: 2026-11-08.
Confirmed in the overlayfs page: lower/upper/merged/work roles, `link`, `lower`, `diff`, `l` symlinks, mount options, precedence, do-not-touch warning. Confirmed in the json-file page: format, defaults and meaning of `max-size`, `max-file`, `compress`, per-container flags, newly created containers only. Confirmed in the docker-explorer README: commands, AuFS/OverlayFS support, workflow.
Removed (not on the cited pages): `data-root`, `config.v2.json`, `hostconfig.json`, `layerdb`, `volumes/<name>/_data`, `docker.service`, privileged and capability indicators, TCP 2375 exposure, `docker exec` and `docker logs` remarks, removed-container carving.
Method: docs-only read of cited pages, 2026-11-08
