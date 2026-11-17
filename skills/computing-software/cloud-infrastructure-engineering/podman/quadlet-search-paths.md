---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-search-paths
name: quadlet-search-paths
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, search-path, rootless, rootful, etc-containers-systemd, xdg-config-home, symlinks]
level: practitioner
status: docs-checked
description: "Find where Podman Quadlet looks for unit files, rootful and rootless directory precedence, per-UID admin directories, symlinks and the User= limitation."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: place a Quadlet file where the generator will read it.

Rootful, in precedence order: `/run/containers/systemd/` (temporary, usually for testing), `/etc/containers/systemd/` (administrator), `/usr/share/containers/systemd/` (distribution). A duplicate name under `/run` wins over `/etc` and `/usr`.

Rootless: `$XDG_RUNTIME_DIR/containers/systemd/`, `$XDG_CONFIG_HOME/containers/systemd/` or `~/.config/containers/systemd/`, `/etc/containers/systemd/users/${UID}`, `/etc/containers/systemd/users/`, `/usr/share/containers/systemd/users/${UID}` and `/usr/share/containers/systemd/users/`.

Administrator placement: files in `/etc/containers/systemd/users` or `/usr/share/containers/users` run for every user's session when the login session begins; files in the `${UID}` subdirectory run only for the matching user. Subdirectories are searched recursively. Symbolic links are supported both for the base of the search paths and inside them.

Quadlet units do not support running as a non-root user through the systemd `User`, `Group` or `DynamicUser` options. To run rootless, create the user and put the file in one of the rootless paths.


The administrator and distribution directories give two ways to ship units. Files under `/etc/containers/systemd/users/${UID}` apply to one numbered user; files directly under `/etc/containers/systemd/users/` apply to everyone. After placing a file run `systemctl --user daemon-reload` (or the rootful form) so the generator re-reads the directories.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
