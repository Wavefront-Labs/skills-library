---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.auth-extensions-for-receivers
name: auth-extensions-for-receivers
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, security, authentication, extensions, oidc, oauth2client]
level: advanced
status: docs-checked
description: "Authenticate incoming and outgoing Collector traffic with authenticator extensions such as oidc and oauth2client."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most receivers exposing an HTTP or gRPC port, and most exporters using HTTP or gRPC clients, can use the Collector's authentication mechanism. It is built on extensions, and each authentication extension can serve as a client authenticator for exporters (adding auth data to outgoing requests) or a server authenticator for receivers (authenticating incoming connections).

To add a server authenticator to a receiver:

1. Add the extension and its configuration under `extensions`.
2. Reference it under `service::extensions` so the Collector loads it.
3. Reference it under the receiver's `auth` block, in its HTTP or gRPC config.

```yaml
extensions:
  oidc:
    issuer_url: http://localhost:8080/auth/realms/opentelemetry
    audience: collector
receivers:
  otlp/auth:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        auth:
          authenticator: oidc
service:
  extensions:
    - oidc
```

On the agent side, the OAuth2 client extension makes the exporter obtain tokens and add them to every RPC:

```yaml
extensions:
  oauth2client:
    client_id: agent
    client_secret: some-secret
    token_url: http://localhost:8080/auth/realms/opentelemetry/protocol/openid-connect/token
exporters:
  otlp_grpc/auth:
    endpoint: remote-collector:4317
    auth:
      authenticator: oauth2client
```

The Registry on the OpenTelemetry site lists known authenticators.

## Checked

Method: docs-checked 2026-11-09 against the Collector configuration page, Authentication section (raw markdown, read in full for that section).
