---
id: computing-software.devops-ci-cd.argocd-image-updater.image-platforms-and-multi-arch
name: image-platforms-and-multi-arch
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, platforms, multi-arch, manifest-list, linux-arm64, mixed-architecture, test-command]
level: practitioner
status: docs-checked
description: "Set allowed platforms for multi-arch clusters: the default is the updater's own platform, platforms only works with newest-build and digest, and the test command has --platforms."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/testing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Platforms and multi-arch images

Image Updater can inspect manifest lists (multi-arch images). By default it only considers images that have a manifest for the platform it runs on. On clusters with several node architectures, or when the updater runs on `linux/amd64` but the workload targets `linux/arm64`, declare the platforms:

```yaml
images:
  - alias: "myalias"
    imageName: "some/image"
    commonUpdateSettings:
      platforms: ["linux/arm64", "linux/amd64"]
```

Kubernetes picks the right image at runtime. `platforms` can be set globally, per application or per image. In the migration, `platforms: linux/amd64,linux/arm64` (comma string) becomes an array.

Limit: only strategies that fetch image metadata honour it. The docs name them `latest` (now `newest-build`) and `digest`; `semver` and `name` (now `alphabetical`) ignore it.

The `test` command takes the platform of the machine it runs on, so on a Mac you will often get no results. Pass `--platforms`:

```
argocd-image-updater test quay.io/argoprojlabs/argocd-e2e-container --platforms darwin/amd64 --update-strategy newest-build --loglevel debug
```

shows `Found 0 tags` because the manifest list has no usable reference; with `--platforms linux/amd64` it finds 3 tags and selects `0.3`.

## Checked

2026-11-04. Confirmed against images.md (Image platforms, platforms field), update.md (multi-arch section), testing.md (the darwin/amd64 versus linux/amd64 test output) and migration.md (comma string becomes an array). The old strategy names are kept as the pages use them.

Method: documentation only; no commands were run.
