---
id: computing-software.messaging-and-integration.temporal.last-connection-error-troubleshooting
name: last-connection-error-troubleshooting
category: computing-software
field: messaging-and-integration
product: temporal
tags: [last-connection-error, mtls, certificate-expiry, tcld, openssl, tls-troubleshooting, client-ca]
level: practitioner
status: docs-checked
description: "Fix Temporal Failed reaching server last connection error: check mTLS CA expiry with tcld or openssl, renew, update the Namespace CA, rule out startup race."
sources:
  - https://docs.temporal.io/troubleshooting/last-connection-error
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Failed reaching server: last connection error` usually means an expired TLS certificate, or a Client calling the Server before its roles finish initializing at startup.

Check expiry with one of these:
- Cloud CLI:

    temporal cloud namespace mtls cert-ca list --namespace <namespace_id>.<account_id>

- tcld, reading the date with jq:

    tcld namespace accepted-client-ca list --namespace <namespace_id>.<account_id> | jq -r '.[0].notAfter'

A date in the past means the certificate expired.
- Existing certificate infrastructure, via OpenSSL:

    openssl s_client -connect <namespace_grpc_endpoint> -showcerts -cert ~/certs/path.pem -key ~/certs/path.key -tls1_2

- Self-signed certificates, via the Temporal CLI:

    temporal namespace describe --namespace <namespace_id>.<account_id> --address <namespace_grpc_endpoint> --tls-cert-path <pem> --tls-key-path <key>

The gRPC endpoint is on the Namespace details page in Temporal Cloud.

Renew: ask the issuing CA or your certificate infrastructure administrator. Without infrastructure, generate a new certificate with OpenSSL or the step CLI.

Then install the new CA certificate in the Temporal Cloud Namespace, either through the Cloud UI or with tcld, and retry the connection. Set calendar reminders to issue new CA certificates well before expiry.

If the error persists, confirm the Client presents the correct certificate and that requests arrive after the Server roles are fully initialized; otherwise open a support ticket.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: troubleshooting/last-connection-error (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
