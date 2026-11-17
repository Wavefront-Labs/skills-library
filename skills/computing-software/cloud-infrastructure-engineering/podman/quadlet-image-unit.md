---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-image-unit
name: quadlet-image-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, image-unit, image-pull, policy, creds, tlsverify, imagetag]
level: practitioner
status: docs-checked
description: "Pull images ahead of containers with a Quadlet .image: Image and ImageTag keys, pull policy, credentials, TLS and cert settings, retries and the .image reference rule."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pre-pull and name images through systemd.

An `.image` file's `[Image]` section generates a one-time service that ensures the image exists on the host, pulling it if needed. Containers and volumes can then depend on it (`Image=name.image`), which suits special pull options. This also avoids slow pulls inside a container unit that could hit the start timeout.

Keys from the table: `Image=` (the reference to pull), `ImageTag=` (the name used when resolving `.image` references), `AllTags=true` (`--all-tags`), `Arch=`, `OS=`, `Variant=`, `Policy=always` (`--policy`), `Creds=` (`--creds`), `AuthFile=`, `CertDir=`, `DecryptionKey=`, `TLSVerify=false`, `Retry=` and `RetryDelay=`, `ServiceName=`, `GlobalArgs=`, `PodmanArgs=` (e.g. `--os=linux`).

Because `Mount=type=image,source=name.image` and `Volume` with `Driver=image` both accept `.image` references, a single image unit can feed several consumers, each getting a dependency on its service. Note that the corresponding `.image` file must exist for any such reference.


Examples from the table: `Image=quay.io/centos/centos:latest`, `ImageTag=quay.io/centos/centos:latest`, `Policy=always`, `Creds=myname:mypassword`, `CertDir=/etc/registry/certs`, `AuthFile=/etc/registry/auth.json`, `DecryptionKey=/etc/registry.key`, `Arch=aarch64`, `OS=windows`, `Variant=arm/v7`, `AllTags=true`.

`ServiceName=name` renames the generated service to `name.service`; otherwise the usual `$name-image.service` applies, which is the dependency container units get.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
