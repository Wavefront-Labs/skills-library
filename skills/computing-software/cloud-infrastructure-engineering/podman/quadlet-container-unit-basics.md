---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-unit-basics
name: quadlet-container-unit-basics
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, container-unit, image, containername, servicename, podman-run, systemd]
level: intro
status: docs-checked
description: "Write a minimal Quadlet .container: required Image key, systemd- name prefix, ContainerName and ServiceName overrides, and how keys map to podman run options."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a container as a service.

A `.container` file contains a `[Container]` section; the generated service has an `ExecStart=podman run ... image-name` line. Most keys translate to `podman run` options (the page has a table), though some also affect how systemd runs the container. The only required key is `Image`.

Naming: `$name.container` creates `$name.service` and a Podman container called `systemd-$name`. The prefix avoids conflicts with user-managed containers; override the container name with `ContainerName=`. The default expressed in the page is `systemd-%N`. `ServiceName=` changes the systemd unit name from the Quadlet name; do not include the `.service` extension.

`Image=` takes the same format as `podman pull` (tags or digests). A fully qualified name is recommended for performance and robustness. If it ends in `.image` Quadlet uses the image pulled by that `.image` file and depends on `$name-image.service`; if it ends in `.build` it uses the image built by that `.build` file and depends on `$name-build.service`. The referenced file must exist.

`Exec=` adds arguments after the image, like `podman run <image> <arguments>`; it combines with the image's ENTRYPOINT or CMD, like a Kubernetes pod `args` field. `Entrypoint=` maps to `--entrypoint`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
