---
id: computing-software.cloud-infrastructure-engineering.cert-manager.vault-issuer
name: vault-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [vault, approle, kubernetes-auth, jwt, serviceaccountref, mtls, pki]
level: advanced
status: docs-checked
description: "Configure a cert-manager Vault issuer: signing path, caBundle, AppRole, token, Kubernetes or JWT auth, required RBAC and mTLS to Vault."
sources:
  - https://cert-manager.io/docs/configuration/vault/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Common fields: `spec.vault.server` (URL), `spec.vault.path` (must be a `sign` endpoint such as `pki_int/sign/example-dot-com`), `spec.vault.caBundle` (base64 PEM, usually needed for https) or `caBundleSecretRef`. Exactly one auth method goes under `spec.vault.auth`; without one the config does not work.

- AppRole: `appRole.path`, `roleId`, `secretRef` (name/key of the `secretId`), in the Issuer's namespace, or the cluster resource namespace for a ClusterIssuer.
- Token: `tokenSecretRef`. cert-manager does not refresh tokens; an external process must.
- Kubernetes/JWT (v1.12.0+): `kubernetes.role`, `kubernetes.mountPath` (e.g. `/v1/auth/kubernetes-cluster001`), `kubernetes.serviceAccountRef.name`. `serviceAccountRef.audiences` needs v1.15.0+. Use JWT/OIDC when Vault is outside the cluster and can reach the OIDC endpoint; use Kubernetes auth when Vault is in-cluster or only the API is reachable.

RBAC: a Role allowing `create` on `serviceaccounts/token` for the named ServiceAccount, bound to the `cert-manager` ServiceAccount in `cert-manager`.

Vault side, JWT: `role_type=jwt`, `user_claim=sub`, `bound_audiences=vault://<namespace>/<issuer-name>` (ClusterIssuer: `vault://<cluster-issuer-name>`), `bound_subject=system:serviceaccount:<ns>:<sa>`, `ttl=1m`.

mTLS: Vault listener `tls_require_and_verify_client_cert = true`; Secret holds `client.crt`, `client.key`, `server_ca.crt`, referenced by `clientCertSecretRef` and `clientKeySecretRef`.

Readiness uses `v1/sys/health`, so Vault must be initialised and unsealed. Healthy: `READY True`, `STATUS Vault verified`.

## Checked

2026-11-03. Confirmed on the cert-manager Vault issuer page (configuration/vault): common fields, sign endpoint, AppRole, token, Kubernetes and JWT auth, v1.12.0 and v1.15.0 gates, RBAC, JWT role values, mTLS listener setting and Secret keys, v1/sys/health readiness and the verified status output. Nothing removed.
Method: documentation only; no commands were run.
