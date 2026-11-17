---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-gcp-secretmanager-auth
name: external-secrets-operator-gcp-secretmanager-auth
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [gcp-secret-manager, authentication, workload-identity, projectid]
level: practitioner
status: docs-checked
description: "Pick a GCP Secret Manager authentication mechanism for ESO and avoid the projectID versus clusterProjectID mix-up."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/google-secrets-manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three mechanisms:
- `auth.workloadIdentity`: GKE Workload Identity, the usual choice on GKE. Patterns: a Kubernetes ServiceAccount used directly as a GCP IAM principal, a ServiceAccount linked to a GCP service account, or authorising the core controller pod's own service account so stores need no auth.
- `auth.workloadIdentityFederation`: AKS, EKS, self-hosted or OpenShift via an IAM workload identity pool.
- `auth.secretRef`: a static service account JSON key; not recommended where the other two are available.

`spec.provider.gcpsm.projectID` is the project that holds the secrets (used in `projects/{projectID}/secrets/{name}`). `clusterProjectID` (under `workloadIdentity`) identifies the project hosting the GKE cluster and is used only to build the identity pool URL. For cross-project access set both:

```yaml
gcpsm:
  projectID: "secrets-project-456"
  auth:
    workloadIdentity:
      clusterProjectID: "cluster-project-123"
      serviceAccountRef:
        name: demo-sa
```

## Checked

2026-11-03. Claims were read against provider/google-secrets-manager.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
