---
id: computing-software.software-engineering.deno.docker-images-and-multistage
name: docker-images-and-multistage
category: computing-software
field: software-engineering
product: deno
tags: [docker, dockerfile, multi-stage, deno-ci, deno-dir, non-root, healthcheck]
level: practitioner
status: docs-checked
description: "Containerize a Deno app with the official denoland/deno image: cached deno ci layer, multi-stage builds copying DENO_DIR, tags, non-root user and health check."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```dockerfile
FROM denoland/deno:latest
WORKDIR /app
COPY deno.json deno.lock package.json* ./
RUN deno ci --prod --skip-types
COPY . .
CMD ["deno", "run", "--allow-net", "main.ts"]
```

Copy manifests first so the install layer caches across source-only edits. `deno ci` installs reproducibly from `deno.lock`; `--prod` skips devDependencies, `--skip-types` drops `@types/*`.

Multi-stage: point `DENO_DIR` at a known path in the builder and copy it to the final stage, otherwise the container re-downloads dependencies on first run.

```dockerfile
FROM denoland/deno:latest AS builder
ENV DENO_DIR=/deno-dir
# ...manifests, deno ci, COPY . .
FROM denoland/deno:latest
ENV DENO_DIR=/deno-dir
COPY --from=builder /app .
COPY --from=builder /deno-dir /deno-dir
```

Tags: `latest`, `alpine`, `distroless`, `ubuntu`, `2.x`. Useful env: `DENO_NO_UPDATE_CHECK=1`, `DENO_NO_PROMPT=1`. Pass narrow permissions in `CMD`, e.g. `--allow-net=api.example.com --allow-read=/data`. Add a `.dockerignore`.

Non-root:

```dockerfile
RUN addgroup --system deno && adduser --system --ingroup deno deno
USER deno
```

Health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD deno eval "try { await fetch('http://localhost:8000/health'); } catch { Deno.exit(1); }"
```

## Checked

2026-11-04. Confirmed against docs runtime/reference/docker.md (Deno and Docker): Dockerfile with deno ci --prod --skip-types, manifest-first layer caching, multi-stage DENO_DIR copy and its reason, tags, env vars, scoped permissions in CMD, non-root user commands, HEALTHCHECK.

Method: documentation only; no commands were run.
