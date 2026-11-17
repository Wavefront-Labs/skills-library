---
id: computing-software.cloud-infrastructure-engineering.docker.zombie-reaping-and-the-init-flag
name: zombie-reaping-and-the-init-flag
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pid1, tini, init, zombie-processes, zombie-reaping, subreaper, init-flag, docker-init-flag]
level: advanced
description: "Diagnose zombie build-up and ignored SIGTERM under PID 1, then fix with docker run --init, Compose init true, tini -s subreaper mode or a baked-in init."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/#init", "https://docs.docker.com/reference/cli/dockerd/", "https://github.com/krallin/tini", "https://github.com/compose-spec/compose-spec/blob/main/spec.md#init"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zombie reaping and the --init flag

## The problem
PID 1 in a namespace has two jobs most apps don't do:
1. **Reap orphans.** Children that exit after their parent died are re-parented to PID 1;
   if it never calls `wait()`, they stay `<defunct>` and eventually exhaust `pids-limit`.
2. **Signals.** Linux treats PID 1 specially: it ignores any signal with the default action, so it does not terminate on SIGINT or SIGTERM unless it is coded to do so (Docker's attach reference says this).

Symptoms: `ps -eo pid,ppid,stat,cmd` shows `Z` entries and `docker stop` has to fall back to killing the container after its timeout.

## Fix 1: --init (no image change)
```sh
docker run --init app:1
```
```yaml
services:
  app:
    init: true
```
Docker runs an init process as PID 1 that forwards signals and reaps processes. The default is the first `docker-init` executable found in the daemon's path, backed by tini and included in the default installation. Daemon-wide default: `{"init": true}` in daemon.json; custom binary via `"init-path"` (`--init-path`).

## Fix 2: bake tini into the image
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
CMD ["serve"]
```
On Debian (Buster or newer) the package installs `/usr/bin/tini`. Alpine: `apk add --no-cache tini` installs `/sbin/tini`. `tini -g` kills the child process group so every process in it receives the signal.

## Subreaper mode
When tini cannot be PID 1, register it as a process subreaper (Linux 3.4 or newer) with `tini -s -- cmd` or by setting the `TINI_SUBREAPER` environment variable; zombies are then re-parented to tini even though it is not PID 1.

## When you don't need it
- The app is a single process that handles SIGTERM and never forks.
- The image already runs its own init or supervisor; check that product's documentation before also adding `--init`.

## Gotchas
- With a shell-form `ENTRYPOINT`, a shell sits between the init and your app and may not forward signals; use exec form or `exec` in the script.
- `--init` is a Docker run option (`init: true` in Compose); it is not a Kubernetes setting, so bake tini into the image there.

## Verify
```sh
docker exec app ps -o pid,ppid,stat,comm     # PID 1 is docker-init/tini, no Z states
time docker stop app                         # should return quickly instead of waiting out the timeout
```

## Checked

Checked against the `docker container run` reference ("Specify an init process"), the dockerd reference (`init`, `init-path`), the Compose Specification (`init`), the docker/docs attach reference (PID 1 signal note) and the krallin/tini README (docker/docs latest commit 2026-10-23, Engine 29).

- `--init` and Compose `init: true`, default `docker-init` backed by tini, daemon `init` and `init-path`, PID 1 signal behaviour, tini `-g`, `-s` and `TINI_SUBREAPER` (Linux 3.4+), Debian `/usr/bin/tini` and Alpine `/sbin/tini` install paths.
- Removed as unconfirmed: the `/sbin/docker-init` path, the 10-second timing and `pids-limit` error text, the s6-overlay and Kubernetes `shareProcessNamespace` remarks.

Method: documentation only; no commands were run.
