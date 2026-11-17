---
id: computing-software.cloud-infrastructure-engineering.docker.diagnosing-slow-or-oversized-build-context
name: diagnosing-slow-or-oversized-build-context
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, build-context, context-size, context-transfer, transferring-context, slow-build, dockerignore, build-performance, remote-builder]
level: practitioner
description: "Find out why 'transferring context' is slow or huge, measure what is actually sent, and fix it with .dockerignore, narrower contexts, bind mounts or a local builder."
sources: ["https://docs.docker.com/build/concepts/context/#dockerignore-files", "https://docs.docker.com/build/cache/optimize/#keep-the-context-small", "https://docs.docker.com/reference/compose-file/build/#additional_contexts"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnosing slow or oversized build contexts

**Goal:** turn a build that spends minutes on `transferring context` with a multi-gigabyte
context into one that sends only what the Dockerfile needs.

## Measure first
`docker build --progress=plain .` prints `[internal] load build context` and a
`transferring context: <size>` line. Compare it to the size of the source you expect. The
`.dockerignore` removes matched files from the context before it is sent to the builder, which
matters most for a remote builder.

To see **which files** are included, build a throwaway listing image:
```sh
docker build --progress=plain -f- . <<'EOF'
FROM busybox
COPY . /ctx
RUN find /ctx -type f
EOF
```

## Usual culprits
- `.git`, dependency directories (`node_modules`, `.venv`, `target`, `vendor`), build output such
  as `dist`.
- Data directories used by local containers that live inside the context.
- Logs, coverage output and caches.
- A `.dockerignore` in the wrong place: it must be at the **root of the context** (or be a
  `<Dockerfile>.dockerignore` next to the Dockerfile).
- A context that is wider than needed: `docker build -f app/Dockerfile .` with `.` as the
  repository root when `app/` would do.

## Fixes
1. Add a `.dockerignore`; an allowlist (`*` then `!src`, `!package.json`, ...) keeps new files
   out by default.
2. Narrow the context: `docker build app/` or Compose `build.context: ./app`, with
   `additional_contexts` (named contexts) for shared files.
3. Use a bind mount for build-only inputs instead of `COPY`:
   `RUN --mount=type=bind,target=. go build -o /app/hello` mounts the directory for that step.
4. A Dockerfile-specific ignore file (`<Dockerfile>.dockerignore`) lets each Dockerfile in a
   repository exclude different things.

## Gotchas
- The `.dockerignore` can exclude `Dockerfile` and `.dockerignore`; they are still sent but cannot
  be copied into the image.
- Version information normally taken from `.git` can be passed with `--build-arg`, or a Git
  context can keep `.git` via `BUILDKIT_CONTEXT_KEEP_GIT_DIR`.

## Verify
The `transferring context` size drops to the expected source-only size, and the listing build
shows only the files the Dockerfile needs.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (.dockerignore), "Optimize cache usage in builds" (keep the context small, bind mounts), the Compose build `additional_contexts` reference and the Dockerfile reference.
Confirmed: `.dockerignore` location and effect, per-Dockerfile ignore files, bind-mount `RUN --mount`, `additional_contexts`, `BUILDKIT_CONTEXT_KEEP_GIT_DIR`. Removed unconfirmed claims: driver-specific transfer costs, incremental transfer snapshots, symlink handling, Desktop file-sharing overhead, the `/tmp` listing script and numeric size targets.

Method: documentation only; no commands were run.
