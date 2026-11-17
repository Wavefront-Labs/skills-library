---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-template-units
name: quadlet-template-units
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, template, instance, defaultinstance, specifier, volume-reference, systemd]
level: advanced
status: docs-checked
description: "Create templated Quadlets like foo@.container, instantiate them with systemctl, drop-in directories or symlinks, DefaultInstance, and reference template volumes from containers."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run many instances from one Quadlet.

A file named `foo@.container` generates `foo@.service`; start an instance with `systemctl start foo@bar.service`. Alternatively an instance-specific drop-in directory such as `foo@instance.container.d/` creates the instance from `foo@.container` without a `foo@instance.container` file or symlink; an empty directory is enough, and the instance inherits the template's settings and drop-ins, including `[Install]`. An explicit instance file or symlink takes precedence. A drop-in directory without a matching template creates nothing. When generating an instance Quadlet reads drop-ins from both `foo@instance.container.d` and `foo@.container.d`.

Enabling: instanced files can be enabled like normal ones; a bare template only gets enabled if `[Install]` has `DefaultInstance=`.

Example `sleep@.container`: `Image=quay.io/fedora/fedora`, `Exec=sleep %i`, `Restart=always` under `[Service]`, and `WantedBy=multi-user.target` plus `DefaultInstance=100` under `[Install]`. `sleep@10.container.d/10-image.conf` with `Image=quay.io/centos/centos` creates a 10 second instance on another image.

Referencing templates: write `Volume=foo-data@.volume:/mnt/path` (template name, not `foo-data@%i.volume`); Quadlet resolves it to the right per-instance volume name.


The `%i` specifier expands to the instance name, as the `Exec=sleep %i` line shows.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
