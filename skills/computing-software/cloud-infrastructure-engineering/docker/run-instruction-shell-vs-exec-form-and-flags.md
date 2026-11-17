---
id: computing-software.cloud-infrastructure-engineering.docker.run-instruction-shell-vs-exec-form-and-flags
name: run-instruction-shell-vs-exec-form-and-flags
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, run-instruction, run-exec-form, shell-form, exec-form, run-mount, run-network, run-security, buildkit]
level: practitioner
description: "Choose RUN shell form vs exec form correctly, and use RUN's BuildKit flags (--mount, --network, --security) without breaking caching or portability."
sources: ["https://docs.docker.com/reference/dockerfile/#run", "https://docs.docker.com/reference/dockerfile/#shell-and-exec-form", "https://docs.docker.com/reference/dockerfile/#run---mount", "https://docs.docker.com/build/building/best-practices/", "https://docs.docker.com/reference/build-checks/json-args-recommended/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RUN: shell form vs exec form, and the RUN flags

**Goal:** write `RUN` lines that do what you think they do — shell features only when you
want them, exec form when you need exact argv, and the BuildKit flags for mounts, network
and sandbox control.

## The two forms
```dockerfile
RUN apt-get update && apt-get install -y curl     # shell form: /bin/sh -c "..."
RUN ["/bin/bash", "-c", "echo $HOME"]             # exec form: JSON array, no shell
```
- Shell form always uses a command shell: `/bin/sh -c` by default on Linux (or the shell set by
  a `SHELL` instruction), `cmd /S /C` on Windows. You get `&&`, pipes, redirects and variable
  expansion.
- Exec form is parsed as a JSON array, so use **double quotes**. It does not invoke a command
  shell, so there is no shell variable substitution (`["echo", "$HOME"]` prints `$HOME`); run
  a shell explicitly if you need one.
- Backslashes in exec form must be escaped, which matters for Windows paths (`C:\\path`).
- Pipes in shell form: the exit status is that of the **last** command, so
  `RUN wget -O - https://some.site | wc -l` succeeds even if wget fails. Prepend
  `set -o pipefail &&` (not every shell supports it; on Debian-based images use exec form with
  `/bin/bash -c` to choose a shell that does).

## Line continuation and heredocs
Long shell-form commands use `\` continuation. For multi-line scripts prefer a heredoc
(BuildKit, `# syntax=docker/dockerfile:1`):
```dockerfile
RUN <<EOF
set -eux
apt-get update
apt-get install -y --no-install-recommends curl ca-certificates
rm -rf /var/lib/apt/lists/*
EOF
```
Add `set -e` (or `set -ex`) inside a heredoc script so a failing line stops the script.

## RUN flags (BuildKit only)
| Flag | What it does |
|---|---|
| `--mount=type=cache,target=/root/.cache/pip` | persistent cache dir across builds, not in the image |
| `--mount=type=bind,source=.,target=/src` | bind-mounts context, stage or named-context files (read-only by default), no COPY layer |
| `--mount=type=secret,id=npmrc,target=/root/.npmrc` | secret file for this step only |
| `--mount=type=ssh` | forward the agent socket |
| `--mount=type=tmpfs,target=/tmp` | scratch space that never lands in a layer |
| `--network=none` | run the command with no network access |
| `--network=host` | host network; protected by the `network.host` entitlement (builder started with `--allow-insecure-entitlement network.host`, build run with `--allow network.host`) |
| `--security=insecure` | run without the sandbox for flows needing elevated privileges; protected by the `security.insecure` entitlement (`--allow security.insecure`) |

`--network` defaults to `default`, `--security` to `sandbox`. Flags go **before** the command:
`RUN --mount=type=cache,target=/var/cache/apt apt-get ...`. `--mount` needs Dockerfile syntax
1.2 or later, `--network` 1.3, `--security` 1.20.

## Gotchas
- Each `RUN` creates a layer on top of the previous one; clean up (for example
  `rm -rf /var/lib/apt/lists/*`) in the same `RUN` that created the files.
- Exec form does not use a shell, so to use shell features wrap the command with
  `["sh", "-c", "..."]`.
- Set `DEBIAN_FRONTEND=noninteractive` on the RUN line (`RUN DEBIAN_FRONTEND=noninteractive
  apt-get ...`) or via `ARG`, not `ENV`: `ENV` persists into containers and changes `apt-get`
  behaviour for users of the image.

## Verify
`docker build --check .` (Dockerfile 1.8+) runs the build checks. Note `JSONArgsRecommended`
applies to `CMD` and `ENTRYPOINT`, not `RUN`.

## Checked

Checked 2026-10-23 against the Dockerfile reference (RUN, `RUN --mount`, `--network`, `--security`, shell and exec form; moby/buildkit docs main), docker/docs build best practices and the JSONArgsRecommended rule page.
Confirmed: shell versus exec form semantics and backslash escaping, `set -o pipefail` guidance, heredoc form, bind mounts read-only by default, `--network` values and the `network.host` entitlement, `--security` values and defaults, minimum syntax versions for the flags. Removed the hadolint rule id, the legacy-builder claim, the `~`/PATH exec-form claim and the `docker history` claim.

Method: documentation only; no commands were run.
