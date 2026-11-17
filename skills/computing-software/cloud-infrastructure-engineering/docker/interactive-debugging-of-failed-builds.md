---
id: computing-software.cloud-infrastructure-engineering.docker.interactive-debugging-of-failed-builds
name: interactive-debugging-of-failed-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, buildx-debug, build-debugging, progress-plain, build-target, dockerfile]
level: advanced
status: docs-checked
description: "Get a shell at the failing step of a Docker build: buildx debug with --on=error, the monitor commands, plus the portable fallback of --target and plain progress logs."
sources: ["https://github.com/docker/buildx/blob/master/docs/debugging.md", "https://docs.docker.com/reference/cli/docker/buildx/debug/", "https://docs.docker.com/reference/cli/docker/buildx/build/#progress", "https://docs.docker.com/reference/cli/docker/buildx/history/inspect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactive debugging of failed builds

## 1. Read the full log first
```bash
docker build --progress=plain --no-cache-filter <stage> . 2>&1 | tee build.log
```
`--progress=plain` shows the full output of every step instead of the collapsed TTY view;
`BUILDKIT_PROGRESS` sets it through the environment. `--no-cache-filter` ignores the cache for
the named stage(s).

## 2. buildx debug: a shell in the build result
The debug monitor is an experimental feature: set `BUILDX_EXPERIMENTAL=1` first.
```bash
export BUILDX_EXPERIMENTAL=1
docker buildx debug --on=error build .            # open the debugger when the build fails
docker buildx debug --invoke /bin/sh build .      # launch /bin/sh in the resulting image
```
- `--on` defaults to `error` (values `always` or `error`); `--invoke` takes a command, or
  CSV-style keys `args`, `entrypoint`, `env`, `user`, `cwd`, `tty`.
- `buildx debug build` takes the same arguments as `buildx build`.
- By default you land in a shell in the final stage. With `--on=error` the shell shows the image
  state at the point the build failed.
- Press `Ctrl-a-c` to toggle between the debug shell and monitor mode. Monitor commands include
  `attach`, `disconnect`, `exec`, `exit`, `help`, `kill`, `list`, `ps`, `reload` (reloads the
  context and builds it) and `rollback` (re-runs the interactive container with the step's
  rootfs contents).

## 3. Portable fallback: build up to the stage and run it
```bash
docker build --target build -t dbg .              # stage before the failure
docker run --rm -it --entrypoint sh dbg
```
Comment out the failing `RUN` so the stage builds, then replay it interactively.

## Common root causes found this way
- Command works locally but not in the build: different `WORKDIR`, `SHELL` or `PATH`.
- Network: `RUN --network=none` or missing proxy settings.
- Files missing: `.dockerignore` excluded them; `ls` in the shell confirms.

## Verify the fix
```bash
docker buildx build --progress=plain . 2>&1 | tail -20
docker buildx history inspect            # details of the last build
```

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation, docker/buildx docs. Confirmed in the buildx debug reference and the buildx debugging guide (docker/buildx docs/debugging.md, buildx v0.38.1 current): experimental status and BUILDX_EXPERIMENTAL=1, --invoke and --on options and defaults, Ctrl-a-c toggle, monitor command list, --no-cache-filter, --progress and BUILDKIT_PROGRESS, RUN --network, buildx history inspect. Removed unconfirmed claims about mounts/env of the failed step, unsaved changes, distroless limits, dash, QEMU segfaults and DNS causes.

Method: documentation only; no commands were run.
