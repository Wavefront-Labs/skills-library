---
id: computing-software.cloud-infrastructure-engineering.docker.building-images-in-ci
name: building-images-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ci, ci-cd, github-actions, gitlab-ci, build-push-action, ci-builds, buildx, metadata-action, gha-cache, kaniko, docker-dind, ghcr, oidc, provenance, gitlab-dind, gitlab-kaniko]
level: practitioner
status: docs-checked
description: "The standard CI image pipeline on GitHub Actions and GitLab CI: buildx setup, metadata-action tags, registry login, cache-from/to, multi-platform, provenance, and dind vs kaniko on GitLab."
sources: ["https://docs.docker.com/build/ci/github-actions/", "https://github.com/docker/build-push-action", "https://github.com/docker/metadata-action", "https://github.com/GoogleContainerTools/kaniko", "https://docs.gitlab.com/ci/docker/using_docker_build/", "https://docs.gitlab.com/ci/docker/using_kaniko/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Building and pushing images in CI

**Goal:** every push builds the image once, tags it predictably (sha, branch, semver),
caches layers between runs, pushes to the registry with a short-lived credential, and
emits provenance — in a workflow you can copy between repos.

## GitHub Actions: the canonical workflow
```yaml
name: image
on:
  push: {branches: [main], tags: ['v*']}
  pull_request:
permissions:
  contents: read
  packages: write          # GHCR push with GITHUB_TOKEN; no PAT needed
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-qemu-action@v4          # only if building non-native platforms
      - uses: docker/setup-buildx-action@v4
      - uses: docker/login-action@v4
        with: {registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }}}
      - id: meta
        uses: docker/metadata-action@v6
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,format=long
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=raw,value=latest,enable={{is_default_branch}}
      - uses: docker/build-push-action@v7
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          annotations: ${{ steps.meta.outputs.annotations }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: mode=max
          sbom: true
```
- `setup-buildx-action` creates a buildx builder (docker-container driver by default); the default
  `docker` driver lacks multi-arch and tarball output, and supports cache export only for some backends with the containerd image store.
- `push: false` on PRs still builds (and can `load: true` for a test step — but `load`
  only works single-platform).
- `cache-to: type=gha,mode=max` stores every stage's layers in the Actions cache (GitHub's
  default limit is 10 GB per repository, and entries unused for 7 days are removed). For
  monorepos or big images use `type=registry,ref=ghcr.io/org/app:buildcache` instead.
- `metadata-action` also emits OCI labels and annotations. `type=sha,format=long` gives the full
  commit SHA as a tag (default is the short form with a `sha-` prefix).
- Secrets into the build: `secrets: |` on `build-push-action` → `RUN --mount=type=secret`,
  never `build-args`.
- For signing after push see the cosign skills in this folder.
- `docker/bake-action` replaces `build-push-action` when a `docker-bake.hcl` defines several
  targets; `metadata-action`'s `bake-file` output feeds tags into it.
- Pin actions to a SHA in regulated repos; Dependabot can keep them current.
- Check the latest major version of each action before copying the workflow; the majors above are the ones current at the check date.

## GitLab CI
Two choices, pick deliberately:
```yaml
build:
  image: docker:<version>-cli          # pin a version, as GitLab's examples do
  services: ["docker:<version>-dind"]
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  script:
    - docker buildx create --use
    - docker buildx build --push
        --cache-from type=registry,ref=$CI_REGISTRY_IMAGE:buildcache
        --cache-to   type=registry,ref=$CI_REGISTRY_IMAGE:buildcache,mode=max
        --platform linux/amd64,linux/arm64
        -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -t $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG .
```
- **docker:dind** needs the runner's executor configured with `privileged = true` in
  `config.toml`, which is a security decision: any job can root the runner VM. Fine for
  dedicated ephemeral runners, not for shared ones. GitLab's docs describe Docker socket
  binding as the alternative.
- **Kaniko** is archived (the GoogleContainerTools/kaniko repository is archived and its README
  says it is no longer developed or maintained), and GitLab's kaniko page now says it is
  removed and recommends Docker, Buildah or Podman instead. GitLab's docker-build page has a
  Buildah example that logs in with `buildah login -u "$CI_REGISTRY_USER" --password-stdin
  $CI_REGISTRY`; use that or the Docker-in-Docker flow above for new pipelines.

## Patterns regardless of CI
- Build once, promote by retagging (`crane tag` / `docker buildx imagetools create -t
  app:prod app@sha256:...`) rather than rebuilding per environment.
- Export the digest from the build step and deploy by digest.
- Run tests against the built image in the same job (`docker run app:sha npm test`) before
  push, or push as `:sha` first and only add `:latest`/semver after tests.
- Keep the build context small (`.dockerignore` with `.git`, `node_modules`, test fixtures)
  — context upload is often most of the CI time.

## Verify
`docker buildx imagetools inspect ghcr.io/org/app:<sha>` lists both platforms plus
attestation manifests; a second run of the workflow with no code change should show `CACHED`
for every layer.

## Checked

2026-10-26 against docker/docs main (2026-10-23), action repositories at their latest releases, gitlabhq/gitlabhq doc/. Confirmed: latest majors of build-push-action (v7), metadata-action (v6), setup-buildx-action (v4), login-action (v4), setup-qemu-action (v4) from the repositories' releases and README examples (earlier text used v3/v5/v6); build-push-action inputs (annotations, provenance, sbom, load, push, cache-from, cache-to, secrets); metadata-action type=sha format and bake-file output; GitHub cache limit and eviction; kaniko archived and GitLab kaniko page marked removed; GitLab privileged runner setting and Buildah example. Removed the unconfirmed GitLab TLS, DOCKER_BUILDKIT, CI_JOB_TOKEN and kaniko flag details, the pinned docker:27 tag and the timing claim.

Method: documentation only; no commands were run.
