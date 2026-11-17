---
id: computing-software.cloud-infrastructure-engineering.docker.rebuild-and-compare-verification-in-ci
name: rebuild-and-compare-verification-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, reproducible-builds, rebuild-compare, source-date-epoch, diffoci, provenance, ci-builds]
level: sme
status: docs-checked
description: "Prove an image is reproducible: build twice in isolation with SOURCE_DATE_EPOCH and rewrite-timestamp, compare digests, and diagnose differences with diffoci in a CI job."
sources: ["https://docs.docker.com/build/ci/github-actions/reproducible-builds/", "https://github.com/moby/buildkit/blob/master/docs/build-repro.md", "https://github.com/reproducible-containers/diffoci"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebuild-and-compare verification

A reproducible build gives the **same digest** from the same source. The test: build twice
independently, with identical inputs, and compare the resulting image digests.

## Build settings that make it possible
```bash
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
docker buildx build --no-cache \
  --output type=image,name=<registry>/<image>:<tag>,push=true,rewrite-timestamp=true .
```
- `SOURCE_DATE_EPOCH` is the standard variable for reproducible output. Docker's docs: setting it
  makes the timestamps in the image index, config and file metadata reflect that Unix time. Use the
  Git commit time, or `0`, as the Docker docs examples do.
- BuildKit (docs `build-repro.md`): the Dockerfile frontend consumes it as a special build arg
  since BuildKit 0.11, and Docker Buildx 0.10 or later propagates the environment value to the
  build arg automatically. A Dockerfile can set a default with `ARG SOURCE_DATE_EPOCH=<n>`.
- `rewrite-timestamp=true` is the image exporter option that applies the value to timestamps of
  the files inside the image; available since BuildKit v0.13.
- Pin base images by digest and package sources (apt snapshot, lock files) so inputs cannot drift.

## The comparison
Run the build twice (fresh builder or cache cleared between runs), then compare the two image
digests; they must be identical. Use the same Buildx and BuildKit versions for both runs. BuildKit's
`compatibility-version` option pins digest-affecting image-assembly behaviour for the image and
oci exporters, which matters when build tooling is upgraded.

## When digests differ
Use `diffoci` (reproducible-containers/diffoci) on the two images:
```bash
diffoci diff --semantic IMAGE0 IMAGE1
diffoci diff --semantic --report-dir=<dir> IMAGE0 IMAGE1
```
- `--semantic` ignores differences of timestamps, image names and other "boring" attributes;
  without it the output can be enormous. It does not understand file formats inside layers, so
  boring in-file differences can remain.
- Image names can be registry references, or `docker://name` / `podman://name` for images that
  are not pushed.
- For multi-platform images or non-Linux hosts pass `--platform=linux/amd64` explicitly
  (platform filtering for `docker://` images requires Docker v28 or later).

## Gotchas
- Compare per platform for multi-platform builds.
- If a difference is in a file's content (not metadata), fix the producer of that file; the
  timestamp options do not change file contents.

## Checked
Checked 2026-10-28 against Docker Docs "Reproducible builds" (GitHub Actions), BuildKit
`docs/build-repro.md` (SOURCE_DATE_EPOCH handling, versions, `rewrite-timestamp`,
`compatibility-version`) and the diffoci README (`--semantic`, `--report-dir`, `docker://`,
`podman://`, `--platform`). Removed as unconfirmed: the `oci-archive://` references and
tar-extraction digest script, `--provenance=false` and its explanation, the full CI job, the list
of typical culprits (`.pyc`, dpkg logs, Go build IDs), and the claim that BuildKit versions
compress layers differently (the docs only describe compatibility-version and zstd history).
Method: documentation only; no commands were run.
