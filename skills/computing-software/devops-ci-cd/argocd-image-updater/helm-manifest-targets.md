---
id: computing-software.devops-ci-cd.argocd-image-updater.helm-manifest-targets
name: helm-manifest-targets
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, helm, manifest-targets, helm-parameters, image-name-tag, yaml-list-index, helm-spec]
level: practitioner
status: docs-checked
description: "Tell Argo CD Image Updater which Helm parameters to set with manifestTargets.helm: name and tag, a combined spec, the image.name and image.tag defaults, and list indexes."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/migration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Helm manifest targets

For Helm apps with several images, or with parameters other than `image.name` and `image.tag`, set `manifestTargets.helm`:

```yaml
images:
  - alias: "dex"
    imageName: "quay.io/dexidp/dex:latest"
    manifestTargets:
      helm:
        name: "dex.image.name"
        tag: "dex.image.tag"
```

Rules:

- omit `helm` entirely and the defaults `image.name` and `image.tag` are used
- if you set only one of `name` or `tag`, only that one is written; the other is not defaulted (a defaulted name would be shared and make images overwrite each other)
- `spec` is for charts that take the canonical `name:tag` in one parameter; if set, `name` and `tag` are ignored
- index lists with square brackets: `images[0].name`, `images[0].tag`, or `spec: "foo[1].image"`

Two images in one chart:

```yaml
- alias: "fooalias"
  imageName: "foo/bar"
  manifestTargets: {helm: {name: "foo.image", tag: "foo.tag"}}
- alias: "baralias"
  imageName: "bar/foo"
  manifestTargets: {helm: {name: "bar.image", tag: "bar.tag"}}
```

`manifestTargets.helm` is mutually exclusive with `kustomize` and `plugin`. It replaces the old annotations `<alias>.helm.image-name` and `<alias>.helm.image-tag`. With git write-back, pair it with `writeBackTarget: "helmvalues:<file>"` (a plugin app can also use `helm` this way).

## Checked

2026-11-04. Confirmed against images.md (Specifying Helm parameter names: defaults, only-one-set behaviour, spec, list indexes, the two-image example, mutual exclusivity table) and migration.md (old helm.image-name and image-tag annotations).

Method: documentation only; no commands were run.
