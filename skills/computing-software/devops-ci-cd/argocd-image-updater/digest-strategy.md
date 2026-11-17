---
id: computing-software.devops-ci-cd.argocd-image-updater.digest-strategy
name: digest-strategy
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, digest, mutable-tags, sha256, latest-tag, update-strategy, environment-tags]
level: practitioner
status: docs-checked
description: "Track a mutable tag such as latest, dev or prod with the digest strategy: put the tag in imageName, and updates happen when the registry digest changes."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/examples/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# digest strategy

Use when you follow one mutable tag, such as `latest`, or when CI publishes tags named for environments (`dev`, `stage`, `prod`). The tag to watch goes in `imageName` as the constraint:

```yaml
images:
  - alias: "myimage"
    imageName: "some/image:latest"
    commonUpdateSettings:
      updateStrategy: "digest"
```

An update happens when either:

- the running image is not specified by digest (for example it uses a tag), or
- the current digest differs from the registry's digest for that tag

The updater then writes the `sha256` digest into your configuration, and Kubernetes restarts the pods onto the new image. Example from the docs: a Deployment starts with `image: registry.com/vendor/api@sha256:38089...` and the CR sets `updateStrategy: "digest"` globally with `imageName: "registry.com/vendor/api:latest"`.

Multi-arch: digest fetches metadata, so `platforms` applies to it. In commit message templates `.OldTag` and `.NewTag` hold the tag name or SHA digest before and after the update.

The tag to inspect must be given in `imageName` as the version constraint, so always give the tag name.

## Checked

2026-11-04. Confirmed against update-strategies.md (digest section, mutable versus immutable tags), images.md (tracking an image's latest tag, platforms note), the examples page (digest example with an initial sha256 in the Deployment) and update-methods.md (.OldTag and .NewTag in the commit message template).

Method: documentation only; no commands were run.
