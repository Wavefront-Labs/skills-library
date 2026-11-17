---
id: computing-software.cloud-infrastructure-engineering.docker.image-tagging-strategy-semver-sha-and-latest
name: image-tagging-strategy-semver-sha-and-latest
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, tagging, tag-strategy, semver-tags, latest-tag, ci-tagging, sha-tags, metadata-action]
level: practitioner
description: "Design image tags: immutable git-sha tags, semver major/minor floating tags, branch and PR tags, and when latest is acceptable, generated in CI with metadata-action."
sources: ["https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/", "https://github.com/docker/metadata-action", "https://docs.docker.com/build/ci/github-actions/manage-tags-labels/", "https://docs.docker.com/reference/cli/docker/image/tag/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Image tagging strategy: semver, sha and latest

## A scheme that works
| Tag | Mutable? | Purpose |
|---|---|---|
| `sha-3f2a1c9` | no | exact build; what deploy manifests reference (or the digest) |
| `1.4.2` | no (by policy) | release |
| `1.4`, `1` | yes | consumers who want patch/minor updates |
| `main`, `pr-123` | yes | latest build of a branch/PR, for dev envs |
| `latest` | yes | newest stable release only - never "newest build of main" |
| `1.4.2-alpine`, `1.4.2-debug` | no | variants as suffixes |

Deploy by `sha-*` or `@sha256:`; humans read semver.

## Generating them in CI (GitHub Actions)
```yaml
- uses: docker/metadata-action@v6
  id: meta
  with:
    images: ghcr.io/org/app
    tags: |
      type=sha,format=short
      type=ref,event=branch
      type=ref,event=pr
      type=semver,pattern={{version}}
      type=semver,pattern={{major}}.{{minor}}
      type=semver,pattern={{major}},enable=${{ !startsWith(github.ref, 'refs/tags/v0.') }}
    flavor: |
      latest=auto
- uses: docker/build-push-action@v7
  with:
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
```
Per the metadata-action README: `latest=auto` (the default) generates `latest` for
`type=ref,event=tag`, `type=semver`, `type=pep440` and `type=match` entries; a pre-release
git tag such as `v2.0.8-beta.67` yields only `2.0.8-beta.67` from the semver entry, and a
`v1.2.3` tag yields `1.2.3`, `1.2` and `latest`. `type=sha` produces `sha-<short>` by default
(`format=short`), `type=ref,event=pr` produces `pr-<number>`. To tag `latest` from a branch
instead, use `type=raw,value=latest,enable={{is_default_branch}}`. The action also lowercases
the image name and replaces invalid character sequences in tags with `-`.

## Rules
- Semver build metadata containing `+` is not a safe tag: metadata-action replaces invalid
  character sequences with `-`, so use `-build5` style yourself.
- Promote, don't rebuild: retag the tested `sha-*` image as `1.4.2` (`docker buildx imagetools
  create` or `crane tag`).
- Don't reuse a release tag; turn on immutable tags if your registry offers them.
- Docker's `docker image tag` reference: with no tag, Docker defaults to `latest`, so
  `docker pull app` gets whatever you published as `latest`; if you never want that
  implicit, don't publish it.

## Gotchas
- Floating tags mean different hosts can run different code under one tag if they pulled at
  different times; deploy by digest or immutable tag.

## Verify
`crane ls ghcr.io/org/app` shows the expected set; `crane digest ghcr.io/org/app:1.4.2`
equals `crane digest ghcr.io/org/app:sha-3f2a1c9`.

## Checked
Date: 2026-10-26. Documentation: docker/metadata-action README (latest release v6.2.0), docker/build-push-action latest release v7.4.0, docker/docs `docker image tag` reference. Confirmed: tag type behaviours and tables (`sha-`, `pr-`, semver patterns, latest handling, pre-release exclusion, raw/default-branch expression), invalid-character replacement, default `latest` tag. Fixed: action versions v5 and v6 to the current v6 and v7 majors; the claim that `latest=auto` fires only for the highest semver tag (README: for every tag event of those types, excluding semver pre-releases). Removed as unconfirmed: the tag character regex, GitLab shell snippet, short-SHA collision and imagePullPolicy claims.
Method: documentation only; no commands were run.
