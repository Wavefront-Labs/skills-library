---
id: computing-software.systems-network-administration.patch-management.minimal-and-distroless-base-images
name: minimal-and-distroless-base-images
category: computing-software
field: systems-network-administration
product: patch-management
tags: [distroless, minimal-base-image, chainguard, alpine, container-image-patching, patch-management]
level: practitioner
status: docs-checked
description: "Cut container patch load with minimal and distroless base images: Google distroless, Chainguard/Wolfi, Alpine, UBI micro, multi-stage builds, and debugging without a shell."
sources:
  - https://github.com/GoogleContainerTools/distroless
  - https://edu.chainguard.dev/chainguard/chainguard-images/overview/
  - https://docs.docker.com/build/building/multi-stage/
  - https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minimal and distroless base images

Every package in an image is a future CVE to patch. A distroless image for a Go binary has a handful of packages; `ubuntu:22.04` plus build tools has hundreds.

## Options
| Base | Contents | Notes |
|---|---|---|
| `gcr.io/distroless/static-debian13` | smallest distroless image | static binaries (Go, Rust) |
| `gcr.io/distroless/base-debian13` / `cc-debian13` | libc-based bases | dynamically linked binaries |
| `gcr.io/distroless/java21-debian13`, `python3-debian13`, `nodejs22-debian13` | language runtime only | other versions listed in the README |
| Chainguard Containers (Wolfi-based) | minimal images | tag availability and licensing set by Chainguard; check current terms |
| `alpine` | musl libc based | small, but has a shell and package manager; musl differs from glibc |
| Red Hat UBI micro/minimal | RHEL-based minimal images | check Red Hat's UBI documentation for contents and support terms |
| `scratch` | nothing | static binaries, add certs yourself |

## Multi-stage build
```dockerfile
FROM golang:<version> AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```
Pin by digest (`@sha256:...`) and let Renovate/Dependabot bump it so patched bases arrive as PRs.

## Debugging without a shell
- `:debug` distroless tags include a busybox shell (use only for troubleshooting); with an existing tag use `debug-<tag>`, for example `debug-nonroot`.
- `kubectl debug -it <pod> --image=busybox --target=<container>` adds an ephemeral container; `--target` targets the process namespace of another container.

## Gotchas
- Confirm your scanner reports OS packages for distroless images before relying on a clean result.
- musl behaves differently from glibc; test the workload on Alpine.
- Minimal images still need rebuilding when the base is patched; fewer CVEs, not zero maintenance.

## Verify
Scanner package count and CVE count before/after migration recorded; image runs as non-root; automated base digest bumps merge regularly.

## Checked
Date: 2026-10-27. Documentation checked: Google distroless README (images are based on Debian 13 and tagged `-debian13`; image names; `latest`, `nonroot`, `debug`, `debug-nonroot` tags; busybox shell in `:debug`), Kubernetes "Debug Running Pods" page (`kubectl debug --image --target`). The old `-debian12` names are no longer listed. Removed unconfirmed Chainguard release-cadence and pricing claims, the UBI `microdnf` detail, the distroless image-content list and the `dpkg/status.d` claim.

Method: documentation only; no commands were run.
