---
id: computing-software.cloud-infrastructure-engineering.docker.pid1-signal-handling-and-init
name: pid1-signal-handling-and-init
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pid-1, pid1, signal-handling, tini, init, graceful-shutdown, zombie-processes, sigterm, exec-form, docker-stop, stop-timeout, dumb-init, entrypoint-script]
level: practitioner
status: docs-checked
description: "Making a container stop cleanly: why PID 1 ignores SIGTERM, exec-form vs shell-form, --init/tini for zombie reaping, exec in entrypoint scripts, STOPSIGNAL and stop-timeout tuning."
sources: ["https://docs.docker.com/reference/cli/docker/container/stop/", "https://docs.docker.com/reference/cli/docker/container/run/#init", "https://docs.docker.com/reference/dockerfile/#stopsignal", "https://docs.docker.com/reference/compose-file/services/", "https://github.com/krallin/tini", "https://github.com/nginx/docker-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PID 1, signal handling and init

**Goal:** `docker stop` ends the container within the grace period with in-flight work
finished, and a long-running container does not accumulate zombie processes.

## Why containers hang on stop
Docker's reference: the main process in the container receives `SIGTERM` and, after a grace
period, `SIGKILL`; the first signal can be changed with the `STOPSIGNAL` instruction or the
`--stop-signal` option of `docker run` and `docker create`. The grace period is set with
`docker stop --timeout` / `-t` (the older `--time` flag is deprecated), or `--stop-timeout` on
`docker run`. Compose documents a 10 second default for `stop_grace_period`.
Typical causes of a hang until the kill:
1. **The process does not handle the signal.** Tini's README says an init process ensures the
   default signal handlers work for the software you run, which implies a PID 1 without its own
   handler may not get them.
2. **Shell form wraps your process in a shell.** `CMD node server.js` makes `/bin/sh -c` PID 1
   and `node` a child; the shell may not forward the signal.

Diagnose: `docker exec <c> ps -o pid,ppid,comm` shows which process is PID 1.

## Fix 1: exec form
```dockerfile
CMD ["node", "server.js"]                 # exec form: node is PID 1
ENTRYPOINT ["/app/entrypoint.sh"]
```
`CMD ["sh", "-c", "node server.js"]` is exec form syntactically but still runs a shell as
PID 1. If you need a shell script, end it with `exec`.

## Fix 2: `exec` in entrypoint scripts
```sh
#!/bin/sh
set -e
./migrate.sh                 # setup work runs as a child
exec node server.js          # replaces the shell: node becomes PID 1 and receives signals
```

## Fix 3: an init process (`--init` / tini)
A PID 1 that spawns children should reap them, or exited children stay as zombies.
```bash
docker run --init myimage        # run an init inside the container that forwards signals and reaps processes
```
Compose: `init: true` on the service (the init binary is platform specific). In a Dockerfile,
tini's README shows:
```dockerfile
RUN apk add --no-cache tini
# Tini is now available at /sbin/tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```
Tini reaps zombies and forwards signals; `tini -g` makes it signal the child's whole process
group.

## Tuning the grace period
```dockerfile
STOPSIGNAL SIGINT                     # per-image default
```
```bash
docker run --stop-signal SIGINT --stop-timeout 30 myimage
docker stop -t 30 <c>
```
Compose: `stop_signal: SIGINT`, `stop_grace_period: 30s`. The official nginx image sets
`STOPSIGNAL SIGQUIT`. Keep the runtime's grace period shorter than your orchestrator's, or the
orchestrator may kill first (see your orchestrator's termination settings).

## Verify
```bash
docker run -d --name t myimage
time docker stop t
docker inspect -f '{{.State.ExitCode}}' t
```

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed: docker stop description (SIGTERM then SIGKILL, STOPSIGNAL and --stop-signal), docker stop --timeout/-t with --time deprecated, docker run --init, --stop-timeout and --stop-signal, Compose init, stop_signal and stop_grace_period (10 second default), tini README (apk install at /sbin/tini, -g, zombie reaping), docker-nginx Dockerfile STOPSIGNAL SIGQUIT. Removed unconfirmed per-language handler recipes (Node, npm, Python, Java, Go), the exit-code interpretation, the Kubernetes default grace period, the ps/grep zombie count and the claim that docker stop default is 10 s for the CLI.

Method: documentation only; no commands were run.
