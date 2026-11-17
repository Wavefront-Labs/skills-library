---
id: computing-software.cybersecurity-defensive.system-hardening.distroless-minimal-images
name: distroless-minimal-images
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [container-hardening, distroless-images, minimal-base-image, multi-stage-build, scratch-image, image-attack-surface]
level: practitioner
status: docs-checked
description: "Build minimal container images with multi-stage builds onto distroless or scratch bases, keep them debuggable with debug tags or ephemeral containers, and compare scan results."
sources: ["https://github.com/GoogleContainerTools/distroless", "https://docs.docker.com/build/building/multi-stage/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distroless and minimal images

**Goal:** production images contain the app and its runtime only - no shell, package manager or build tools - shrinking CVE counts and post-exploitation tooling.

## Multi-stage pattern
Docker multi-stage builds use several `FROM` lines; each starts a new stage and you copy only the artifacts you want
into the final one (`COPY --from=<stage>`), leaving the SDK and intermediate files behind.
```dockerfile
FROM golang:<GO_VERSION> AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
Base choices (distroless README):
- Images are published per Debian release (`-debian13` at the time of checking) with tags `latest`, `nonroot`,
  `debug` and `debug-nonroot`: `static`, `base`, `base-nossl`, `cc`, `java-base`, `java17`/`java21`/`java25`,
  `nodejs22`/`nodejs24`/`nodejs26`, `python3`. Check the README for the current set.
- They contain no package manager or shell. The `static` image is the smallest distroless image.
- `scratch` is Docker's empty base for a fully static binary.
- All distroless images are signed with cosign (keyless); the README gives the `cosign verify` command to run
  before building on one.

## Debugging without a shell
- `:debug` tags include a busybox shell (`debug-<tag>`, e.g. `debug-nonroot`, when the image already has a tag);
  use them only outside production.
- Kubernetes ephemeral containers: `kubectl debug -it <pod> --image=busybox:<tag> --target=<container>`;
  `--target` shares the process namespace and must be supported by the container runtime.

## Measure
Compare before/after with your image scanner and a package/SBOM listing, and track the result in the image pipeline.

## Gotchas
- `ENTRYPOINT` must be in exec (vector) form: with no shell in the image, shell form fails.
- By default the `static`, `base` and `cc` images have an empty entrypoint; runtime images (java, nodejs, python3)
  have a language-specific default.
- Minimal does not mean never patched: rebuild on base-image updates and pin by digest.

## Verify
- [ ] `docker run --rm --entrypoint sh <image>` fails (no shell) for the production tag.
- [ ] The scanner shows fewer packages and no high/critical OS CVEs than the previous base.

## Checked
2026-10-31. Confirmed in the distroless README (image names, tags, no shell or package manager, exec-form
ENTRYPOINT note, default entrypoints, `debug` tags with busybox, cosign signing), Docker multi-stage page
(`FROM`, `AS`, `COPY --from`, `scratch`) and the Kubernetes debug page (`kubectl debug -it ... --target`).
Removed as unconfirmed: the `debian12` tag and UID 65532 claim, glibc/musl and Alpine remarks, named vendor
hardened-image products, adding CA certs and `/etc/passwd` to `scratch`, `docker debug`, specific scanner commands.
Method: documentation only; no commands were run.
