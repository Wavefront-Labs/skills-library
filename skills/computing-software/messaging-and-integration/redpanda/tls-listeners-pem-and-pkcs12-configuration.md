---
id: computing-software.messaging-and-integration.redpanda.tls-listeners-pem-and-pkcs12-configuration
name: tls-listeners-pem-and-pkcs12-configuration
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [tls, encryption, redpanda-yaml, pem, pkcs12, kafka-api-tls, rpc-server-tls, crl]
level: practitioner
status: docs-checked
description: "Enable TLS on Redpanda listeners with PEM or PKCS12 in redpanda.yaml, encrypt the RPC port, and avoid the key_file plus p12_path startup error and a bad CRL."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS needs per-broker `broker.key` and `broker.crt` and a truststore `ca.crt` (all brokers may share it). Make them readable by Redpanda:

```bash
chmod 400 broker.key broker.crt ca.crt
chown redpanda:redpanda broker.key broker.crt ca.crt
```
An optional `ca.crl` lets Redpanda reject revoked certificates. Brokers need SAN entries matching the addresses clients use; corporate-CA certificates need `keyUsage = critical,digitalSignature,keyEncipherment` and `extendedKeyUsage = serverAuth,clientAuth`.

**PEM** (required for FIPS mode), in `redpanda.yaml`:

```yaml
redpanda:
  rpc_server_tls: {}
  kafka_api:
    - address: 0.0.0.0
      port: 9092
      name: tls_listener
  kafka_api_tls:
    - name: tls_listener
      key_file: broker.key
      cert_file: broker.crt
      truststore_file: ca.crt
      crl_file: ca.crl # Optional
      enabled: true
      require_client_auth: false
```
The `kafka_api_tls` name must match the listener name. Keys and certificates are read only at startup, so run `systemctl restart redpanda` after editing.

**Encrypt replication** by setting `rpc_server_tls` with `enabled: true`, the same file keys and `require_client_auth: false`.

**PKCS#12** (single password-protected file, not supported in FIPS mode):

```bash
openssl pkcs12 -export -inkey broker.key -certfile broker.crt -passout pass:<password> -out broker.p12
```
then use `p12_path: <path-to-bundle>` and `p12_password: <password>` in the TLS block. Never set `key_file`/`cert_file` together with `p12_path`/`p12_password`; it causes a startup error.

If you replace a working `ca.crl` with an invalid one, such as unsigned, Redpanda rejects all connections until you fix the file or remove `crl_file` and restart. If Kafka API TLS is on, Schema Registry and HTTP Proxy need `schema_registry_client::broker_tls` and `pandaproxy_client::broker_tls`.

## Checked

2026-11-04. YAML, commands, restart requirement and cautions were confirmed on the Encryption page.

Method: documentation only; no commands were run.
