---
id: computing-software.devops-ci-cd.skaffold.custom-builder
name: custom-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [custom, buildcommand, environment, image]
level: advanced
status: docs-checked
description: "Write your own build step with the custom builder: required command, injected variables, and what the script must do."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/custom/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `custom` builder runs a script of your choice (beta in the schema). It works with the local and in-cluster build environments; Google Cloud Build is not supported. Add `local` (or `cluster`) to the `build` section as well as `custom` on the artifact.

```yaml
build:
  local: {}
  artifacts:
  - image: my-registry/app
    custom:
      buildCommand: ./build.sh
      dependencies:
        paths: ["src/**", "build.sh"]
```

`buildCommand` is required and supports Go templates, for example `./build.sh --flag={{ .SOME_FLAG }}` takes `SOME_FLAG` from the environment.

Skaffold passes these environment variables to the script, in addition to the local environment:

- `IMAGE`: the fully qualified image name, for example `gcr.io/image1:tag`.
- `PUSH_IMAGE`: `true` if the image must exist in a remote registry, `false` if it should exist locally.
- `BUILD_CONTEXT`: absolute path to the artifact `context` directory.
- `PLATFORMS`: comma-separated platforms, for example `linux/arm64,linux/amd64`. For one platform build for it; for several, build a multi-arch image.
- `SKIP_TEST`: whether to skip tests after building.

Local builds also get the Docker daemon environment variables (so tools work with Minikube). In-cluster builds also get `KUBECONTEXT`, `NAMESPACE`, `PULL_SECRET_NAME`, `DOCKER_CONFIG_SECRET_NAME` and `TIMEOUT`.

Rules for the script:

1. Build the image and tag it as `$IMAGE`.
2. If `PUSH_IMAGE=true`, push it.
3. Skaffold then obtains the digest from the remote registry (if `PUSH_IMAGE=true`) or the local daemon, and errors out if it cannot.

Artifacts listed in `requires` are exposed to the script as environment variables named after the `alias`. The script's STDOUT and STDERR appear in the Skaffold logs.

Set `dependencies` so the file watcher knows which files trigger a rebuild. The schema says either `dockerfile` or `paths` should be specified for file watching to work; `ignore` works only with `paths`, and `command` can instead print dependencies as a JSON array. Files you want synced must be in both `dependencies.paths` and `sync`.

Use this builder for tools Skaffold has no native support for.

## Checked

2026-11-04. Read the Skaffold Custom Build Script page and the `CustomArtifact` and `CustomDependencies` definitions in the v4beta14 schema. Confirmed the variable contract, `buildCommand` required and templated, digest lookup, `requires` aliases, dependency kinds and sync rule, and the Cloud Build limitation. Rewrote the "changes are not detected without dependencies" sentence to match the schema wording.
Method: documentation only; no commands were run.
