---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-drop-ins
name: quadlet-drop-ins
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, drop-in, override, conf, dash-prefix, systemd, configuration]
level: advanced
status: docs-checked
description: "Override and extend Quadlet units with drop-in directories: foo.container.d, type-level container.d, dash-prefix directories and override order."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change a unit without editing its base file.

For `foo.container`, Quadlet scans the directory `foo.container.d` for files ending in `.conf` and merges them into the base file in alphabetical order. Top-level type drop-ins in `container.d` are included too. If the name contains dashes, directories made by truncating the name after each dash are also searched: for `foo-bar-baz.container` that means `foo-.container.d` and `foo-bar-.container.d`.

Files with the same name further down the hierarchy override those further up. For example `foo-bar-baz.container.d/10-override.conf` overrides `foo-bar-.container.d/10-override.conf`, which overrides `foo-.service.d/10-override.conf` (as written on the page), which overrides `container.d/10-override.conf`.

Drop-in files use the same format as the base file, so they can add or alter `[Container]` keys as well as `[Service]` or `[Install]` settings. The `[Install]` section may be entirely in a drop-in, a way to ship a unit that is installed but not enabled.


Practical layout: put shared settings in a type-wide directory such as `container.d/`, per-family settings in a dash-truncated directory such as `foo-.container.d/`, and per-unit overrides in `foo-bar-baz.container.d/`. Names such as `10-override.conf` sort alphabetically, so the numeric prefix controls merge order inside one directory.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
