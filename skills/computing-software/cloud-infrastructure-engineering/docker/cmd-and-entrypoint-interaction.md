---
id: computing-software.cloud-infrastructure-engineering.docker.cmd-and-entrypoint-interaction
name: cmd-and-entrypoint-interaction
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, cmd-vs-entrypoint, entrypoint-cmd-interaction, entrypoint-override, entrypoint, cmd, exec-form, docker-run]
level: practitioner
description: "The CMD/ENTRYPOINT interaction table, how docker run and Compose override each, and the exec-form rules that decide whether your process gets signals."
sources: ["https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact", "https://docs.docker.com/reference/cli/docker/container/run/#entrypoint", "https://docs.docker.com/reference/compose-file/services/#entrypoint", "https://docs.docker.com/reference/compose-file/services/#command"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CMD and ENTRYPOINT: how they combine and how to override them

**Goal:** predict exactly what argv a container starts with, given the Dockerfile and the
`docker run` / Compose overrides, and get the form right so PID 1 is your process.

## The interaction table (memorise this)
| ENTRYPOINT | CMD | Resulting argv |
|---|---|---|
| none | `["a","b"]` | `a b` |
| none | `a b` (shell form) | `/bin/sh -c "a b"` |
| `["e"]` | none | `e` |
| `["e"]` | `["x","y"]` | `e x y` |
| `["e"]` | `x y` (shell) | `e /bin/sh -c "x y"` (almost never what you want) |
| `e` (shell form) | anything | `/bin/sh -c e` — **CMD is ignored entirely** |

Rules that fall out of it:
- Exec-form ENTRYPOINT + exec-form CMD is the only combination where CMD acts as *default
  arguments*. Mixing forms silently produces `sh -c` wrappers.
- Shell-form ENTRYPOINT makes `/bin/sh` PID 1; your process is a child and does not receive
  `SIGTERM` from `docker stop`, so the daemon waits out the stop timeout (10 seconds by default
  for Linux containers) and then kills it. Use exec form, or `exec` inside a wrapper script.
- If the base image sets an ENTRYPOINT and you set only CMD, the base's ENTRYPOINT still applies.
- If CMD comes from the base image, setting ENTRYPOINT in the child resets CMD to empty, so
  redeclare CMD in the child image.

## Overriding at run time
```sh
docker run img                      # ENTRYPOINT + CMD from image
docker run img arg1 arg2            # replaces CMD only -> ENTRYPOINT arg1 arg2
docker run --entrypoint sh img      # replaces ENTRYPOINT; any image CMD is cleared, so add args after img
docker run --entrypoint sh img -c 'ls /'
docker run --entrypoint "" img ls   # empty string resets ENTRYPOINT; image CMD also cleared
```
Compose:
```yaml
services:
  app:
    entrypoint: ["python"]     # replaces ENTRYPOINT; a non-null entrypoint also ignores the image CMD
    command: ["-m", "app"]     # replaces CMD
```
In Compose, `entrypoint: []` or `entrypoint: ''` overrides the image entrypoint to empty, and
`null` keeps the image's. The same holds for `command`.
Unlike a Dockerfile `CMD`, Compose `command` does not run inside the image's `SHELL`; for variable
expansion run a shell explicitly, for example `command: /bin/sh -c 'echo "hello $$HOSTNAME"'`.

## Pattern: wrapper script
```dockerfile
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]
CMD ["server", "--port", "8080"]
```
```sh
#!/bin/sh
set -e
# setup...
exec "$@"      # hand PID 1 to the CMD
```
Without `exec "$@"` the script stays PID 1 and your server misses signals.

## Gotchas
- JSON array needs double quotes. `CMD ['a']` is parsed as shell form containing literal
  brackets.
- `CMD` in exec form cannot expand variables: `CMD ["echo", "$X"]` prints `$X`. Use
  `CMD ["sh", "-c", "echo $X"]` if you need expansion.
- `docker inspect --format '{{.Config.Entrypoint}} {{.Config.Cmd}}' img` shows the stored
  values.

## Verify
`docker top <container>` on a running container: the listed command should be your binary, not
`/bin/sh -c ...`. `docker stop` should return well inside the stop timeout.

## Checked

Checked 2026-10-23 against the Dockerfile reference (moby/buildkit `frontend/dockerfile/docs/reference.md`, main), the `docker run` reference in docker/cli and the Compose services reference in docker/docs.
Confirmed: the ENTRYPOINT/CMD interaction table; setting ENTRYPOINT resets a base-image CMD; `--entrypoint` clears the image CMD and an empty string resets the entrypoint; the Linux default stop timeout of 10 seconds; Compose `entrypoint`/`command` null, empty-list and empty-string semantics and the no-shell note for `command`.

Method: documentation only; no commands were run.
