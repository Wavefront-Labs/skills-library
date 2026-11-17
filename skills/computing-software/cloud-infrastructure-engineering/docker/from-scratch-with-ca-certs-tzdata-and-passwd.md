---
id: computing-software.cloud-infrastructure-engineering.docker.from-scratch-with-ca-certs-tzdata-and-passwd
name: from-scratch-with-ca-certs-tzdata-and-passwd
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, image-slimming, scratch, scratch-ca-certificates, scratch-passwd, static-binary, ca-certificates, tzdata, empty-base]
level: advanced
description: "Build a working FROM scratch image: static binary plus the things it will miss (CA certificates, zoneinfo or embedded tzdata, /etc/passwd for a non-root user)."
sources: ["https://docs.docker.com/build/building/base-images/#create-a-minimal-base-image-using-scratch", "https://hub.docker.com/_/scratch", "https://pkg.go.dev/time/tzdata"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FROM scratch: the essentials a static binary still needs

**Goal:** a minimal image that holds only what the application needs, yet can still make HTTPS calls, resolve time zones and run as a non-root user.

## What scratch is
`scratch` is Docker's reserved, minimal image. It appears on Docker Hub, but you cannot pull it, run it or tag an image with that name; you only refer to it in a Dockerfile. `FROM scratch` is a no-op that adds no layer: the next instruction becomes the first filesystem layer. Docker's docs warn that building a base this way is hard for anything beyond small, simple programs, which is why you must copy in everything the binary needs.

## Build (Go example)
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:<VERSION>-alpine AS build
RUN apk add --no-cache ca-certificates tzdata
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app .
# a passwd entry for the runtime user
RUN echo 'app:x:10001:10001::/nonexistent:/sbin/nologin' > /out/passwd \
 && echo 'app:x:10001:' > /out/group

FROM scratch
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=build /out/passwd /etc/passwd
COPY --from=build /out/group /etc/group
COPY --from=build --chown=10001:10001 /out/app /app
USER app
ENTRYPOINT ["/app"]
```

## Why each piece
- **CA certificates**: scratch contains no certificate bundle, so copy one in from the build stage for TLS clients.
- **Time zones**: copy `/usr/share/zoneinfo`, or in Go import `time/tzdata`, which embeds a copy of the timezone database used when the system has none. It adds about 450 KB to the program; building with `-tags timetzdata` imports it automatically (pkg.go.dev `time/tzdata`).
- **/etc/passwd and /etc/group**: copied from the build stage so the image carries the `app` user entry referenced by `USER app`.
- **Binary**: build it statically (for Go, `CGO_ENABLED=0`), because the image contains nothing but what you copy in.

## Gotchas
- scratch has no shell: use exec-form `ENTRYPOINT`; `docker run --rm scratch` cannot work because the image cannot be run.

## Checked
2026-10-28. Confirmed against Docker's "Create a minimal base image using scratch" page, the Docker Hub scratch page (reserved image, cannot pull or run, no-op) and the Go `time/tzdata` package page (embedded database, about 450 KB, `-tags timetzdata`). Removed unconfirmed claims: exact TLS error text and env vars, Rust and C static flags, `ldflags` size tuning, `getpwuid`/Kubernetes `runAsNonRoot` behaviour, healthcheck and debugging advice, size figures, multi-platform notes.
Method: documentation only; no commands were run.
