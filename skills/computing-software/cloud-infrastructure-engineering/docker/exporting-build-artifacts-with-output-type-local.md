---
id: computing-software.cloud-infrastructure-engineering.docker.exporting-build-artifacts-with-output-type-local
name: exporting-build-artifacts-with-output-type-local
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, multi-stage, output-type-local, export-artifacts, build-output, buildx, scratch-stage]
level: practitioner
status: docs-checked
description: "Use Docker as a build tool: export binaries, test reports or coverage from a scratch stage with --output type=local or type=tar, including multi-platform layouts."
sources: ["https://docs.docker.com/build/exporters/local-tar/", "https://docs.docker.com/build/exporters/", "https://docs.docker.com/reference/cli/docker/buildx/build/#output", "https://docs.docker.com/build/building/multi-stage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting artifacts from a stage

Instead of building an image, write a stage's filesystem to the host. The `docker` driver
supports the `local`, `tar` and `image` exporters; the `docker-container` driver supports all.

## Pattern
```dockerfile
# syntax=docker/dockerfile:1
FROM golang AS build
WORKDIR /src
COPY . .
RUN mkdir /out && go test ./... -coverprofile=/out/coverage.out && \
    CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM scratch AS export
COPY --from=build /out/ /
```
```bash
docker build --target export --output type=local,dest=./dist .
# shorthand
docker build --target export -o ./dist .
ls dist/            # app  coverage.out
```
The `local` and `tar` exporters output the root filesystem of the build result, so export from
`scratch` to get only the artifacts on disk. New files are owned by the current user.

## Variants
```bash
docker build --target export -o type=tar,dest=dist.tar .        # single tarball
docker build --target export -o - . > dist.tar                   # tar to stdout
docker buildx build --platform linux/amd64,linux/arm64 --target export -o ./dist .
# dist/linux_amd64/app  dist/linux_arm64/app  (platform-split defaults to true)
docker buildx build --platform linux/amd64,linux/arm64 --target export \
  -o type=local,dest=./dist,platform-split=false .              # flat; identical file names make the export fail
```

## Uses
- Release binaries for several OS/arch from one Dockerfile (cross-compile with
  `--platform=$BUILDPLATFORM` in the build stage).
- Test results and coverage out of a CI build without `docker cp`.
- Generated code (protobuf, OpenAPI clients) produced in a pinned toolchain.

## Gotchas
- A failing test fails the build and nothing is exported. To always export reports, have the
  test step write the exit code to a file (`go test ... ; echo $? > /out/exit`) and fail in CI.
- The `local` exporter's `mode` is `copy` by default; `mode=delete` removes stale files from
  `dest` and needs `--allow=buildx.local.delete` unless `dest` is a subdirectory of the current
  working directory.
- A single-platform build exports straight into `dest`; set `platform-split=true` to get the
  platform subdirectory anyway.
- A path given to `-o` selects the `local` exporter and `-` selects `tar` to stdout; `--output`
  replaces the default image export, so no image is loaded unless you add one.

## Verify
```bash
docker build --target export -o ./dist . && file dist/app
```

## Checked

Checked 2026-10-23 against the Docker docs "Local and tar exporters" and "Exporters" pages and the docker/buildx `build --output` reference (main branches).

- `type=local` / `type=tar`, `dest`, `platform-split` (default true; identical names fail when false), `mode=copy|delete` with `--allow=buildx.local.delete`, `-o ./dir` shorthand and `-o -` for tar on stdout.
- Driver support: `docker` driver supports local, tar and image exporters; `docker-container` supports all.
- Fixed the example Dockerfile (`mkdir /out` before writing there) and removed the pinned Go tag and the unconfirmed file-mode claim.

Method: documentation only; no commands were run.
