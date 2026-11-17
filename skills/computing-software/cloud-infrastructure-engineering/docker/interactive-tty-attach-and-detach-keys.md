---
id: computing-software.cloud-infrastructure-engineering.docker.interactive-tty-attach-and-detach-keys
name: interactive-tty-attach-and-detach-keys
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-run, interactive-tty, docker-attach, detach-keys, detach, stdin, tty]
level: practitioner
description: "Use -i and -t correctly in terminals, scripts and pipes, attach to running containers without killing them, and change the Ctrl-P Ctrl-Q detach keys."
sources: ["https://docs.docker.com/reference/cli/docker/container/attach/", "https://docs.docker.com/reference/cli/docker/container/run/#detach-keys", "https://docs.docker.com/reference/cli/docker/#configuration-files", "https://github.com/compose-spec/compose-spec/blob/main/spec.md#tty"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# -it, attach and detach keys

## -i and -t are different things
| Flags | Effect | Use |
|---|---|---|
| `-i` | keep STDIN open | piping data in: `cat dump.sql \| docker exec -i db psql` |
| `-t` | allocate a pseudo-TTY | interactive shells, colour, line editing |
| `-it` | both | interactive shell |
| neither | no stdin, no tty | scripts, logs to stdout |

- In CI or cron there is no terminal on stdin, so do not pass `-t` there (use `-i` only, or neither), and do not use `-t` when capturing binary output.
- Signals: `--sig-proxy` (default true on `attach`) proxies received signals to the process, so Ctrl-C sends SIGINT to the container process. A process running as PID 1 ignores signals with the default action, so it must install a handler to exit on SIGINT or SIGTERM.

## attach
```sh
docker attach app                 # connect to PID 1's stdio
docker attach --no-stdin app      # watch only; Ctrl-C won't reach the app
docker logs -f app                # usually what you actually want
```
Danger: with `--sig-proxy` on, Ctrl-C is forwarded to the container and can terminate it (Docker's attach example shows this for a container started without `-it`). Use the detach sequence instead.

## Detach keys
Default `Ctrl-P Ctrl-Q` detaches from `run -it` or `attach` and leaves the container running
(it works when the container was started with both `-i` and `-t`; without them the keys are forwarded and have no effect). Docker's docs also note you cannot redirect stdin of `docker attach` for a TTY-enabled container.
Override when it collides (bash/emacs use Ctrl-P):
```sh
docker run -it --detach-keys="ctrl-x,x" alpine sh
docker attach --detach-keys="ctrl-x,x" app
```
Persist in `~/.docker/config.json`:
```json
{ "detachKeys": "ctrl-x,x" }
```
Format: a sequence of keys, each a letter or `ctrl-` plus one of `a-z`, `@`, `[`, `\`, `_` or `^`, for example `a`, `ctrl-a`, `X` or `ctrl-\`. The config-file key is `detachKeys`.

## Compose
`stdin_open: true` (= `-i`) and `tty: true` (= `-t`) in the Compose Specification; `docker compose attach svc`;
`docker compose run` allocates a TTY automatically when it can and `-T` disables it (use it in CI).

## Verify
`docker run -i --rm alpine cat < file | sha256sum` equals the file's hash; detach with your
keys and `docker ps` still shows the container running.

## Checked

Checked against the `docker container attach` and `docker container run` references (`data/cli/engine`), the `docker` command reference (`detachKeys`), the Compose Specification (`stdin_open`, `tty`) and the `docker compose run` reference (docker/docs latest commit 2026-10-23, Engine 29).

- Default detach keys `CTRL-p CTRL-q` only when `-i` and `-t` are set, `--detach-keys` format, `detachKeys` config property, `--sig-proxy` default true and `--no-stdin`, the PID 1 default-signal note, `docker compose run -T`.
- Removed as unconfirmed: the "not a TTY" error text, the stdout/stderr merging and newline translation claims, the `pg_dump` example and the shell snippet that detects a TTY.

Method: documentation only; no commands were run.
