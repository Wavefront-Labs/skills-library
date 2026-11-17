---
id: computing-software.cloud-infrastructure-engineering.docker.shell-form-cmd-signals-and-exec-wrappers
name: shell-form-cmd-signals-and-exec-wrappers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pid1, signal-handling, shell-form-signals, exec-in-entrypoint, graceful-shutdown, json-args-recommended]
level: practitioner
status: docs-checked
description: "Why shell-form CMD/ENTRYPOINT and wrapper scripts ignore docker stop (10s then SIGKILL), and how to fix it with exec form, exec in scripts, and the JSONArgsRecommended check."
sources: ["https://docs.docker.com/reference/dockerfile/#entrypoint", "https://docs.docker.com/reference/dockerfile/#shell-and-exec-form", "https://docs.docker.com/reference/build-checks/json-args-recommended/", "https://docs.docker.com/reference/cli/docker/container/run/#init"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shell form, signals and exec wrappers

Symptom: `docker stop` always takes the full stop timeout (10 seconds by default for Linux
containers) and the app never logs a graceful shutdown.

## Cause
```dockerfile
CMD node server.js              # shell form
```
Shell form runs as a subcommand of `/bin/sh -c`, which does not pass signals. The executable is
not the container's PID 1 and does not receive the `SIGTERM` that `docker stop` sends; after the
timeout the daemon kills the container. The build check `JSONArgsRecommended` warns about this for
`CMD` and `ENTRYPOINT`.

## Fixes
**Exec form** (no shell, the executable is PID 1):
```dockerfile
CMD ["node", "server.js"]
ENTRYPOINT ["/usr/local/bin/app", "--config", "/etc/app.yaml"]
```
**Need shell features?** Use `exec` so the shell replaces itself with the program:
```dockerfile
CMD ["sh", "-c", "exec node server.js --port=${PORT:-3000}"]
```
**Wrapper script**: end it with `exec` so the final executable receives the signals:
```sh
#!/bin/sh
set -e
# setup work here
exec /app/server "$@"
```
Without `exec` the script stays PID 1 and the server does not receive signals directly.
**Several processes or work on shutdown**: the reference shows an `ENTRYPOINT` script that
traps signals, forwards them and then does more work, or you can run with an init process:
`docker run --init` (Compose `init: true`) runs an init inside the container that forwards
signals and reaps processes.

## Check what is PID 1
```bash
docker top <c>                         # shows the process list; the app should be the main process
docker inspect -f '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' <image>
time docker stop <c>                   # should return well inside the stop timeout
```

## Gotchas
- Wrappers such as `npm start` are shells or launchers too; run the runtime directly in exec form.
- `STOPSIGNAL` sets the signal `docker stop` sends (default `SIGTERM`); set it in the Dockerfile
  if the app expects another one. It does not change what Ctrl+C sends.
- A shell-form `ENTRYPOINT` ignores `CMD` and `docker run` arguments (see the CMD/ENTRYPOINT table
  in the Dockerfile reference).

## Checked

Checked 2026-10-23 against the Dockerfile reference (ENTRYPOINT, shell and exec form, STOPSIGNAL; moby/buildkit docs main), docker/cli `docker run` and `docker stop` references, the JSONArgsRecommended rule page and docker/docs build best practices.
Confirmed: shell form runs under `/bin/sh -c` and does not pass signals so `SIGTERM` from `docker stop` is not received; the exec-based entrypoint pattern; `--init` forwards signals and reaps processes; the 10 second Linux default stop timeout; shell-form ENTRYPOINT ignores CMD. Removed the exit-code (137/143) claims, the claim about `sh` lacking a default PID 1 handler, tini and the build-tool wrapper examples.

Method: documentation only; no commands were run.
