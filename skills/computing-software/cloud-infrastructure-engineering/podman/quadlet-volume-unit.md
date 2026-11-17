---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-volume-unit
name: quadlet-volume-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, volume-unit, volumename, uid, gid, mount-options, image-driver]
level: practitioner
status: docs-checked
description: "Create named volumes with a Quadlet .volume: systemd- name prefix, UID/GID versus User/Group, mount Options and Type, Copy, label and image-backed volumes."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pre-create volumes with specific options.

A `.volume` file's `[Volume]` section yields a one-time service ensuring the volume exists. `$name.volume` creates the Podman volume `systemd-$name`, served by `$name-volume.service`; `VolumeName=` overrides the volume name and `ServiceName=` the service. Containers reference it as `Volume=name.volume:/path`. Without a unit, Podman would create volumes with default options.

Ownership: `UID=` and `GID=` set who owns the volume's mount point directory (they affect the chown operation, and are not passed to mount; table: `--uid`, `--gid`). `User=` and `Group=` are host numeric IDs or names that are passed to the mount operation (`--opt "o=uid=..."`, `--opt "o=group=..."`).

Mount: `Device=` (e.g. `tmpfs`), `Type=` is the filesystem type of `Device` as in `mount -t`, and `Options=` the `mount -o` options (`--opt "o=XYZ"`). `Copy=` (default true) copies the image content at the mountpoint into the volume on first run.

Image volumes: `Driver=image` requires `Image=`, which accepts a fully qualified name with tag or digest, or a `.image` reference with a dependency on its service. `Label=` sets OCI labels; `PodmanArgs` passes extra `podman volume create` arguments.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
