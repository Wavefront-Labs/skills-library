---
id: computing-software.devops-ci-cd.earthly.earthly-podman-frontend
name: earthly-podman-frontend
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, podman, container-frontend, podman-shell, rootful, with-docker, locally, qemu]
level: practitioner
status: docs-checked
description: "Run Earthly on Podman: set global.container_frontend to podman-shell, rootful mode for WITH DOCKER, Mac podman machine resources, and fixes for common errors."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/podman.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using Earthly with Podman

Goal: use Podman instead of Docker as Earthly container frontend.

## Prerequisites

- Install Podman. On Mac a podman machine must be running.
- Linux multi-platform builds need `qemu-user-static`.
- `WITH DOCKER` requires rootful mode: on Linux run with `sudo` (`sudo earthly -P +with-docker-target`); on Mac use a rootful machine.

## Choose the frontend

At startup Earthly tries docker, then falls back to podman. To force it:

```bash
earthly config global.container_frontend podman-shell
# or back to docker
earthly config global.container_frontend docker-shell
```

This writes a `container_frontend` entry under `global:` in `~/.earthly/config.yml`. Check with `earthly github.com/earthly/hello-world:main+hello`: it should print `Starting buildkit daemon as a podman container (earthly-buildkitd)...`.

## Troubleshooting

- `No frontend initialized` (Mac): the podman machine is probably not running; `podman machine start`.
- Slow builds on Mac: machines used one core and 2GB RAM by default when the docs were written. Resize:
  ```bash
  podman machine init --now --cpus 5 --disk-size 128 --memory 8196
  podman machine stop ; podman machine set --cpus 5 --disk-size 128 --memory 8196 && podman machine start
  ```
  Also compare the OS/Arch of client and server in `podman version` (to rule out emulation) and look for `graphDriverName: overlay` in `podman info --debug` (VFS and similar drivers perform poorly).
- `docker-credential-desktop: executable file not found in $PATH` (Mac, after leaving Docker Desktop): remove or rename `~/.docker/config.json`.
- Rootless podman is not supported, since earthly/dind and earthly/buildkitd need privileged access; `WITH DOCKER` will fail.
- Inside `WITH DOCKER` use the docker CLI; the podman CLI only works if the target uses `LOCALLY`:
  ```bash
  docker-locally:
     LOCALLY
     WITH DOCKER
       RUN podman ps
     END
  ```
- Cross-platform target fails with `exec /bin/sh: exec format error`: QEMU is not configured; install `qemu-user-static` (apt-get or yum).
- `crun: open executable: Permission denied: OCI permission denied`: a binary run directly or referenced by `ENTRYPOINT` lacks the execute permission.

## Checked

2026-11-07. Read docs/guides/podman.md in full. Prerequisites, config commands and troubleshooting items match. Corrected: the one-core, 2GB default is qualified as true when the docs were written.
Method: documentation only; no commands were run.
