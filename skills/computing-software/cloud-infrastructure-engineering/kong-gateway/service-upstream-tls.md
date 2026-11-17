---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.service-upstream-tls
name: service-upstream-tls
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, tls-verify, client-certificate, tls-sans, ca-certificates, services, mtls]
level: advanced
status: docs-checked
description: "Verify upstream certificates and present a client certificate per Kong Service with tls_verify, tls_verify_depth, ca_certificates, client_certificate and tls_sans."
sources:
  - https://developer.konghq.com/gateway/entities/service/
  - https://developer.konghq.com/gateway/entities/ca-certificate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service upstream TLS settings

| Field | Meaning |
|---|---|
| `client_certificate` | ID of the certificate Kong presents to the upstream during the TLS handshake |
| `tls_verify` | enable upstream certificate verification; if not set, the global `proxy_ssl_verify` setting is used |
| `tls_verify_depth` | maximum chain depth to verify (0 to 64); default `null` |
| `ca_certificates` | array of CA certificate UUIDs forming the trust store |

These fields apply only to Services whose `protocol` is `https` or `tls`.

CA certificates are separate entities: create one with `POST /ca_certificates/` and use its `id` here. Used globally they verify all upstream server certificates; attached to a Service they verify only that Service.

Global defaults come from `kong.conf`: `client_ssl` (default `off`), `client_ssl_cert` and `client_ssl_cert_key` send a client certificate to all upstreams. The Service field is the per-Service alternative.

To verify client certificates, use the Mutual TLS Authentication or Header Cert Authentication plugins.

## Checked

2026-11-04. Confirmed against services.lua (client_certificate, tls_verify falling back to global proxy_ssl_verify, tls_verify_depth between 0 and 64 default null, ca_certificates UUID array, https/tls-only conditional checks), the CA Certificates page (POST /ca_certificates/, global versus per-Service verification, mTLS plugins) and kong.conf.default (client_ssl, client_ssl_cert, client_ssl_cert_key). Removed tls_sans (not in the Service schema), the claim that the handshake fails with no trusted CAs, and the Nginx-default wording for null.

Method: documentation only; no commands were run.
