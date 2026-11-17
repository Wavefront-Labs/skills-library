---
id: computing-software.systems-network-administration.linux.containerfile-builds-with-podman
name: containerfile-builds-with-podman
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, podman, containerfile, podman-build, buildah, multi-stage-build, ubi, rootless-build, build-cache, image-tagging, skopeo, sysadmin]
level: practitioner
status: docs-checked
description: "Build container images with podman build from a Containerfile: base image choice, layer ordering for cache, multi-stage builds, non-root USER, build args/secrets, tagging and pushing."
sources:
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-build.1.md.in
  - https://github.com/containers/container-libs/blob/main/common/docs/Containerfile.5.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-image-tree.1.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containerfile builds with Podman

**Goal:** small, reproducible, non-root images built rootless on a Linux host or CI runner.

## 1. A solid Containerfile
```dockerfile
# Containerfile
FROM registry.example.com/base/python-build:<tag> AS build
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY . .

FROM registry.example.com/base/python-runtime:<tag>
COPY --from=build /install /usr/local
COPY --from=build /src /app
WORKDIR /app
USER 1001
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "app"]
LABEL org.opencontainers.image.version="1.4.2"
```
- Order: rarely-changing layers first (deps), source last — each change invalidates every later layer.
- Pin bases by digest for reproducibility: `FROM <image>@sha256:<digest>`.
- `.containerignore` (or `.dockerignore`) excludes files from the build context.
- Use the exec form of `ENTRYPOINT`/`CMD` (JSON array); the shell form wraps the command in a shell.

## 2. Build
```bash
podman build -t registry.example.com/team/app:1.4.2 -f Containerfile .
podman build --build-arg VERSION=1.4.2 --target build -t app:build .     # stop at a stage
podman build --secret id=npmrc,src=$HOME/.npmrc .      # used in the Containerfile as RUN --mount=type=secret,id=npmrc ...
podman build --platform linux/amd64,linux/arm64 --manifest app:1.4.2 .  # multi-arch; foreign platforms need emulation (qemu)
podman build --layers --no-cache ...                   # cache control
podman image tree app:1.4.2; podman history app:1.4.2  # layer sizes
```
`podman build --format` selects the image format (oci or docker); health checks can also be set when the container is created (`--health-cmd`).

## 3. Push and inspect
```bash
podman login registry.example.com
podman push registry.example.com/team/app:1.4.2
podman image inspect registry.example.com/team/app:1.4.2   # labels and config
```

## Gotchas
- Rootless builds need `/etc/subuid` and `/etc/subgid` ranges for the user.
- `ADD` unpacks a local compressed archive at the destination and can download a URL (the two cannot be combined); use `COPY` unless you want that.
- Secrets passed via `ARG`/`ENV` can end up in image history; use `--secret` instead.
- Bind-mounting host paths with `podman build -v` follows the usual `:z`/`:Z` relabelling rules.

## Verify
- [ ] `podman run --rm app:1.4.2 id` shows a non-root UID; the app starts and its health endpoint responds.
- [ ] Rebuild with only a source change reuses the dependency layers ("Using cache"); image size is as expected in `podman images`.

## Checked
Checked 2026-10-25 against the Podman documentation source on GitHub (containers/podman docs/, main, last commit 2026-10-23; latest release v5.8.9 of 2026-10-12): Containerfile and Dockerfile share syntax (Containerfile is tried first), `FROM ... AS`, `COPY --from`, `ADD` archive-unpacking and URL rules, `USER`, `EXPOSE`, `ENTRYPOINT`/`CMD` exec form, `LABEL`, `podman build` options `-t`, `-f`, `--build-arg`, `--target`, `--secret id=,src=` (and `RUN --mount=type=secret`), `--platform`, `--manifest`, `--layers`, `--no-cache`, `--format`, `.containerignore`/`.dockerignore`, `podman image tree`, `podman history`. Removed unconfirmed claims: distro base image names and package commands, the HEALTHCHECK/OCI-format statement (the Containerfile reference page does not document HEALTHCHECK), the skopeo and jq pipeline, and the qemu-user-static package name.

Method: documentation only; no commands were run.
