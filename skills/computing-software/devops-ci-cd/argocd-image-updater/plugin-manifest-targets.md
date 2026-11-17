---
id: computing-software.devops-ci-cd.argocd-image-updater.plugin-manifest-targets
name: plugin-manifest-targets
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, plugin, cmp, manifest-targets, plugin-env, helmfile, config-management-plugin]
level: advanced
status: docs-checked
description: "Update Config Management Plugin apps via manifestTargets.plugin env vars (name and tag or one spec), or via helm and kustomize targets with git."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Plugin (CMP) manifest targets

Approach 1: first-class plugin support. If the plugin reads images from environment variables in `spec.source.plugin.env`, name them:

```yaml
manifestTargets:
  plugin:
    name: "REDIS_IMAGE_NAME"
    tag: "REDIS_IMAGE_TAG"
```

or one variable for the full reference: `plugin: {spec: "REDIS_IMAGE"}` (then `name` and `tag` are ignored). Result for `name`/`tag`: env `REDIS_IMAGE_NAME=myregistry/redis`, `REDIS_IMAGE_TAG=7.0.0`; for `spec`: `REDIS_IMAGE=myregistry/redis:7.0.0`.

Works with both write-back methods:

- `argocd`: writes `spec.source.plugin.env` on the Application
- `git`: writes `.argocd-source-<appName>.yaml` (or `.argocd-source-<namespace>_<appName>.yaml` when the Application namespace differs from the controller's)

Each image can have its own variable names. `plugin` is mutually exclusive with `helm` and `kustomize`. Do not set `writeBackTarget` to `helmvalues` or `kustomization` with it.

Approach 2: the plugin (for example helmfile) reads values files from Git. Use `manifestTargets.helm` or `.kustomize` with the `git` method only (argocd cannot override Helm or Kustomize params on a plugin source), and a `writeBackTarget` of `kustomization` or `helmvalues:<path>`. Example: `manifestTargets.helm` with `name: "image.repository"` and `tag: "image.tag"`; the helmfile reads `kustomization.yaml` via `readFile "kustomization.yaml" | fromYaml`.

## Checked

2026-11-08. Read in full: docs/configuration/images.md and docs/configuration/applications.md. Read the first 170 lines of docs/basics/update-methods.md plus its plugin passages (the rest covers Git write-back details this skill does not cite). Confirmed both approaches, the env var results, the write-back file names, mutual exclusivity, the writeBackTarget incompatibility and the argocd-method limitation for approach 2. Nothing removed.

Method: documentation only; no commands were run.
