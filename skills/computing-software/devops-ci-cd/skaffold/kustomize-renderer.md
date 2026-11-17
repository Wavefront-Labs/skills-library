---
id: computing-software.devops-ci-cd.skaffold.kustomize-renderer
name: kustomize-renderer
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [kustomize, manifests, overlays, render]
level: practitioner
status: docs-checked
description: "Render manifests through kustomize with manifests.kustomize.paths and buildArgs, and select overlays per profile."
sources:
  - "https://skaffold.dev/docs/renderers/kustomize/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold works with kustomize by calling its command-line interface. Use it as the renderer with `manifests.kustomize`:

```yaml
manifests:
  kustomize:
    paths:
    - overlays/dev
    buildArgs: ["--enable-helm"]
deploy:
  kubectl: {}
profiles:
- name: prod
  patches:
  - op: replace
    path: /manifests/kustomize/paths/0
    value: overlays/prod
```

- `paths`: list of folders containing a kustomization file (the page says `kustomize.yaml`). Schema default is `["."]`.
- `buildArgs`: additional arguments passed to `kustomize build`.
- The `kustomize` CLI must be installed; Skaffold does not install it.

A common layout is `base/` plus one overlay per environment, with a profile that swaps the path (the layout and the profile patch are illustrative, not from the page). Select a profile with `-p`, for example `skaffold dev -p prod`.

## Checked

2026-11-04. Read the whole Skaffold Kustomize renderer page and the `Kustomize` definition in the v4beta14 schema. Confirmed `paths`, its default, `buildArgs` and the install note. Removed: the claims that Skaffold substitutes image names so the kustomization must use the artifact name, that `skaffold init` generates kustomize config, that `skaffold render` output shows built images, and the advice about images transformers (none on the page). The earlier profile example nested a full `manifests` block directly in the profile; the replacement uses a patch, which is the documented profile mechanism.
Method: documentation only; no commands were run.
