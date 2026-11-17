---
id: computing-software.cloud-infrastructure-engineering.gateway-api.frontend-client-certificate-validation
name: frontend-client-certificate-validation
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [tls, mtls, frontendvalidation, client-certificate, cacertificaterefs, gateway]
level: advanced
status: docs-checked
description: "Validate client certificates at the Gateway with spec.tls.frontend: CA bundle refs, AllowValidOnly versus AllowInsecureFallback, and per-port overrides."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gateway-level frontend TLS lets the Gateway verify certificates presented by clients (mutual TLS from the client side).

Extended feature `GatewayFrontendClientCertificateValidation`, in the Standard Channel since v1.5.0. Unlike server certificates, which are set per listener, client validation is configured at the **Gateway level** in `spec.tls`, to mitigate risks from HTTP/2 and TLS connection coalescing, where a connection for one listener is reused for another on the same port and could bypass listener-specific validation.

It uses the `frontendValidation` struct:

- A default configuration applies to all HTTPS listeners on the Gateway unless a per-port override is defined.
- `caCertificateRefs` refers to Kubernetes objects (typically ConfigMaps) holding PEM-encoded CA certificate bundles used as trust anchors to validate the client certificate.
- `mode` chooses enforcement:
  - `AllowValidOnly` (default): connections are accepted only if the client presents a certificate that validates against the CA bundle.
  - `AllowInsecureFallback`: connections are accepted even if the client certificate is missing or fails verification. This typically delegates authorization to the backend and should be used with caution. It is the separate Extended feature `GatewayFrontendClientCertificateValidationInsecureFallback`.
- A per-port configuration overrides the default for all listeners handling traffic on that port.

This is distinct from backend mTLS, where the Gateway itself presents a client certificate to the upstream (see the backend client certificate skill), and from BackendTLSPolicy, which validates the upstream server.

## Checked

2026-11-08. Read in full: the TLS configuration guide and the Gateway reference (raw markdown on GitHub). Confirmed: Gateway-level scoping in spec.tls and its HTTP/2 coalescing rationale, frontendValidation with caCertificateRefs, the AllowValidOnly default and AllowInsecureFallback modes, default plus per-port override, and the Extended feature names and Standard Channel since v1.5.0. Removed: the cross-namespace CA ReferenceGrant statement, the migration-period advice and the supportedFeatures pointer, none of which are on the pages. Exact YAML nesting is in the guide's example file, which is not reproduced here.

Method: documentation only; no commands were run.
