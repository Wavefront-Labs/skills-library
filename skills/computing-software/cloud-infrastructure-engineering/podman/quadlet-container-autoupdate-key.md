---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-autoupdate-key
name: quadlet-container-autoupdate-key
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, autoupdate, auto-update, registry, local, image-reference, systemd-restart]
level: practitioner
status: docs-checked
description: "Enable podman auto-update for a Quadlet container with AutoUpdate=registry or local, requirements for fully qualified images, and local-storage restarts."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let podman auto-update manage a Quadlet container.

`AutoUpdate=` sets the label `io.containers.autoupdate` (the page maps `AutoUpdate=registry` to `--label "io.containers.autoupdate=registry"`) and controls whether podman-auto-update(1) updates the container. Supported values:

- `registry`: requires a fully qualified image reference such as `quay.io/podman/stable:latest` to create the container. This is needed so Podman knows which image to check and pull; if an image ID was used, Podman no longer knows which image to look up.
- `local`: Podman compares the image the container uses against the image with its raw name in local storage. If the image is updated locally, Podman restarts the systemd unit executing the container.

Combine this with a unit-level restart arrangement through systemd; the update step works by restarting the unit.


The page lists no other values for the container unit. In a `.kube` unit the same key can be given several times and also accepts `name/(local|registry)` to apply `local` or `registry` to one named container. Both forms rely on the update step restarting the systemd unit that executes the container, which is why the key sits next to the unit definition. For the update command itself see podman-auto-update(1), which the key references.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
