---
id: computing-software.cloud-infrastructure-engineering.docker.copy-parents-and-exclude
name: copy-parents-and-exclude
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, copy, copy-parents, copy-exclude, monorepo, layer-caching]
level: practitioner
status: docs-checked
description: "Copy monorepo files keeping their directory structure with COPY --parents (and the /./ pivot), and filter sources with COPY/ADD --exclude, plus frontend version needs."
sources: ["https://docs.docker.com/reference/dockerfile/#copy---parents", "https://docs.docker.com/reference/dockerfile/#copy---exclude", "https://docs.docker.com/build/buildkit/frontend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COPY --parents and --exclude

Two flags that remove the most common reason for many `COPY` lines in monorepos.

## Frontend requirement
Both flags are documented in the Dockerfile reference. Declare the frontend so the builder uses
the latest stable Dockerfile syntax:
```dockerfile
# syntax=docker/dockerfile:1
```

## --parents: keep the source path
Plain `COPY` flattens: `COPY ./a/package.json ./b/package.json /app/` writes both to
`/app/package.json`, and BuildKit silently overwrites the colliding file. With `--parents` the
parent directories of each source are preserved (like `cp --parents` or `rsync --relative`):
```dockerfile
WORKDIR /app
# copies to /app/packages/api/package.json, /app/packages/web/package.json, ...
COPY --parents packages/*/package.json package.json package-lock.json ./
RUN npm ci
COPY . .
```
This is a way to do "manifests first" caching for repositories with several packages. The `**`
wildcard matches any number of path components, including none.

Inserting `./` into the source path limits which parent directories are kept: only those after
it are preserved.
```dockerfile
COPY --parents ./services/./api/**/*.go /src/      # lands in /src/api/..., not /src/services/api/...
```
With `--parents`, BuildKit can also pack multiple `COPY` instructions together while keeping the
directory structure, which keeps the layer count low.

## --exclude: filter a copy
```dockerfile
COPY --exclude=*.txt --exclude=*.md hom* /mydir/
```
- The path expression follows the same format as `<src>`: wildcards, matched with Go
  `filepath.Match` rules. Repeat the flag for several patterns; a file matching any of them is
  not copied, even if it matches `<src>`.
- `ADD` accepts `--exclude` with the same meaning.

## Verify
```bash
docker build --target deps -t t . && docker run --rm t find /app -name package.json
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (`COPY --parents`, `COPY --exclude`, `ADD --exclude`; moby/buildkit `frontend/dockerfile/docs/reference.md`, main branch) and the Docker docs Dockerfile frontend page.

- `--parents` semantics, the `./` pivot, `**`, collision behaviour without `--parents`, and BuildKit packing of `--parents` copies.
- `--exclude` syntax (Go `filepath.Match`, repeatable) and that `ADD` takes it too.
- Removed the labs-channel history and `unknown flag` remark, the Git-source `ADD --exclude` example, the `.dockerignore` interplay, the bare-directory `--parents` claim and the cache-key claims, none of which the reference states.

Method: documentation only; no commands were run.
