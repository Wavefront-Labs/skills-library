---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-install-controller-manifest-and-helm
name: sealed-secrets-install-controller-manifest-and-helm
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, install, helm, kustomize, controller-manifest, fullnameoverride, kubeseal]
level: practitioner
status: docs-checked
description: "Install the Sealed Secrets controller from the release manifest, kustomize or the Helm chart, and fix the controller name mismatch with kubeseal."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets install controller manifest and helm

The official installation mechanism is a single YAML manifest per release (see the project's GitHub releases page). Applying it creates the `SealedSecret` CRD, installs the controller into the `kube-system` namespace, and creates a service account and the RBAC it needs. After a few moments the controller generates a key pair and is ready; if not, check its logs.

For custom namespaces or environment variables, layer your changes with kustomize, which `kubectl` supports natively.

Helm chart:

```bash
helm repo add sealed-secrets https://bitnami.github.io/sealed-secrets
```

Chart versioning differs from the project: controller versions are 0.X.Y, chart versions are 1.X.Y-rZ, so there can be several chart revisions for one controller release.

Name mismatch trap: the chart installs the controller as `sealed-secrets`, while `kubeseal` looks for `sealed-secrets-controller` in `kube-system`. Either pass `--controller-name sealed-secrets` on every call, or install with the override:

```bash
helm install sealed-secrets -n kube-system \
  --set-string fullnameOverride=sealed-secrets-controller \
  sealed-secrets/sealed-secrets
```

If the controller lives in another namespace, give kubeseal `--controller-namespace` or set `SEALED_SECRETS_CONTROLLER_NAMESPACE`.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Controller, Kustomize, Helm Chart, FAQ on controller namespace.
Confirmed: kube-system install, kustomize note, `helm repo add` URL, 0.X.Y vs 1.X.Y-rZ versioning, name mismatch and both fixes, `fullnameOverride` command.
Removed: nothing.
Method: documentation only; no commands were run.
