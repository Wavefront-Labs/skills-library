---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-vault-auth-methods
name: external-secrets-operator-vault-auth-methods
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [vault, authentication, approle, kubernetes-auth]
level: advanced
status: docs-checked
description: "Choose among the Vault authentication methods ESO supports and set the Kubernetes auth audience required by Vault 1.21."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/hashicorp-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported methods: token (`tokenSecretRef`), AppRole, Kubernetes, LDAP, UserPass, JWT/OIDC, AWS IAM and TLS certificates. In a ClusterSecretStore all secret references need a `namespace`.

Kubernetes auth: credentials come from a ServiceAccount token ESO requests (`serviceAccountRef`), or a token in a Secret. Vault validates it with TokenReview, so bind `system:auth-delegator` to that service account. Vault 1.20 warns about roles without an audience and 1.21 and later fail, so set it:

```yaml
auth:
  kubernetes:
    mountPath: kubernetes/my-cluster
    role: my-role
    serviceAccountRef:
      name: my-service-account
      audiences:
        - vault
```

TLS certificate auth: a `kubernetes.io/tls` Secret with `tls.crt` and `tls.key`, referenced from the store (ClusterSecretStore needs `namespace` on both `clientCert` and `secretRef`). If the Vault server enforces mutual TLS with `tls_require_and_verify_client_cert = true`, that applies to all APIs.

AWS IAM auth reuses the AWS options: access keys, EKS service account, or the controller's IRSA or Pod Identity (auto-detected). With Vault namespaces you may authenticate in one namespace and use the token in another.

## Checked

2026-11-03. Claims were read against provider/hashicorp-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
