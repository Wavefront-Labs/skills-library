---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-aws-auth-methods
name: external-secrets-operator-aws-auth-methods
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [aws, authentication, irsa, accesskey]
level: practitioner
status: docs-checked
description: "Authenticate an ESO AWS SecretStore with the controller pod identity, static access keys or EKS service account (jwt) credentials."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/aws-access.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `service` to `SecretsManager`, `ParameterStore` or `CertificateManager`.

1. Controller's pod identity: zero configuration, inherits the AWS SDK default credential chain. Attach a role to the controller pod with IRSA, kiam or kube2iam. When no other method is set, this is used.
2. Access key and secret: `auth.secretRef.accessKeyIDSecretRef` and `secretAccessKeySecretRef` point to a Kubernetes Secret; add `sessionTokenSecretRef` for temporary STS credentials.
3. EKS service account: annotate a ServiceAccount with `eks.amazonaws.com/role-arn` and reference it with `auth.jwt.serviceAccountRef.name`. Short-lived tokens, and ESO itself runs without credentials. Needs service account volume projection (default on EKS).

```yaml
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-central-1
      auth:
        jwt:
          serviceAccountRef:
            name: my-serviceaccount
```

In a ClusterSecretStore, every Secret or ServiceAccount reference must include a `namespace`.

## Checked

2026-11-03. Claims were read against provider/aws-access.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
