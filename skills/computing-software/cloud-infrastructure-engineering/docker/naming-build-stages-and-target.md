---
id: computing-software.cloud-infrastructure-engineering.docker.naming-build-stages-and-target
name: naming-build-stages-and-target
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, multi-stage, named-stages, build-target, target-stage, from-as, buildx]
level: practitioner
description: "Name multi-stage build stages with FROM ... AS and build only up to one with --target, for dev/test/prod variants from a single Dockerfile."
sources: ["https://docs.docker.com/build/building/multi-stage/", "https://docs.docker.com/reference/dockerfile/#from", "https://docs.docker.com/build/exporters/local-tar/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Naming stages and building to a target

**Goal:** one Dockerfile that produces a builder, a test image, a debug image and a slim
runtime image, selected with `--target`, without duplicating instructions.

## Naming
```dockerfile
FROM golang AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM build AS test
RUN go test ./...

FROM scratch AS runtime
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
- Stages are numbered from 0 by default; `AS <name>` lets you refer to them by name, so
  re-ordering the Dockerfile does not break `COPY --from`.
- Use lowercase stage names (the `StageNameCasing` build check) that are unique and not the
  reserved words `scratch` or `context`.
- Names work in `FROM <name>`, `COPY --from=<name>` and `RUN --mount=from=<name>`.
- Without `--target`, the build produces the last stage, so put the runtime stage last.

## Building to a target
```sh
docker build --target build -t app:builder .     # stops at the stage named build
docker build --target runtime -t app:1.2 .
```
With BuildKit only the stages the target depends on are built; the legacy builder processes
every stage up to the target, even stages it does not depend on. So `test` is skipped when you
target `runtime` unless `runtime` depends on it (for example via `COPY --from=test`).
Typical uses of `--target`: debugging a stage, a `debug` stage with tools next to a lean
`production` stage, a `testing` stage with test data next to one with real data.

Compose:
```yaml
services:
  app:
    build:
      context: .
      target: runtime
```
Bake: `target "app" { target = "runtime" }`.

## Patterns
- **dev target**: `FROM build AS dev` adding hot-reload tooling; a Compose override points
  `target: dev`, production uses `runtime`.
- **debug target**: a `debug` stage derived from `runtime` that adds tools.
- **Artefact extraction**: `docker build --target build --output type=local,dest=out .` writes
  the stage filesystem to a local directory (local exporter) instead of creating an image.

## Gotchas
- A stage name equal to an image name (`FROM alpine AS alpine`) makes `COPY --from` references
  ambiguous to read; avoid.
- Check `--target` names before sending a large build context.

## Verify
`docker build --target test --progress=plain .` lists the steps that ran; `runtime` steps should
be absent.

## Checked

Checked 2026-10-23 against docker/docs "Multi-stage builds" (naming, stopping at a stage, legacy builder versus BuildKit), the Dockerfile reference (FROM, stage names) and the BuildKit rule pages StageNameCasing and ReservedStageName.
Confirmed: numbered and named stages, `--target`, BuildKit builds only required stages while the legacy builder builds all stages up to the target, the use cases listed. Removed unconfirmed stage-name character rules, the case-insensitivity claim, the exact error message, the log-grep command and pinned image tags.

Method: documentation only; no commands were run.
