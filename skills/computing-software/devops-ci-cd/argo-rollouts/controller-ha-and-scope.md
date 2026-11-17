---
id: computing-software.devops-ci-cd.argo-rollouts.controller-ha-and-scope
name: controller-ha-and-scope
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [ha, leader-elect, controller, multi-cluster, version-skew, crd, argo-rollouts]
level: advanced
status: docs-checked
description: "Run the controller in HA mode and respect its single-cluster scope and version-skew rules."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
  - https://argo-rollouts.readthedocs.io/en/stable/best-practices/
  - https://argo-rollouts.readthedocs.io/en/stable/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**HA.** Yes, multiple controller replicas are supported. Start the controller with `--leader-elect` and increase the replica count in the controller Deployment. The implementation is based on the Kubernetes client-go `leaderelection` package and is tolerant to arbitrary clock skew among replicas; tune the tolerance with `--leader-election-lease-duration` and `--leader-election-renew-deadline`.

```yaml
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: argo-rollouts
          args: [--leader-elect]
```

**One controller per cluster that runs Rollouts.** You cannot install Argo Rollouts centrally and manage Rollouts in external clusters. The Rollout CRD is unknown to vanilla Kubernetes, so the CRD and the controller must exist in every cluster that deploys Rollout workloads, unlike Argo CD which can manage remote clusters.

**Version skew.** The CLI and kubectl plugin only patch the Rollout object or read fields from it, because there is no separate Argo Rollouts API. Old plugin versions may not understand fields added to the Rollout specification later, so keep the plugin reasonably current.

**API version.** The Rollout CRD is `v1alpha1`. The docs say the alpha label does not carry the meaning Kubernetes gives it and does not imply the project is not production ready.

**Namespaced installs.** `namespace-install.yaml` needs only namespace-level privileges and suits running several controller instances in different namespaces on one cluster. It does not include the CRDs, which must be installed separately from the `manifests/crds` directory.

**Scope.** Rollouts work with a single application and a single cluster; the docs advise against using Argo Rollouts for infrastructure applications such as cert-manager, nginx, coredns or sealed-secrets.

Verify: the controller Deployment runs the replica count you set with `--leader-elect` in its args.

## Checked

2026-11-08. Confirmed against the Argo Rollouts FAQ and best-practices pages (both read in full) and the installation page (read in full) for the namespaced install: leader-elect HA, one controller per cluster, plugin version skew, v1alpha1 stability, scope guidance.

Removed or corrected: removed the claims that only the leader acts and that replicas download plugins at startup, and the kubectl get lease verify command (not documented).

Method: documentation only; no commands were run.
