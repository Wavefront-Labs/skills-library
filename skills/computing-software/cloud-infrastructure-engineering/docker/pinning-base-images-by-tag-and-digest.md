---
id: computing-software.cloud-infrastructure-engineering.docker.pinning-base-images-by-tag-and-digest
name: pinning-base-images-by-tag-and-digest
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, base-image, digest-pinning, sha256-digest, tag-plus-digest, image-pinning, reproducible, supply-chain, from-digest]
level: practitioner
description: "Pin FROM lines as tag@sha256 digests so builds are reproducible and tamper-evident, find the right digest for your platform, and keep the pins readable and updatable."
sources: ["https://docs.docker.com/reference/dockerfile/#from", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/", "https://docs.docker.com/build/building/best-practices/#pin-base-image-versions", "https://docs.renovatebot.com/docker/", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_digest.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning base images by digest

**Goal:** `FROM python:3.12-slim` can resolve to a different image next month; a digest pin
means the same image every build, and a changed digest is a visible diff in code review.
Docker's best-practices guide describes this trade-off: tags are mutable, and pinning to a
digest guarantees the same image even if the publisher replaces the tag.

## Syntax
```dockerfile
FROM python:3.12-slim-bookworm@sha256:<digest> AS build
```
Keep the tag **and** the digest, as Docker's guide does (`FROM alpine:3.21@sha256:...`): the
digest is what is pulled; the tag tells humans and update tools which release you intend.

## Getting the digest
```sh
docker buildx imagetools inspect python:3.12-slim-bookworm      # digest of the index and its manifests
docker manifest inspect -v python:3.12-slim-bookworm
crane digest python:3.12-slim-bookworm                           # no daemon needed
docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim-bookworm  # of what you pulled
```
Pin the **index (manifest list) digest** for multi-platform images unless you deliberately
want one architecture.

## Where to pin
- Every `FROM`, including builder stages and `COPY --from=image`.
- The Dockerfile frontend can be pinned too: `# syntax=docker/dockerfile:1@sha256:...`.
- Compose `image:` for third-party services you deploy.
- For your own images in dev loops, pin on promotion rather than on every build.

## Keeping pins fresh
Pinning to a digest opts you out of automatic security fixes (Docker's guide says so), so pair
pins with an update mechanism. Renovate's documentation recommends pinning Docker images to an
exact digest and has `pinDigests` support for the docker datasource (see the Renovate Docker
docs); Docker Scout's "No outdated base images" policy also flags a pinned digest that is out
of date. See `automating-base-image-updates-with-renovate-and-dependabot`.

## Verifying a pin
```sh
docker pull python@sha256:<digest>        # succeeds only for an existing manifest
docker buildx imagetools inspect python@sha256:<digest>
```
`docker build --pull` always attempts to pull a newer version of the `FROM` image, which still
helps for unpinned lines.

## Gotchas
- The full digest (`sha256:` plus 64 hex characters) must appear in the Dockerfile.
- Digest pins do not freeze packages installed during the build (`apt-get install`); pin those
  separately.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed in Docker's build best-practices guide (pin base image versions), the docker build --pull option, docker manifest inspect --verbose, crane digest, and the Renovate Docker documentation on digest pinning. Removed unconfirmed claims about mirrors and compression changing digests, RepoDigests listing several digests, legacy builder truncation, snapshot.debian.org and the layer-size verification.

Method: documentation only; no commands were run.
