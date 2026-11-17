---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gateway-backend-client-certificate-mtls
name: gateway-backend-client-certificate-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [mtls, tls, backend, clientcertificateref, gateway, upstream]
level: advanced
status: docs-checked
description: "Present a client certificate from the Gateway to backends with spec.tls.backend.clientCertificateRef, and how it pairs with BackendTLSPolicy for full mutual TLS upstream."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gateway.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/policy/backendtlspolicy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backend mutual TLS has two halves.

1. Verify the server: `BackendTLSPolicy` (CA source and hostname). See the BackendTLSPolicy skill.
2. Present a client identity: the Gateway sets a client certificate under `spec.tls.backend`, using `tls.backend.clientCertificateRef` to name the client certificate. The Gateway presents it to the backend, in addition to verifying the backend's certificate, so the backend only accepts connections from authorized Gateways.

Points to keep straight:

- The client certificate setting is on the **Gateway** (`tls.backend.clientCertificateRef`), not on the BackendTLSPolicy. It applies to the Gateway as a client for all upstream connections managed by that Gateway.
- BackendTLSPolicy validation needs a `hostname` (the SNI) and either `caCertificateRefs` or `wellKnownCACertificates`; cross-namespace certificate references and wildcard hostnames are not allowed there. Its optional `subjectAltNames` is the Extended feature `BackendTLSPolicySANValidation`.

Contrast with frontend validation, which verifies certificates presented **to** the Gateway by clients.

The TLS guide says the `GatewayBackendClientCertificate` feature has been in the Standard Channel since v1.5.0, and BackendTLSPolicy since v1.4.0. Check your implementation's documentation for support.

## Checked

2026-11-08. Read in full: the TLS configuration guide, the Gateway reference and the BackendTLSPolicy reference (raw markdown on GitHub). Confirmed: tls.backend.clientCertificateRef on the Gateway applying to all upstream connections, the GatewayBackendClientCertificate feature (Standard Channel since v1.5.0), BackendTLSPolicy as the server-verification half (hostname, CA refs, SAN validation, restrictions) and frontend validation as the contrast. Removed: the Secret type, ReferenceGrant and handshake-failure statements, which are not on the pages, and the supportedFeatures pointer.

Method: documentation only; no commands were run.
