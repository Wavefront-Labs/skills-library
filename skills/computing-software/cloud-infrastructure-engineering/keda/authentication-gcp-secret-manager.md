---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-gcp-secret-manager
name: authentication-gcp-secret-manager
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [gcp-secret-manager, gcpsecretmanager, gcp-pod-identity, service-account-credentials]
level: advanced
status: docs-checked
description: "Fetch scaler credentials from GCP Secret Manager with a service account key stored in a Kubernetes Secret or the gcp pod identity provider."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `gcpSecretManager` key lets a TriggerAuthentication pull secrets from Google Cloud Secret Manager. The `secrets` list is required and maps each Secret Manager secret (`id`, with optional `version`) to a trigger `parameter`.

Two ways to authenticate to Secret Manager:
- GCP IAM service account credentials, supplied through a Kubernetes secret:
  `credentials.clientSecret.valueFrom.secretKeyRef` with `name` and `key` (both required);
- the `gcp` pod identity provider, configured inside the block as `podIdentity.provider: gcp`.

```yaml
gcpSecretManager:
  secrets:
    - parameter: {param-name-used-for-auth}
      id: {secret-manager-secret-name}
      version: {secret-manager-secret-name}
  podIdentity:
    provider: gcp
  credentials:
    clientSecret:
      valueFrom:
        secretKeyRef:
          name: {k8s-secret-with-gcp-iam-sa-secret}
          key: {key-within-the-secret}
```

Note the specification comments label `podIdentity` and `credentials` both as optional, with `provider` required inside `podIdentity` and `clientSecret` required inside `credentials`. The page presents the two routes as alternatives. The `version` field is optional, but the page's sample describes it with the same placeholder as `id`, so check the Secret Manager version identifier you intend to pin.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: gcpSecretManager secrets, podIdentity.provider gcp, credentials.clientSecret. Removed: advice to choose exactly one route.

Method: documentation only; no commands were run.
