---
id: computing-software.software-engineering.go.minimal-container-images-for-go-binaries
name: minimal-container-images-for-go-binaries
category: computing-software
field: software-engineering
product: go
tags: [go, go-release-ops, go-docker-multistage, docker, multistage, distroless, scratch, static-binary]
level: practitioner
status: docs-checked
description: "Build small, reproducible container images for Go services with multi-stage builds, CGO_ENABLED=0, distroless or scratch bases and non-root users."
sources:
  - https://docs.docker.com/build/building/multi-stage/
  - https://github.com/GoogleContainerTools/distroless
  - https://go.dev/doc/modules/managing-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Minimal container images for Go binaries

**Goal:** a small image with no shell, built in a multi-stage Dockerfile and running as non-root.

```dockerfile
FROM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```

In a multi-stage build the final stage starts a new `FROM` and `COPY --from=build` copies only the artifact, so the Go SDK and intermediate files are left behind. Copy `go.mod`/`go.sum` first so the dependency layer caches. `CGO_ENABLED=0` builds without cgo, which keeps the binary free of C library dependencies so it can run on `scratch` or distroless static; the distroless project also ships `base` and `cc` images and a `static` image that is the smallest. Distroless tags include `latest`, `nonroot`, `debug` and `debug-nonroot`; the `debug` variants add a busybox shell. Current image names on the project page use `-debian13`.

## Gotchas
- Distroless images have no shell: use a `:debug` tag temporarily to get one, not in production.
- Pick the `nonroot` tag rather than the default when the service does not need root.
- Read-only root filesystems need a writable scratch location for temp files; provide one at runtime.

## Verify
Run the image with the container runtime and confirm the service starts as the non-root user; compare image size against the build stage's.

## Checked
2026-11-03. Confirmed against docs.docker.com multi-stage page (`FROM ... AS`, `COPY --from`, artifact-only final stage) and the distroless README (image set, `nonroot`/`debug`/`debug-nonroot` tags, busybox shell in debug, static is smallest). Removed: size target, `--mount` cache syntax, `-ldflags -s -w` advice, tzdata/CA copy, `ko`, `GODEBUG=netdns=go`, digest pinning and scanner advice, specific docker flags (all not on the cited pages). Image tag moved from debian12 to debian13 per the README.
Method: documentation only; no commands were run.
