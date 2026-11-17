---
id: computing-software.cloud-infrastructure-engineering.docker.docker-exec-and-logs-options
name: docker-exec-and-logs-options
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-exec, docker-logs, exec-user, exec-workdir, exec-env, logs-since, logs-tail, logs-timestamps, container-debugging]
level: practitioner
description: "Get precise output from docker exec (--user, --workdir, --env, -i without -t) and docker logs (--since, --until, --tail, --timestamps, -f) during incidents."
sources: ["https://docs.docker.com/reference/cli/docker/container/exec/", "https://docs.docker.com/reference/cli/docker/container/logs/", "https://docs.docker.com/engine/logging/dual-logging/", "https://docs.docker.com/engine/logging/configure/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker exec and docker logs options

## exec
```sh
docker exec -it app sh                                     # interactive
docker exec -u 0 app apt-get install -y procps             # as root in a non-root image
docker exec -u 1000:1000 app touch /data/x                 # as a specific uid:gid
docker exec -w /srv/app app ls                             # working directory
docker exec -e LOG_LEVEL=debug app ./cli diag              # extra env for this process only
docker exec --env-file diag.env app ./cli diag
docker exec -i db psql -U postgres < query.sql             # stdin, no tty
docker exec -d app ./warm-cache.sh                         # background
docker exec --privileged app ...                           # extended privileges for this process
```
- exec runs a new command in a running container; it only runs while the container's primary process (PID 1) is running and is not restarted if the container restarts.
  The command must be an executable: wrap chained commands as `sh -c "a && b"`.
- Only works on **running** containers. For a crash-looping one: `docker run --rm -it
  --entrypoint sh <image>` with the same mounts.
- If the image has no shell, `exec` of `sh` cannot work; use an image or sidecar that has one.

## logs
```sh
docker logs --tail 200 app
docker logs -f --since 10m app
docker logs --since 2026-10-16T09:00:00 --until 2026-10-16T09:15:00 app
docker logs -t app                              # timestamps prepended
docker logs --details app                       # extra details provided to logs
```
- `--since/--until` accept RFC3339 timestamps, Unix timestamps, or relative durations (`42m`, `1h30m`).
- `--tail all` is the default - on a chatty container, always pass `--tail`.
- Reading logs depends on the logging driver. With a remote driver, dual logging (a local cache) lets `docker logs` still work; with `"log-opts": {"cache-disabled": "true"}` it fails with `configured logging driver does not support reading`.
- `docker logs --follow` streams the container's STDOUT and STDERR.

## Verify
`docker exec -u 0 -w / app id && pwd` shows root and `/`; `docker logs --since 5m -t app` shows
timestamps within the window.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the dual-logging page. Confirmed: exec options `-d`, `-e`, `--env-file`, `-i`, `-t`, `--privileged`, `-u`, `-w`; exec runs only while PID 1 runs and needs an executable (use `sh -c` for chains); logs options `--details`, `-f`, `--since`, `-n/--tail` (default all), `-t`, `--until`; since/until accept timestamps or relative durations; dual logging and the `cache-disabled` error text. Removed: signal and namespace claims, executable-not-found text, CRLF claim, `docker debug`, RFC3339Nano and stdout-only comments, Engine 20.10 gate, Compose logs line, grep and head pipelines.
Method: documentation only; no commands were run.
