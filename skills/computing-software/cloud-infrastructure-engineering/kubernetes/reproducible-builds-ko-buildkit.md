---
id: computing-software.cloud-infrastructure-engineering.kubernetes.reproducible-builds-ko-buildkit
name: reproducible-builds-ko-buildkit
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, supply-chain, ko-build, buildkit, reproducible-builds, multi-arch]
level: practitioner
status: docs-checked
description: "Build reproducible, multi-arch container images with ko for Go services and BuildKit for Dockerfiles, with pinned bases, SOURCE_DATE_EPOCH, SBOMs and provenance."
sources: ["https://ko.build/", "https://ko.build/configuration/", "https://ko.build/advanced/faq/", "https://ko.build/features/k8s/", "https://github.com/moby/buildkit/blob/master/docs/build-repro.md", "https://docs.docker.com/build/ci/github-actions/reproducible-builds/", "https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/metadata/attestations/slsa-provenance/", "https://docs.docker.com/build/metadata/attestations/sbom/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible builds with ko and BuildKit

Reproducible means the same source gives the same image digest, so anyone can rebuild and
compare with what was signed.

## ko (Go)
```bash
export KO_DOCKER_REPO=registry.internal/payments
ko build ./cmd/server --bare --platform=linux/amd64,linux/arm64 --sbom=spdx --image-refs=refs.txt
ko resolve -f config/ > release.yaml       # replaces ko://example.com/cmd/server with digests
```
```yaml
# .ko.yaml
defaultBaseImage: cgr.dev/chainguard/static@sha256:<digest>
builds:
- id: server
  main: ./cmd/server
  flags: [-trimpath]
  ldflags: ["-s -w -X main.version={{.Env.VERSION}}"]
```
ko does not embed timestamps in the images it produces by default (they appear created in 1970) and
respects `SOURCE_DATE_EPOCH`; `KO_DATA_DATE_EPOCH` sets the modtime of files under `KO_DATA_PATH`.
Its default base image is `cgr.dev/chainguard/static` and, by default, it passes only `-trimpath` to
the Go build. For reproducibility also pin the base image by digest and your Go dependencies.

## BuildKit (any language)
```bash
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
docker buildx build --platform linux/amd64,linux/arm64 \
  --build-arg SOURCE_DATE_EPOCH \
  --output type=image,name=registry.internal/app:1.4,push=true,rewrite-timestamp=true \
  --cache-from type=registry,ref=registry.internal/app:buildcache \
  --cache-to type=registry,ref=registry.internal/app:buildcache,mode=max \
  --provenance=mode=max --sbom=true .
```
BuildKit consumes `SOURCE_DATE_EPOCH` as a special Dockerfile build arg (since BuildKit 0.11), and the
`rewrite-timestamp=true` image exporter option (since BuildKit 0.13) applies it to the timestamps of
files inside the image. Pin every `FROM` by digest (BuildKit's reproducibility page shows source
policies for pinning image references), pin package versions, and avoid `apt-get upgrade` or
downloading "latest" during the build.

## Verify reproducibility
Build twice on different machines from the same commit and compare digests:
```bash
crane digest registry.internal/app:1.4
```
Differences usually come from timestamps, unpinned packages, or file ordering.

## Checked

2026-10-27. Release: ko docs (main), BuildKit docs (master), Docker docs, October 2026
- Confirmed ko flags `--bare`, `--platform`, `--sbom` (default `spdx`) and `--image-refs`, `ko resolve` replacing `ko://` references, default base `cgr.dev/chainguard/static`, the `-trimpath` default, `{{.Env.VERSION}}` ldflags templating, and the 1970 timestamp default with `SOURCE_DATE_EPOCH` and `KO_DATA_DATE_EPOCH` in the ko docs.
- Confirmed in the BuildKit docs the `SOURCE_DATE_EPOCH` build arg (since 0.11) and `rewrite-timestamp=true` (since 0.13), and in Docker's attestation pages `--provenance=mode=max` (modes `min` default and `max`) and `--sbom=true`.
- Confirmed the registry cache backend flags `--cache-to`/`--cache-from type=registry,ref=...` with `mode=min|max` (Docker cache backend page) and the `crane digest IMAGE` command (go-containerregistry docs).

Method: documentation only; no commands were run.
