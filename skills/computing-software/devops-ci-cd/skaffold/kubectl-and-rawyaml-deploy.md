---
id: computing-software.devops-ci-cd.skaffold.kubectl-and-rawyaml-deploy
name: kubectl-and-rawyaml-deploy
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [kubectl, rawyaml, deploy, manifests]
level: intro
status: docs-checked
description: "Deploy plain Kubernetes YAML with the kubectl deployer and the rawYaml renderer, including flags and default paths."
sources:
  - "https://skaffold.dev/docs/deployers/kubectl/"
  - "https://skaffold.dev/docs/renderers/rawyaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Plain manifests use `manifests.rawYaml` as the renderer and `deploy.kubectl` as the deployer. The `rawYaml` renderer is for projects with no render engine (helm, kustomize, kpt): Skaffold only does its own field replacement (`image:` and `labels:` modifications).

```yaml
manifests:
  rawYaml:
  - k8s/*.yaml
deploy:
  kubectl:
    flags:
      global: ["--v=1"]
      apply: ["--server-side"]
      delete: ["--ignore-not-found"]
      disableValidation: false
    defaultNamespace: dev
```

- `rawYaml` is enabled by default with the default path `['k8s/*.yaml']`. It takes a list of paths, and glob syntax is supported.
- The kubectl deployer uses client-side `kubectl apply` and is marked beta in the schema. The `kubectl` CLI must be installed, in a version compatible with your cluster; Skaffold does not install it.
- `kubectl.flags` has `global` (every command), `apply`, `delete` and `disableValidation` (adds `--validate=false` to supported commands, default false).
- `defaultNamespace` is the namespace passed to kubectl when no other override is given.
- `remoteManifests` lists Kubernetes manifests in remote clusters.
- `hooks` run lifecycle commands before and after every deploy.

If validation fails because a custom resource definition is not yet installed, one option is `disableValidation`; leaving it on permanently is a trade-off (this advice is not from the pages).

## Checked

2026-11-04. Read the Skaffold Kubectl deployer page, the Raw YAML renderer page and the `KubectlDeploy`, `KubectlFlags` and `RenderConfig` definitions in the v4beta14 schema. Confirmed paths, default, flags and their meanings, `defaultNamespace`, `remoteManifests`, `hooks` and the kubectl install note. Removed: the claim that a missing `deploy` section defaults to kubectl, that `defaultNamespace` supports templating, that the manifest `image` must match the artifact name, and the advice to review with `skaffold render` (none on these pages).
Method: documentation only; no commands were run.
