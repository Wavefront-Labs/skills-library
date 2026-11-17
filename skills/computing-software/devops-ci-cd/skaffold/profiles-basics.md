---
id: computing-software.devops-ci-cd.skaffold.profiles-basics
name: profiles-basics
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [profiles, patches, activation, environments]
level: practitioner
status: docs-checked
description: "Override parts of skaffold.yaml per environment with profiles that carry build, test, deploy or JSON patches."
sources:
  - "https://skaffold.dev/docs/environment/profiles/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Profiles define build, test and deployment configurations for different contexts, typically environments such as production or development. Once active, a profile's `build`, `test` and `deploy` content is laid onto, but does not completely replace, the main sections. The profile syntax is the same as the main sections and the defaults are the same.

```yaml
profiles:
- name: gcb
  build:
    googleCloudBuild: {}
- name: dev
  patches:
  - op: replace
    path: /build/artifacts/0/docker/dockerfile
    value: Dockerfile.dev
```

The profiles page lists six parts: `name`, `build`, `test`, `deploy`, `patches` and `activation`. The schema also allows `manifests`, `portForward`, `customActions`, `resourceSelector`, `verify` and `requiresAllActivations`.

- Override via replacement: with no profile active, the main config applies. With `skaffold dev -p gcb` Skaffold switches to Google Cloud Build for building; since that profile has no deploy configuration, it continues to use kubectl.
- Override via patches: a more verbose, fine-grained way to override individual values, based on JSON Patch. The page's example gives the first artifact a different Dockerfile.
- Activate with `-p` / `--profile`, which the page documents for `skaffold dev` and `skaffold run`, or with `activation` entries (see the activation skill).
- Multiple profiles: repeat `-p` or comma-separate, as in `skaffold dev -p hello,world`. This is useful with patches for a composable setup.
- Deactivate with a `-` prefix: `skaffold dev -p hello,-world`.

## Checked

2026-11-04. Read the whole Skaffold Profiles page and the `Profile` definition in the v4beta14 schema. Confirmed layering, parts, replacement and patch behaviour, multiple profiles and deactivation. Removed: the `skaffold diagnose --yaml-only -p prod` tip and the advice about when to use modules instead (not on the page). Changed the example: the earlier example's patch plus googleCloudBuild in one profile is replaced with two profiles that follow the page's examples.
Method: documentation only; no commands were run.
