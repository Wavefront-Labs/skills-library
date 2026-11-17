---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-file-types-and-generator
name: quadlet-file-types-and-generator
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, systemd, generator, container-unit, service-files, daemon-reload, podman]
level: intro
status: docs-checked
description: "How Podman Quadlet turns .container, .volume, .network, .build, .pod, .kube and .artifact files into systemd services via the generator, and what passes through."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what Quadlet does with your files.

Quadlet is a systemd generator. At boot, and whenever `systemctl daemon-reload` runs, it reads files with the extensions `.container`, `.volume`, `.network`, `.build`, `.pod`, `.kube` and `.artifact` (the synopsis also lists `.image`) and writes a similarly named `.service` file for each. Generated services are managed with `systemctl` like any other; `systemctl --user list-unit-files` lists a user's units. For a login shell of `/sbin/nologin`, use `sudo systemctl --machine username@ --user list-unit-files`.

The files use ordinary systemd syntax. Each type has its own section handled by Podman (for example `[Container]`); every other section such as `[Unit]`, `[Service]` and `[Install]` is passed to systemd untouched, so normal dependency and cgroup options work. Existing vendor services under `/usr/` are replaced when they share a name.

Type summary: `.build` builds an image from a Containerfile, `.container` defines one container, `.image` pulls and caches an image, `.kube` deploys Kubernetes YAML, `.network` creates a network, `.pod` creates a pod, `.volume` ensures a named volume exists.

Quadlet requires cgroup v2. Check with `podman info --format {{.Host.CgroupsVersion}}`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
