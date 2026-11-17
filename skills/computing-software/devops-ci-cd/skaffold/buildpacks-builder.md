---
id: computing-software.devops-ci-cd.skaffold.buildpacks-builder
name: buildpacks-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [buildpacks, builder, runimage, project-toml]
level: practitioner
status: docs-checked
description: "Build images with Cloud Native Buildpacks, choosing a builder image, passing env vars and using auto file sync."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/buildpacks/"
  - "https://skaffold.dev/docs/filesync/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `buildpacks` builder builds an image from source without a Dockerfile. Skaffold needs only a local Docker daemon and runs the build in a container using the configured `builder`. On success the built image is pushed to the remote registry unless you skip that. The builder is marked alpha in the config schema.

```yaml
build:
  artifacts:
  - image: my-registry/app
    buildpacks:
      builder: gcr.io/buildpacks/builder:v1
      runImage: gcr.io/buildpacks/run:v1
      env:
      - MY_SETTING=value
      trustBuilder: true
      clearCache: false
```

Options: `builder` (required), `runImage` (overrides the stack's default run image), `env`, `buildpacks` (explicit buildpack list; order matters and builder auto-detection is then ignored), `trustBuilder`, `clearCache`, `projectDescriptor` (default `project.toml`), `dependencies`, `volumes` and `buildArgs` (extra args to `pack build`).

Gotchas from the docs:

- The field is `buildpacks`; it was renamed from `buildpack` in Skaffold 1.11 (schema `v2beta5`). The page's own `dependencies` snippet still shows the old singular spelling, so use `buildpacks`.
- Your current shell environment is not passed to the build; set variables explicitly under `env` (values can use Go template syntax).
- `requires` lets you use another artifact image as the `builder` or `runImage`.
- By default every file in the artifact `context` is watched; `dependencies.paths` and `dependencies.ignore` narrow that, and `ignore` works only together with `paths`.
- File sync `auto` mode is on by default for Buildpacks artifacts. Turn it off with `sync: auto: false`.

The GCP builder (`gcr.io/buildpacks/builder:v1`) supports auto sync for Go (`*.go`), Java (`*.java`, `*.kt`, `*.scala`, `*.groovy`, `*.clj`) and NodeJS (`*.js`, `*.mjs`, `*.coffee`, `*.litcoffee`, `*.json`) sources. Other file types trigger an image rebuild. Skaffold sets `GOOGLE_DEVMODE=1` when running `skaffold dev` with auto sync.

If a build is slow, check whether `clearCache` is set; it removes the cache volume for the image, so leave it false for the inner dev loop.

Practical advice: pin the builder image to a version tag and keep variables in the `env` list so the build is the same on every machine and in CI.

## Checked

2026-11-04. Read the Skaffold Buildpacks builder page, the File Sync page (auto mode, supported file types, `sync.auto`) and the `BuildpackArtifact` definition in the v4beta14 schema. Confirmed all options and the `project.toml` default, the env pass-through note, the rename note, `requires`, dependencies/ignore behaviour. Removed: the "only linux/amd64 is supported" claim (not on either page), advice on `trustBuilder` being only for builders you control (not in the docs), and the example `GOOGLE_RUNTIME_VERSION` variable. Conflict: the page text says `buildpacks` while its own dependencies example uses `buildpack`.
Method: documentation only; no commands were run.
