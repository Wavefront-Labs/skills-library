---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-build-unit
name: quadlet-build-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, build-unit, imagetag, containerfile, build-arg, setworkingdirectory, podman-build]
level: practitioner
status: docs-checked
description: "Build images locally with a Quadlet .build: minimum ImageTag plus File or SetWorkingDirectory, referencing from .container Image=, caching on restart, mapped build keys."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have systemd build an image before a container needs it.

A `.build` file's `[Build]` section yields a one-time service that ensures the image is built from a supplied Containerfile and context directory. Later restarts usually finish quickly because layer caching skips unchanged steps. A minimal unit needs `ImageTag=` and either `File=` or `SetWorkingDirectory=`. Containers and volumes can depend on it: set `Image=name.build` in the container and Quadlet depends on `$name-build.service`. The use cases named are images not available on registries and local testing.

Keys from the table: `ImageTag=` (`--tag`), `File=` (`--file`), `BuildArg=` (`--build-arg`), `Target=` (`--target`, skips later stages), `Arch=`, `Variant=`, `Annotation=`, `Label=`, `Environment=`, `Network=`, `Volume=`, `Secret=` (`--secret=id=mysecret,src=path`), `AuthFile=`, `TLSVerify=`, `Pull=`, `Retry=`, `RetryDelay=`, `IgnoreFile=`, `ForceRM=`, `DNS`, `DNSOption`, `DNSSearch`, `GroupAdd=`, and `SetWorkingDirectory=` (e.g. `unit`) to set the unit's `WorkingDirectory`. `PodmanArgs=` appends extra arguments.


Example values from the table: `File=/path/to/Containerfile`, `ImageTag=localhost/imagename`, `BuildArg=foo=bar`, `Target=my-app`, `Variant=arm/v7`, `Arch=aarch64`, `TLSVerify=false`, `Retry=5`, `RetryDelay=10s`, `Pull=never`. `ForceRM=false` maps to `--force-rm=false`, and `IgnoreFile=/path/to/.customignore` to `--ignorefile`, so a build unit can express most of a `podman build` command line.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed. Wording tightened where the page is softer than the draft.
Method: documentation only; no commands were run.
