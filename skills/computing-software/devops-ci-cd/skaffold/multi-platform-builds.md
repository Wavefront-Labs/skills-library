---
id: computing-software.devops-ci-cd.skaffold.multi-platform-builds
name: multi-platform-builds
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [platforms, multi-arch, arm64, amd64]
level: advanced
status: docs-checked
description: "Build for several CPU architectures with build.platforms, per-artifact platforms or the --platform flag."
sources:
  - "https://skaffold.dev/docs/builders/cross-platform/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold selectively supports cross-platform builds (a different architecture from the dev machine) and multi-platform builds (several architectures). Target platforms can be set three ways, in increasing precedence:

```yaml
build:
  platforms: ["linux/amd64", "linux/arm64"]   # pipeline level
  artifacts:
  - image: app
    platforms: ["linux/arm64"]                # overrides the pipeline value
```

```bash
skaffold build --platform=linux/arm64,linux/amd64   # overrides both
```

For `dev`, `debug` and `run`, where output is deployed immediately, Skaffold checks the platform of the cluster nodes and attempts to build for that target platform.

The final platform list must be supported by the builder, or the build fails. Support by builder (local / in-cluster / Google Cloud Build):

- Dockerfile: cross and multi / cross only, and the platform should match the node running the pod / cross and multi.
- Jib: cross and multi / not supported / cross and multi.
- Cloud Native Buildpacks: only `linux/amd64` locally and on Cloud Build.
- Bazel: cross-platform locally only.
- ko: cross and multi locally and on Cloud Build.
- Custom script: cross and multi locally and in-cluster, but you implement it in the script.

Skaffold builds multi-platform images natively for the jib, ko and custom builders. For other builders that can cross-build, it builds one single-platform image per architecture, stitches them into a multi-platform image and pushes it to the registry.

The `--disable-multi-platform-build` flag forces single-platform builds even when several platforms are specified. Per the CLI reference it defaults to false for `build` and is enabled by default for `dev` and `debug` to keep the dev loop fast.

## Checked

2026-11-04. Read the whole Cross/multi-platform page and the `--disable-multi-platform-build` entries in the CLI reference for build, dev and debug. Confirmed precedence, the cluster-node behaviour, the support table and the stitching note. Removed: the claim that `skaffold build --platform` in CI is the typical workflow, that multi-platform images cannot load into a single-arch daemon, and the advice to set platforms per artifact after a failure (none on the page). The page does not mention the `--disable-multi-platform-build` flag.
Method: documentation only; no commands were run.
