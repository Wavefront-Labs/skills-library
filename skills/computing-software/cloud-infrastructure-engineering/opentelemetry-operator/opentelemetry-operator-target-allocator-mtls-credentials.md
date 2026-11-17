---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-mtls-credentials
name: opentelemetry-operator-target-allocator-mtls-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, mtls, usecertmanager, endpoint-credentials, tls-secrets, allowinsecureauthsecrets]
level: sme
status: docs-checked
description: "Serve ServiceMonitor endpoint credentials to collectors over mTLS using cert-manager or user-provided certificates, and know when allowInsecureAuthSecrets applies."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitor credentials and mTLS between allocator and collector

If Service or Pod Monitor endpoints need authentication (bearer tokens, basic auth, OAuth2), the collector must obtain the credentials from the target allocator, and mTLS secures that channel.

With cert-manager (default): cert-manager issues the CA, server and client certificates. Prerequisites: cert-manager installed; the TA has RBAC to get the Secrets referenced by monitors; the operator has a ClusterRole on `cert-manager.io` `issuers`, `certificaterequests` and `certificates` (create, get, list, watch, update, patch, delete). Enable with `spec.mtls.enabled: true` on a `TargetAllocator`, or `spec.targetAllocator.mtls.enabled: true` on the Collector, which the operator forwards. `useCertManager` defaults to true.

Without cert-manager: set `useCertManager: false` and reference your own material under `mtls.tls`:
- `certificateAuthorityCertificate`: exactly one of `secret` or `configMap`.
- `serverCertificate`: the TA HTTPS server certificate and key.
- `clientCertificate`: the collector's client certificate and key.
The server and client blocks reference `certificateSecret` and `keySecret` separately, so they may be different Secrets. Each reference needs `name`; `key` defaults to `tls.crt`, `tls.key` or `ca.crt`. Create them in the workload namespace; a standard `kubernetes.io/tls` Secret works. Keys are mounted at `/tls` through subPath, so rotating certificates requires restarting the pods.

`allowInsecureAuthSecrets` (default false) serves auth secret values over plain HTTP without mTLS; enable it only when a service mesh or equivalent secures the endpoint. In the Operator it is set as `allowInsecureAuthSecrets: true` under `targetAllocator` (or on the standalone TargetAllocator CR); a standalone allocator without the Operator uses its own config file setting.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator README section on endpoint credentials (read in full).
