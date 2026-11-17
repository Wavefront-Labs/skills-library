---
id: computing-software.messaging-and-integration.apache-kafka.kafka-ssl-hostname-verification-pitfalls
name: kafka-ssl-hostname-verification-pitfalls
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, hostname-verification, ssl-endpoint-identification-algorithm, subject-alternative-name, extended-key-usage]
level: advanced
status: docs-checked
description: "Keep hostname verification on, use SAN entries, and avoid corporate-CA pitfalls such as missing clientAuth key usage."
sources:
  - https://kafka.apache.org/42/security/encryption-and-authentication-using-ssl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get certificates right for production SSL.

Hostname verification checks the server certificate against the actual host to prevent man-in-the-middle attacks. Since Kafka 2.0.0 it is enabled by default for clients and inter-broker connections. Disable it only by setting `ssl.endpoint.identification.algorithm` to an empty string. For dynamic listeners:
`bin/kafka-configs.sh --bootstrap-server localhost:9093 --entity-type brokers --entity-name 0 --alter --add-config "listener.name.internal.ssl.endpoint.identification.algorithm="`
The docs say there is normally no good reason to disable it; it is far harder to fix once the cluster runs.

Clients match the FQDN or IP against the Common Name or the Subject Alternative Name. CN matching has been deprecated since 2000; use SAN (`-ext SAN=DNS:{FQDN},IP:{IPADDRESS}`), which also frees the CN for authorization-friendly naming.

Corporate CA pitfalls:
1. Extended Key Usage: brokers act as both client and server toward each other, so certificates need both clientAuth and serverAuth. A web-server profile with only serverAuth makes the handshake fail.
2. Intermediate certificates: import the entire chain up to the root, for example by concatenating the certificate files.
3. Dropped extensions: CA operators may not copy requested SANs. Inspect the result with `openssl x509 -in certificate.crt -text -noout`.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Encryption and authentication using SSL page. Removed: nothing.

Method: documentation only; no commands were run.
