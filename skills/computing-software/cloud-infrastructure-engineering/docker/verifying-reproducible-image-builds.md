---
id: computing-software.cloud-infrastructure-engineering.docker.verifying-reproducible-image-builds
name: verifying-reproducible-image-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, reproducible-builds, source-date-epoch, rewrite-timestamp, deterministic-layers, file-ordering, diffoci, image-diff, buildkit]
level: sme
description: "Get bit-identical images from BuildKit with SOURCE_DATE_EPOCH and rewrite-timestamp, remove remaining nondeterminism, and find differences with diffoci."
sources: ["https://docs.docker.com/build/ci/github-actions/reproducible-builds/", "https://github.com/moby/buildkit/blob/master/docs/build-repro.md", "https://github.com/reproducible-containers/diffoci", "https://reproducible-builds.org/docs/source-date-epoch/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Verifying reproducible image builds

## Timestamps
```sh
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
docker buildx build --build-arg SOURCE_DATE_EPOCH \
  --output type=image,name=<REGISTRY>/app:<TAG>,push=true,rewrite-timestamp=true .
```
- The Dockerfile frontend consumes `SOURCE_DATE_EPOCH` as a special build arg since BuildKit 0.11; Docker Buildx (>= 0.10) propagates the client's `SOURCE_DATE_EPOCH` environment value. It sets the `created` timestamp in the OCI image config and its history objects, and the `org.opencontainers.image.created` annotation.
- To apply the value to file timestamps **inside the image**, add `rewrite-timestamp=true` to the image exporter (available since BuildKit v0.13). It is off by default because of the overhead of rewriting layers.
- Base images: pin by digest, or the bits change under you.

## Remaining nondeterminism (and fixes)
| Source | Fix |
|---|---|
| package manager pulls latest | snapshot repos (`snapshot.debian.org`), lockfiles with hashes |
| timestamps written by your own tools | pass `SOURCE_DATE_EPOCH` to them (the reproducible-builds.org spec) |
| random/hostname/time in generated files | avoid or seed from `SOURCE_DATE_EPOCH` |

Other sources (logs, caches, bytecode, tar ordering, locale, compiler build IDs, provenance attestations) vary by toolchain: find them with `diffoci` below instead of guessing.

## Comparing two builds
```sh
diffoci diff --semantic IMAGE0 IMAGE1
diffoci diff docker://<IMAGE0> docker://<IMAGE1> --semantic --report-dir=<DIR>
```
`--semantic` ignores timestamps, image names and other "boring" attributes; without it diffoci may print an enormous amount of output. diffoci does not know the formats of files inside layers, so some boring differences remain. For multi-platform images from Docker add `--platform=linux/amd64` (platform filtering for `docker://` images needs Docker v28+).

## Gotchas
- A cached second build trivially reproduces; use `--no-cache` for an honest comparison.

## Verify
Two clean builds give the same image digest, and `diffoci diff` prints nothing.

## Checked
2026-10-28. Confirmed against BuildKit `build-repro.md` (SOURCE_DATE_EPOCH since 0.11, `rewrite-timestamp` since v0.13, what it sets), the reproducible-builds.org SOURCE_DATE_EPOCH page (Buildx 0.10 propagation, off by default) and the diffoci README (`--semantic`, `--report-dir`, `--platform`, Docker v28+). Removed unconfirmed claims: the nondeterminism fix table entries for logs, tar flags, umask, locale, Go/C flags and provenance, `--chmod`, blob-digest and compression gotchas.
Method: documentation only; no commands were run.
