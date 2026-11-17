---
id: computing-software.devops-ci-cd.flux.kustomization-remote-clusters
name: kustomization-remote-clusters
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, kubeconfig, remote-cluster, configmapref, hub-spoke]
level: advanced
status: docs-checked
description: "Apply a Kustomization to a remote cluster with spec.kubeConfig using a kubeconfig Secret or a workload-identity ConfigMap."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.kubeConfig` lets a Kustomization apply, health check, prune and delete on a remote cluster, for hub-and-spoke setups. Two authentication options:

- `.spec.kubeConfig.secretRef`: a static kubeconfig in a Secret in the Kustomization namespace. The kubeconfig is loaded on each reconcile from key `value` or `value.yaml` (or the `key` you set), so you can rotate expiring tokens by updating the Secret.
- `.spec.kubeConfig.configMapRef` (recommended): secret-less. A kubeconfig is built dynamically from parameters in a ConfigMap, using workload identity (`data.provider` such as aws, azure or gcp).

```yaml
spec:
  interval: 10m
  path: ./apps
  prune: true
  sourceRef:
    kind: GitRepository
    name: apps
  kubeConfig:
    secretRef:
      name: prod-cluster-kubeconfig
```

If you also set `.spec.serviceAccountName`, the controller impersonates that ServiceAccount on the target cluster. It must exist in a namespace with the same name as the Kustomization namespace there, so that namespace has to exist on both clusters.

React instantly to changes in the referenced Secret or ConfigMap by labelling it `reconcile.fluxcd.io/watch: Enabled`.

Security: kubeconfigs with exec plugins are blocked unless the controller flag `--insecure-kubeconfig-exec` is enabled, and the security best practices say to leave that off, as well as `--insecure-kubeconfig-tls`. Prefer configMapRef with workload identity over long-lived tokens.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/) and the Flux security best practices page (fluxcd.io/flux/security/best-practices/): `kubeConfig.secretRef` and `configMapRef` (recommended), key lookup, impersonation namespace rule, and the `--insecure-kubeconfig-exec` and `--insecure-kubeconfig-tls` guidance. Nothing removed.

Method: documentation only; no commands were run.
