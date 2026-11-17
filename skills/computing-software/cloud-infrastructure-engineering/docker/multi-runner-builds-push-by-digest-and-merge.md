---
id: computing-software.cloud-infrastructure-engineering.docker.multi-runner-builds-push-by-digest-and-merge
name: multi-runner-builds-push-by-digest-and-merge
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, multi-platform, push-by-digest, merge-manifests, imagetools, github-actions, native-builders, arm64]
level: advanced
status: docs-checked
description: "Build each platform natively on its own CI runner, push untagged by digest, then merge the digests into one tagged multi-arch index with buildx imagetools create."
sources: ["https://docs.docker.com/build/ci/github-actions/multi-platform/", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/", "https://docs.docker.com/build/exporters/image-registry/", "https://docs.docker.com/reference/cli/docker/buildx/build/#metadata-file"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-runner builds: push by digest, then merge

Building several platforms on one runner can significantly extend build times. With native
runners per platform, build each platform separately, push by digest, and stitch the results
into one manifest list. (Docker's current GitHub Actions docs recommend the Docker GitHub
Builder reusable workflows, `docker/github-builder`, which distribute platforms across runners
and create the final manifest for you; the manual pattern below shows the mechanics.)

## Build job (matrix per platform)
```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - { platform: linux/amd64, runner: ubuntu-24.04 }
          - { platform: linux/arm64, runner: ubuntu-24.04-arm }
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: docker/login-action@v4
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/setup-buildx-action@v4
      - id: build
        uses: docker/build-push-action@v7
        with:
          platforms: ${{ matrix.platform }}
          outputs: type=image,"name=ghcr.io/org/app",push-by-digest=true,name-canonical=true,push=true
          cache-from: type=gha,scope=${{ matrix.platform }}
          cache-to: type=gha,scope=${{ matrix.platform }},mode=max
      - run: |
          mkdir -p ${{ runner.temp }}/digests
          d="${{ steps.build.outputs.digest }}"; touch "${{ runner.temp }}/digests/${d#sha256:}"
      - uses: actions/upload-artifact@v7
        with:
          name: digests-${{ strategy.job-index }}
          path: ${{ runner.temp }}/digests/*
          retention-days: 1
```

## Merge job
```yaml
  merge:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/download-artifact@v8
        with: { path: ${{ runner.temp }}/digests, pattern: digests-*, merge-multiple: true }
      - uses: docker/login-action@v4
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/setup-buildx-action@v4
      - id: meta
        uses: docker/metadata-action@v6
        with: { images: ghcr.io/org/app, tags: "type=sha\ntype=semver,pattern={{version}}" }
      - working-directory: ${{ runner.temp }}/digests
        run: |
          docker buildx imagetools create \
            -t ghcr.io/org/app:${{ steps.meta.outputs.version }} \
            $(printf 'ghcr.io/org/app@sha256:%s ' *)
      - run: docker buildx imagetools inspect ghcr.io/org/app:${{ steps.meta.outputs.version }}
```

## Without GitHub Actions
```bash
# on each native host; the digest is written to the metadata file as "containerimage.digest"
docker buildx build --platform linux/arm64 \
  --output type=image,name=reg.example.com/app,push-by-digest=true,name-canonical=true,push=true \
  --metadata-file meta-arm64.json .
# anywhere: pass the digests read from the metadata files
docker buildx imagetools create -t reg.example.com/app:1.4.0 \
  reg.example.com/app@sha256:<amd64 digest> \
  reg.example.com/app@sha256:<arm64 digest>
```

## Gotchas
- `push-by-digest=true` pushes the image without a name tag (the `image` exporter's "push image
  without name"); `name-canonical=true` adds the canonical `name@<digest>` name. The tags come
  from the later `imagetools create` step.
- `imagetools create` builds a new manifest list from source manifests that must already exist
  in the registry where the new manifest is created.
- Use per-platform cache scopes; the `gha` cache identifies objects by scope, so builds sharing
  a scope share (and overwrite) one cache.

## Checked

Checked 2026-10-23 against the Docker docs GitHub Actions multi-platform page, the image/registry exporter page, the docker/buildx `imagetools create` and `build --metadata-file` references, and the READMEs and releases of docker/build-push-action, docker/metadata-action, docker/login-action, docker/setup-buildx-action, actions/upload-artifact and actions/download-artifact (main branches and releases API).

- Current majors: login-action v4, setup-buildx-action v4, build-push-action v7, metadata-action v6, upload-artifact v7, download-artifact v8 (the draft used older majors); `digest` output of build-push-action; `merge-multiple` and `pattern` inputs of download-artifact.
- `push-by-digest` and `name-canonical` exporter parameters; `imagetools create` requirements; `--metadata-file` writes `containerimage.digest`; Docker GitHub Builder reusable workflow and its default `ubuntu-24.04-arm` runner for Arm platforms.
- Removed the 5-20x emulation figure, the `jq` pipelines (not in any current documentation), and the registry-retention and attestation-merge claims.

Method: documentation only; no commands were run.
