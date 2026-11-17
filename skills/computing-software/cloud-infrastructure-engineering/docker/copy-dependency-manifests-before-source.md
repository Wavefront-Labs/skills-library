---
id: computing-software.cloud-infrastructure-engineering.docker.copy-dependency-manifests-before-source
name: copy-dependency-manifests-before-source
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, layer-caching, build-cache, dependency-manifest-first, package-manifest-ordering, layer-ordering, npm-ci, go-mod-download, pip-install, cache-invalidation]
level: practitioner
description: "Order COPY so lockfiles and dependency manifests are copied and installed before application source, so the expensive install layer is cached across code changes."
sources: ["https://docs.docker.com/build/cache/optimize/", "https://docs.docker.com/build/cache/invalidation/", "https://docs.docker.com/reference/dockerfile/#impact-on-build-caching"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Copy dependency manifests before source

**Goal:** make the dependency-install layer survive source edits, so a one-line code change
rebuilds quickly instead of re-downloading every package.

## The rule
A change in an instruction (or in files an `ADD`/`COPY` copies) rebuilds the steps that follow,
so expensive steps belong near the top and frequently changing ones near the end.
`COPY . .` followed by the install reruns the install on any file change. Split it: copy the
package-management files, install dependencies, then copy the project source.

Docker's own example (Node):
```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock ./   # package management files
RUN npm install                  # install dependencies
COPY . .                         # project files
RUN npm run build
```
The same shape for other stacks:
```dockerfile
# Python (pip)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Go
COPY go.mod go.sum ./
RUN go mod download
COPY . .
```

## Details that decide whether it works
- Copy the **lockfile** with the manifest, so the layer changes when resolved versions change.
- The `ADD`/`COPY` cache checksum comes from file metadata and ignores `mtime`, so touching a file
  without changing it does not invalidate the cache.
- Add a package-manager cache mount so that when the manifest does change, packages come from
  the local cache: for example `RUN --mount=type=cache,target=/root/.npm npm install`,
  `--mount=type=cache,target=/root/.cache/pip`, or for Go
  `--mount=type=cache,target=/go/pkg/mod` with `target=/root/.cache/go-build`.
- Keep `node_modules`, virtual environments and build output in `.dockerignore` so the final
  `COPY . .` does not copy host artefacts over the installed ones.

## Gotchas
- An `ARG` or `ENV` placed before the install step whose value changes per build (for example a
  Git SHA used for labels) invalidates everything below it; declare such ARGs just before the step
  that needs them. A changed `ARG` causes a miss at its first use, and every `RUN` after it uses it
  implicitly.

## Verify
Change one source file and rebuild with `--progress=plain`: the install step should show
`CACHED` while the final copy and build steps re-run.

## Checked

Checked 2026-10-23 against docker/docs "Optimize cache usage in builds" (order your layers, cache mounts), "Build cache invalidation" and the Dockerfile reference (ARG cache impact).
Confirmed: the split-COPY pattern for Node, the mtime-exempt metadata checksum, cache mount targets for npm, pip and Go, `.dockerignore` for the context, ARG miss behaviour. Removed unconfirmed language-tool recipes (uv, Rust stub build, Maven offline) and the workspace and monorepo glob advice.

Method: documentation only; no commands were run.
