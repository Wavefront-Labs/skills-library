---
id: computing-software.cybersecurity-defensive.pomerium.k8s-pomerium-jwt-method
name: k8s-pomerium-jwt-method
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [authentication-config, kube-apiserver, jwt-issuer-format, claim-mappings, structured-authentication]
level: advanced
status: docs-checked
description: "Configure kube-apiserver Structured Authentication to trust the Pomerium JWT (Kubernetes 1.30+) with a Pomerium route in front of the API server."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/kubernetes-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended for self-hosted clusters (Kubernetes 1.30+); cloud-hosted clusters may not allow configuring the API server.

**Pomerium route** (`config.yaml`):
- `from`: `https://mycluster.localhost.pomerium.io`
- `to`: the API server address
- `tls_custom_ca`: base64 API server CA cert
- `jwt_issuer_format: uri`
- `set_request_headers`: `Authorization: 'Bearer ${pomerium.jwt}'`

The CA and address can often be copied from an existing kubeconfig.

**API server**: write `authentication_config.yaml` on every control-plane node and start kube-apiserver with `--authentication-config=/path/to/authentication_config.yaml`. Contents: `apiVersion: apiserver.config.k8s.io/v1beta1`, `kind: AuthenticationConfiguration`, and under `jwt`:
- `issuer.url`: `https://mycluster.localhost.pomerium.io/` (trailing slash required)
- `issuer.discoveryURL`: `https://mycluster.localhost.pomerium.io/.well-known/pomerium`
- `issuer.audiences`: `mycluster.localhost.pomerium.io`
- `claimMappings.username`: `claim: email`, `prefix: ''`

Tips: use a non-empty prefix such as `"pomerium:"` to avoid collisions with built-in names; for custom claims configure JWT Claims Headers so they appear in the Pomerium JWT. If configured correctly, Pomerium logs show the API server's requests to the discovery URL and JWKS endpoints (the page's example log has path `/.well-known/pomerium` and `response-code` 200).

## Checked

2026-11-04. Confirmed against the Kubernetes Access page: route setup, authentication config, trailing slash, tips. Reworded the log success note to match the page.

Method: documentation only; no commands were run.
