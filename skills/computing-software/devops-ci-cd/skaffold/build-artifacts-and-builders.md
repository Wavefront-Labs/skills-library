---
id: computing-software.devops-ci-cd.skaffold.build-artifacts-and-builders
name: build-artifacts-and-builders
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [build, artifacts, builders, docker, buildpacks]
level: intro
status: docs-checked
description: "Define images in build.artifacts and choose a builder per image: Docker, Jib, Buildpacks, Bazel, ko or a custom script."
sources:
  - "https://skaffold.dev/docs/builders/"
  - "https://skaffold.dev/docs/references/cli/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`build.artifacts` lists the images Skaffold builds. Each entry has an `image` name (the only required field) and one builder block; `context` defaults to `.`, the directory containing the artifact's sources.

```yaml
build:
  artifacts:
  - image: my-registry/web
    context: web
    docker:
      dockerfile: Dockerfile
  - image: my-registry/api
    context: api
    jib: {}
```

Builders documented: `docker`, `jib`, `buildpacks`, `bazel`, `ko` and `custom`. Different artifacts in one config can use different builders.

Where the build runs is a separate choice, and not every builder supports every environment:

| Builder | Local | In cluster | Google Cloud Build |
|---|---|---|---|
| Dockerfile | yes | yes (Kaniko) | yes |
| Jib | yes | no | yes |
| Buildpacks | yes | no | yes |
| Bazel | yes | no | no |
| ko | yes | no | yes |
| Custom script | yes | yes | no |

Practical points:

- Skaffold templates the newly built, tagged image into your manifests in place of the `image` reference.
- Build only some images with `skaffold build -b web`; `-b/--build-image` matches image names that contain the given substring.
- Caching is on by default (`--cache-artifacts=true`); the cache file defaults to `$HOME/.skaffold/cache` and can be changed with `--cache-file`.

Print what would be built without building via `skaffold build --dry-run` (it only computes the tag for each artifact), and write results to a file with `--file-output build.json` for later `deploy` or `render` steps.

## Checked

2026-11-04. Read the Skaffold Build overview page (builder-by-environment matrix), the CLI reference section for `skaffold build` and the `Artifact` definition in the v4beta14 config schema. Confirmed: builder list, support matrix, `context` default `.`, `image` required, `-b/--build-image` substring match, `--cache-artifacts` default true, `--cache-file` default, `--dry-run`, `--file-output`. Removed: the claim that the `image` name must match manifest references exactly (the pages only say tags are templated into manifests).
Method: documentation only; no commands were run.
