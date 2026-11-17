---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-tls-and-mtls
name: otel-collector-tls-and-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [exporter-tls-config, mtls-collector, collector-config, otel-collector, tls]
level: practitioner
status: docs-checked
description: "Configure TLS and mutual TLS on OTel Collector receivers and exporters: cert files, client CA, insecure flags, server name override, reload, and cert-manager on Kubernetes."
sources: ["https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md", "https://opentelemetry.io/docs/collector/configuration/", "https://cert-manager.io/docs/usage/certificate/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/otlpexporter/README.md", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/otlphttpexporter/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector TLS and mTLS

## Receiver (server side)
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        tls:
          cert_file: /certs/tls.crt
          key_file: /certs/tls.key
          client_ca_file: /certs/ca.crt     # presence of this = require client certs (mTLS)
          min_version: "1.2"
          reload_interval: 1h               # pick up renewed certs without restart
      http:
        endpoint: 0.0.0.0:4318
        tls: {cert_file: /certs/tls.crt, key_file: /certs/tls.key}
```
No `tls` block = plaintext.

## Exporter (client side)
```yaml
exporters:
  otlp/gateway:
    endpoint: otel-gateway.observability.svc:4317
    tls:
      ca_file: /certs/ca.crt
      cert_file: /certs/client.crt          # for mTLS
      key_file: /certs/client.key
      server_name_override: otel-gateway.example.internal   # if cert SAN differs from dial address
  otlp/plain:
    endpoint: otel-gateway:4317
    tls: {insecure: true}                   # plaintext gRPC
```
- In current releases the exporter types are named `otlp_grpc` and `otlp_http`; `otlp` and `otlphttp` are deprecated aliases (exporter metadata.yaml, v0.163.0), so the examples above still work.
- The `otlp` (gRPC) exporter requires TLS by default (README); plaintext needs `tls: {insecure: true}`. An `https` scheme in `endpoint` enables transport security and overrides `insecure`.
- The `otlphttp` exporter's `endpoint` is a base URL (for example `https://example.com:4318`); use an `https://` URL for TLS.
- `insecure_skip_verify: true` keeps TLS but skips verification (default false); use only for debugging.
- `ca_pem`, `cert_pem` and `key_pem` take certificate contents as a string instead of a path (for example `${env:CA_PEM}`).
- `client_ca_file` (server side) sets ClientAuth to RequireAndVerifyClientCert; `client_ca_file_reload` (default false) reloads it when modified. `min_version` defaults to "1.2". `server_name_override` overrides the :authority virtual host name (the README says typically for testing).

## Kubernetes with cert-manager
Issue a cert-manager `Certificate` for the gateway Service DNS names and mount the resulting Secret; clients mount the CA.
cert-manager renews certificates before expiry (`renewBefore`); `reload_interval` (unset means never reloaded) lets the
collector pick up the renewed files.

## Debugging
- `x509: certificate signed by unknown authority` -> wrong/missing `ca_file`.
- `x509: certificate is valid for X, not Y` -> SAN mismatch, use `server_name_override` or fix SANs.
- `tls: first record does not look like a TLS handshake` -> TLS client to plaintext server.
- `transport: authentication handshake failed: remote error: tls: certificate required` -> mTLS server, no client cert.
- Test: `openssl s_client -connect gw:4317 -alpn h2 -CAfile ca.crt -cert client.crt -key client.key`.
- The error strings above come from Go's crypto/x509 and crypto/tls and grpc-go's transport.

## Checked

2026-10-24. OpenTelemetry Collector configtls, configgrpc and otlpexporter/otlphttpexporter READMEs (main branch), cert-manager Certificate docs, Go crypto/x509, crypto/tls and grpc-go source (error strings), and OpenSSL s_client manual. Confirmed: `insecure`, `insecure_skip_verify`, `ca_pem`/`cert_pem`/`key_pem`, `client_ca_file` semantics, `client_ca_file_reload`, `reload_interval` default (never), `min_version` default, `server_name_override`, exporter TLS defaults, cert-manager auto-renewal, the five error messages, and the s_client options.

Method: documentation only; no commands were run.
