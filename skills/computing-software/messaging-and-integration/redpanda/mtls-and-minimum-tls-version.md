---
id: computing-software.messaging-and-integration.redpanda.mtls-and-minimum-tls-version
name: mtls-and-minimum-tls-version
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [mtls, tls, require-client-auth, tls-min-version, rpk-tls-flags, client-certificates]
level: practitioner
status: docs-checked
description: "Require client certificates on a Redpanda Kafka API listener, raise tls_min_version, and pass --tls-key, --tls-cert and --tls-truststore to rpk."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
mTLS authenticates the client as well as the server. Clients need certificates signed by the same CA. Set `require_client_auth: true` on the listener TLS block in `redpanda.yaml`:

```yaml
redpanda:
  kafka_api:
  - name: internal
    address: 0.0.0.0
    port: 9092
  advertised_kafka_api:
    - name: internal
      address: <port-clients-connect-to>
    port: 9092
  kafka_api_tls:
  - name: internal
    enabled: true
    require_client_auth: true
    cert_file: <path-to-pem-cert-file>
    key_file: <path-to-pem-key-file>
    truststore_file: <path-to-pem-ca-file>
```
Names: `kafka_api` declares the listener (any name), `advertised_kafka_api` must reuse a declared name and its address is the host clients use, and `kafka_api_tls` must match the listener name. The PKCS#12 variant uses `p12_path` and `p12_password` with `require_client_auth: true` (never alongside PEM file keys).

**Minimum version.** Redpanda defaults `tls_min_version` to 1.2 so clients cannot negotiate a downgrade. Change it with the cluster property, then restart:

```bash
rpk cluster config set tls_min_version <version-number>
systemctl restart redpanda
```
Accepted values named on the page are `v1.0`, `v1.1` and `v1.3`.

**rpk with mTLS identity.** Pass `--tls-key`, `--tls-cert` and `--tls-truststore` to authenticate, for example when creating a topic.

## Checked

2026-11-04. The mTLS YAML, the name-matching rules, `tls_min_version` commands and rpk flags were confirmed on the Encryption page.

Method: documentation only; no commands were run.
