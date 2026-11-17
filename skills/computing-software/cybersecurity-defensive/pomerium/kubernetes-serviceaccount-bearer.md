---
id: computing-software.cybersecurity-defensive.pomerium.kubernetes-serviceaccount-bearer
name: kubernetes-serviceaccount-bearer
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [serviceaccount-token, projected-token, audience-binding, certificate-authority-file, pod-access]
level: advanced
status: docs-checked
description: "Let Kubernetes pods call a Pomerium route with an audience-scoped projected ServiceAccount token trusted via a jwt identity provider."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/bearer-token-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. **Trust the cluster.** Set global `certificate_authority_file` to the mounted CA `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`. Add an `identity_providers` entry with issuer `https://kubernetes.default.svc.cluster.local`, `jwks_url` `https://kubernetes.default.svc.cluster.local/openid/v1/jwks`, `supported_algs` `RS256` and an audience such as `pomerium.example.com`.
2. **Route.** `bearer_token_format: jwt`, `identity_providers` limited to `kubernetes`, and policy `claim/sub` equal to `system:serviceaccount:default:pom-tester`.
3. **Mint a scoped token.** In the pod set `serviceAccountName: pom-tester` and a `projected` volume with a `serviceAccountToken` source: `audience` `pomerium.example.com`, `expirationSeconds` 3600, `path` `token`, mounted read-only at `/var/run/secrets/pomerium`. Kubernetes keeps it refreshed.
4. **Call.** `Authorization: Bearer` plus the contents of `/var/run/secrets/pomerium/token`.

Caveats:
- Assumes Pomerium runs inside the cluster.
- `jwks_url` can be omitted if the issuer is reachable, so OIDC discovery finds keys; this may need the `system:service-account-issuer-discovery` ClusterRole.
- The global `certificate_authority_file` covers all JWKS and discovery fetches; there is no per-provider CA.
- The token `aud` must match the provider `audiences`; that binds a general cluster token to Pomerium.

Claims for policy: `sub`, `kubernetes.io.namespace`, `kubernetes.io.serviceaccount.name`.

## Checked

2026-11-04. Confirmed against the Bearer Token Access page: certificate_authority_file path, issuer, jwks_url, RS256, projected serviceAccountToken volume values, mount path, caveats and available claims. Nothing removed.

Method: documentation only; no commands were run.
