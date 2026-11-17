---
id: computing-software.cloud-infrastructure-engineering.docker.wolfi-and-chainguard-images
name: wolfi-and-chainguard-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, image-slimming, wolfi, chainguard-images, cgr-dev, apko, melange, distroless, low-cve, glibc-distroless]
level: practitioner
description: "Use Chainguard Wolfi images (cgr.dev) as minimal bases with -dev variants, know free vs production tags, and build with apko."
sources: ["https://edu.chainguard.dev/chainguard/chainguard-images/overview/", "https://github.com/wolfi-dev/os", "https://github.com/chainguard-dev/apko", "https://edu.chainguard.dev/chainguard/chainguard-images/working-with-images/image-variants/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Wolfi and Chainguard images

**Goal:** a minimal, apk-managed, low-CVE base that is as small as distroless but has a
shell and package manager in its `-dev` variant, and know what the free tier does not give you.

## What Wolfi is
Wolfi is a lightweight GNU software distribution designed around minimalism for containerised
environments built with `apko`. Its packages are built with `melange`, and it is sponsored by
Chainguard, which uses it for its runtime images. The apk repository is
`https://packages.wolfi.dev/os` and the signing key is
`https://packages.wolfi.dev/os/wolfi-signing.rsa.pub`. Wolfi is not a general-purpose desktop OS,
and packages need an open-source licence.

## Image layout
- `cgr.dev/chainguard/<name>:latest` is the runtime image; the `-dev` variant (`:latest-dev`) typically
  adds a shell and tools such as a package manager, to debug and modify the image. Use it in build
  stages, not in what you ship.
- Free images need no authentication but are limited to the latest build, tagged `latest` and
  `latest-dev`. The Containers Directory (images.chainguard.dev) lists which images are free.
- Production images offer specific major and minor versions, patch SLAs and unique time-stamped
  tags, and need an authenticated Chainguard organisation.
- `cgr.dev/chainguard/wolfi-base` is the quickest way to try Wolfi (`docker run -it cgr.dev/chainguard/wolfi-base`).

## Typical multi-stage
```dockerfile
FROM cgr.dev/chainguard/python:latest-dev AS build
WORKDIR /app
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest
WORKDIR /app
COPY --from=build /venv /venv
COPY . .
ENV PATH=/venv/bin:$PATH
ENTRYPOINT ["python", "app.py"]
```
Both stages come from the same image family, so the venv's interpreter path matches.

## Mixing with other distributions
Mixing Wolfi packages with other distributions is not supported. Wolfi and Alpine both use apk,
but their packages are not compatible with each other, so do not copy Alpine package names or
repositories into a Wolfi image.

## Building your own with apko
apko builds OCI images declaratively from apk packages: no `RUN` steps, bitwise reproducible by
default, with an SBOM produced for every image.
```shell
apko build apko.yaml my-app:latest out.tar
docker load < out.tar
```
Anything bespoke must first be packaged as an apk with `melange`. See the apko file-format docs
for the YAML (`contents.repositories`, `contents.packages`, `entrypoint`). Where apko is not a fit,
build a base with apko and melange and finish with a Dockerfile.

## Gotchas
- The free `latest` tag is a moving target across versions; pin by digest and let a dependency
  bot bump it, or use Production images for version tags.
- Scanner "0 CVEs" is for the base; your app's dependencies still count.
- Runtime images have no shell; debug with the `-dev` variant.

## Verify
`docker run --rm cgr.dev/chainguard/python:latest --version` prints a Python version; the Containers
Directory page of an image shows its CVE comparison against its upstream image.

## Checked
2026-11-09. Confirmed against the Chainguard overview page, the Chainguard image-variants page, the wolfi-dev/os README and the apko README: Wolfi definition, repository and key URLs, the `-dev` variant, free-image limit to latest/latest-dev, production versioned tags, apko declarative/reproducible/SBOM behaviour, and the not-supported mixing note.
Removed as unsupported by those sources: the uid 65532 and nonroot claim, `static` image equivalence, the exact free-image list, the apko YAML sample with accounts and archs, the cosign certificate-identity command, the Alpine-comparison claims, "no stable release branches", and the `COPY --chown` advice.
Method: documentation only; no commands were run.
