---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.ca-certificate
name: ca-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, ca-certificates, trust-store, tls, admin-api]
level: practitioner
status: docs-checked
description: "Kong CA Certificate entity: create a trusted CA via POST /ca_certificates/ and use it globally or on a Service to verify upstream or client certificates."
sources:
  - https://developer.konghq.com/gateway/entities/ca-certificate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CA certificates

A CA Certificate is a trusted certificate authority Kong uses to verify client or server certificates.

Fields:
- `cert`: PEM public certificate of the CA

Create one:

```bash
curl -i -X POST http://localhost:8001/ca_certificates/ \
  --header "Content-Type: application/json" \
  --data '{ "cert": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n" }'
```

Usage:
- Globally: verifies all upstream server certificates.
- On a Gateway Service: add its UUID to `ca_certificates` to verify that Service's upstream certificate only.
- Client verification: use the Mutual TLS Authentication or Header Cert Authentication plugins.

In self-managed Kong Gateway, CA certificates apply to all Workspaces and appear under every Workspace.

## Checked

2026-11-04. Confirmed against the CA Certificates page: purpose, global versus per-Service verification, mTLS and Header Cert Authentication plugins for client certificates, POST /ca_certificates/ example, Workspace behaviour. Removed cert_digest and the field list (the page's schema table is empty) and the claim that the handshake fails with no trusted CAs.

Method: documentation only; no commands were run.
