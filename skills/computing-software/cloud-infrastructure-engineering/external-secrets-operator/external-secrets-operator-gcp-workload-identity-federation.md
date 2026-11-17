---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-gcp-workload-identity-federation
name: external-secrets-operator-gcp-workload-identity-federation
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [gcp-secret-manager, workload-identity-federation, audience, sts]
level: sme
status: docs-checked
description: "Configure ESO with GCP Workload Identity Federation using serviceAccountRef, credConfig or awsSecurityCredentials and grant the federated principal access."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/google-secrets-manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Under `auth.workloadIdentityFederation` set exactly one of:
- `serviceAccountRef`: ESO requests a bound Kubernetes token (via TokenRequest) for that ServiceAccount with the audience and exchanges it at Google STS. Requires `audience`.
- `credConfig`: an `external_account` JSON loaded from a ConfigMap key; the audience may come from it or be overridden.
- `awsSecurityCredentials`: static AWS credentials in a Secret plus `region`. Requires `audience`.

`audience` is the full workload identity provider resource name (`//iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/...`). Set `projectID` explicitly when not on GKE nodes. For a ClusterSecretStore set `serviceAccountRef.namespace`.

Grant the federated principal access:

```shell
gcloud secrets add-iam-policy-binding "${SECRET_NAME}" --project="${PROJECT_ID}" \
  --role="roles/secretmanager.secretAccessor" \
  --member="principal://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL_NAME}/subject/system:serviceaccount:${K8S_NAMESPACE}:${K8S_SA}"
```

A `PermissionDenied` on `secretmanager.versions.access` while the store is `Ready` means the IAM binding is on the wrong identity.

## Checked

2026-11-03. Claims were read against provider/google-secrets-manager.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
