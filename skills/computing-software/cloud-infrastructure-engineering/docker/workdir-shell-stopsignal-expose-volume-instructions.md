---
id: computing-software.cloud-infrastructure-engineering.docker.workdir-shell-stopsignal-expose-volume-instructions
name: workdir-shell-stopsignal-expose-volume-instructions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, workdir, shell-instruction, stopsignal, volume-instruction, expose, dockerfile-instructions, pipefail]
level: practitioner
description: "Correct use of the secondary Dockerfile instructions: WORKDIR semantics, SHELL with pipefail, STOPSIGNAL for clean shutdown, EXPOSE as documentation, and why VOLUME is usually a mistake."
sources: ["https://docs.docker.com/reference/dockerfile/#workdir", "https://docs.docker.com/reference/dockerfile/#shell", "https://docs.docker.com/reference/dockerfile/#stopsignal", "https://docs.docker.com/reference/dockerfile/#expose", "https://docs.docker.com/reference/dockerfile/#volume"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WORKDIR, SHELL, STOPSIGNAL, EXPOSE and VOLUME

**Goal:** use the smaller Dockerfile instructions precisely, and avoid the one (VOLUME)
that creates surprises for everyone downstream.

## WORKDIR
- Sets the working directory for the `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions
  that follow. If the directory does not exist it is created, even if no later instruction uses it.
- Relative paths chain: `WORKDIR /a`, `WORKDIR b`, `WORKDIR c` makes `RUN pwd` print `/a/b/c`.
- Resolves variables set earlier with `ENV` (only variables set in the Dockerfile):
  `ENV DIRPATH=/path` then `WORKDIR $DIRPATH/$DIRNAME` gives `/path/$DIRNAME` when `DIRNAME` is unset.
- Without it the default working directory is `/` (a base image may set its own); the reference
  recommends setting `WORKDIR` explicitly.
- A container's working directory can be overridden with `docker run -w` / `--workdir`
  and `docker exec -w`.
- Use it instead of `RUN cd ...`, which only affects that one `RUN`.
- The `WorkdirRelativePath` build check flags a relative `WORKDIR` path.

## SHELL
The default is `["/bin/sh", "-c"]` on Linux and `["cmd", "/S", "/C"]` on Windows. It must be
written in JSON form, can appear several times, each one overrides the previous and affects all
later instructions. It applies to the shell form of `RUN`, `CMD` and `ENTRYPOINT` only, not to
exec form. It is most useful on Windows to switch between `cmd` and `powershell`:
```dockerfile
SHELL ["powershell", "-command"]
RUN Write-Host hello
```

## STOPSIGNAL
```dockerfile
STOPSIGNAL SIGQUIT
```
Sets the signal sent to the container to stop it: a name such as `SIGKILL` or an unsigned number
from the kernel's syscall table such as `9`. Default is `SIGTERM`. It applies to `docker stop`
(and the daemon stopping a container), not to Ctrl+C, which sends `SIGINT` directly. Override per
container with `--stop-signal` on `docker run` or `docker create`.
`docker stop` waits for the stop timeout before killing: 10 seconds by default for Linux
containers, adjustable with `--stop-timeout` / `-t`. In Compose the grace period is
`stop_grace_period` and the signal is `stop_signal`.

## EXPOSE
```dockerfile
EXPOSE 8080
EXPOSE 53/udp
```
Documentation between the image builder and the person running the container about which ports
are intended to be published; the protocol defaults to TCP. It does **not** publish anything. Use
`-p` on `docker run` to publish and map ports, or `-P` to publish all exposed ports to
high-order host ports (a TCP and a UDP entry for the same number get different host ports).
`-p` works regardless of `EXPOSE`.

## VOLUME: think twice
```dockerfile
VOLUME /var/lib/data
```
Creates a mount point and marks it as holding externally mounted volumes. `docker run`
initializes the new volume with whatever exists at that path in the image. Things to know:
- Each container started without an explicit mount at that path gets a new anonymous volume.
  `docker rm -v` / `--volumes` removes a container's anonymous volumes (named volumes are kept),
  and `docker volume prune` removes unused anonymous volumes by default (`--all` includes named).
- Changing data in the volume path in later build steps is discarded with the legacy builder; with
  BuildKit the changes are kept.
- The host directory cannot be given in the Dockerfile; you specify the mount at `docker run` or
  create time.
- On Windows containers the destination must be a non-existing or empty directory, or a drive
  other than `C:`.
- The list form is JSON: double quotes only.

## Verify
```sh
docker inspect --format '{{.Config.WorkingDir}} {{.Config.StopSignal}} {{.Config.ExposedPorts}} {{.Config.Volumes}}' img
docker build --check .
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (WORKDIR, SHELL, STOPSIGNAL, EXPOSE, VOLUME; moby/buildkit docs main), the docker/cli reference for `docker run`, `docker rm` and `docker volume prune`, and the Compose services reference.
Confirmed: WORKDIR creation, chaining and ENV expansion; SHELL defaults and scope; STOPSIGNAL values, default, Ctrl+C note and override; EXPOSE semantics with `-p`/`-P`; VOLUME initialisation, legacy-versus-BuildKit behaviour, Windows restriction; 10 second Linux stop timeout. Removed unconfirmed claims (root ownership of created WORKDIR, SIGQUIT-for-nginx, proxy port guessing, `--read-only` behaviour, official database images).

Method: documentation only; no commands were run.
