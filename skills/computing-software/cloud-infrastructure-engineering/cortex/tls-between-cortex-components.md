---
id: computing-software.cloud-infrastructure-engineering.cortex.tls-between-cortex-components
name: tls-between-cortex-components
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [tls, mtls, grpc, certificates, security]
level: advanced
status: docs-checked
description: "Secure Cortex inter-service HTTP and gRPC traffic with TLS, including how to generate a private CA and client and server certificates."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex has heavy service-to-service traffic, and TLS is supported between all components. Use a private Certifying Authority, because any certificate it signs can talk to the cluster.

The guide generates keys with `openssl genrsa` for a root, a client and a server; creates a root certificate with `openssl req -x509`; creates CSRs for client and server (the server CSR uses `CN=localhost` in the example); and signs both with `openssl x509 -req -CA root.crt -CAkey root.key`. The sample validity is 100,000 days, but the guide recommends replacing certificates at least every 2 years.

The result is `client.key`, `client.crt`, `server.key`, `server.crt` and `root.crt`. Load them into each component using the server and client TLS flags.

Server flags, for both HTTP and gRPC: `-server.http-tls-cert-path`, `-server.http-tls-key-path`, `-server.http-tls-client-auth` (the guide uses `RequireAndVerifyClientCert`) and `-server.http-tls-ca-path`, plus the same four with `grpc` in place of `http`.

Client flags are component-specific. Examples from the guide: the Alertmanager HTTP client uses `-alertmanager.configs.tls-cert-path`, `-alertmanager.configs.tls-key-path` and `-alertmanager.configs.tls-ca-path`; the querier gRPC client to the frontend uses `-querier.frontend-client.tls-cert-path`, `-tls-key-path` and `-tls-ca-path`; the ingester gRPC client uses `-ingester.client.tls-cert-path`, `-tls-key-path` and `-tls-ca-path`. Other HTTP and gRPC clients are configured similarly.

## Checked

Method: docs-checked 2026-11-09 against the Cortex TLS guide (raw markdown, read in full).
