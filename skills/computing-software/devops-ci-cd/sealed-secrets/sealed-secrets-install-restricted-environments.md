---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-install-restricted-environments
name: sealed-secrets-install-restricted-environments
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, install, no-rbac, restricted-environment, helm, controller-norbac, crds]
level: advanced
status: docs-checked
description: "Deploy Sealed Secrets without cluster-wide RBAC, using controller-norbac.yaml or a Helm values file that reuses an allocated service account."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets install restricted environments

Two approaches exist when you cannot create ClusterRoles or other cluster-scoped objects.

No-RBAC manifest: use `controller-norbac.yaml` from the releases page. It contains only the Deployment, Service and CustomResourceDefinition, and deliberately omits the ServiceAccount, ClusterRole and ClusterRoleBinding. Requirements: a cluster administrator has already installed the SealedSecret CRDs, and you have an allocated service account to run the Deployment.

Helm in a single allocated namespace: the most restrictive scenario in the README is a namespace with a service account, no access to cluster CRDs, no ability to create further service accounts or roles, and mandatory resource limits. The one prerequisite is that the CRDs are already installed. Prepare a values file:

```yaml
serviceAccount:
  create: false
  name: {allocated-service-account}
rbac:
  create: false
  clusterRole: false
resources:
  limits:
    cpu: 150m
    memory: 256Mi
```

Then install, skipping the CRDs:

```bash
helm install sealed-secrets -n {allocated-namespace} sealed-secrets/sealed-secrets --skip-crds -f config.yaml
```

The limits are sample values that should work; review them for your setup.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Installation in Restricted Environments, Helm Chart on a restricted environment.
Confirmed: `controller-norbac.yaml` contents and requirements, restrictive scenario, values file, `--skip-crds` install command.
Removed: the closing claim about managing Secrets only where roles exist and the flag advice (not in the README).
Method: documentation only; no commands were run.
