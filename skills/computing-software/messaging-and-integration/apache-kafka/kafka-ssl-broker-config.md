---
id: computing-software.messaging-and-integration.apache-kafka.kafka-ssl-broker-config
name: kafka-ssl-broker-config
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, ssl-client-auth, ssl-keystore-location, ssl-enabled-protocols, ssl-secure-random-implementation]
level: practitioner
status: docs-checked
description: "Configure broker SSL settings, require client certificates with ssl.client.auth and test the listener with openssl s_client."
sources:
  - https://kafka.apache.org/42/security/encryption-and-authentication-using-ssl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable SSL on a broker once keystores exist.

Listeners: if inter-broker traffic is not SSL, keep both: `listeners=PLAINTEXT://host.name:port,SSL://host.name:port`. To use SSL between brokers add `security.inter.broker.protocol=SSL` (default PLAINTEXT).

Required:
```
ssl.keystore.location=/path/to/server.keystore.jks
ssl.keystore.password=...
ssl.key.password=...
ssl.truststore.location=/path/to/server.truststore.jks
ssl.truststore.password=...
```
`ssl.truststore.password` is technically optional but recommended; without it the truststore stays readable but integrity checking is disabled.

Optional:
- `ssl.client.auth=none` (default); `required` demands client certificates; `requested` is discouraged because it gives false security as misconfigured clients still connect.
- `ssl.cipher.suites`, `ssl.enabled.protocols`, `ssl.keystore.type`, `ssl.truststore.type`.
- `ssl.secure.random.implementation=SHA1PRNG`: the default NativePRNG on Linux uses a global lock; SHA1PRNG is non-blocking and performed well at 50 MB/sec of produced messages plus replication per broker.

Verify: server.log lists the endpoints, for example `PLAINTEXT -> EndPoint(...,9092,PLAINTEXT),SSL -> EndPoint(...,9093,SSL)`, and `openssl s_client -debug -connect localhost:9093 -tls1` should print the server certificate (TLSv1 must be listed in `ssl.enabled.protocols`).

Each broker node has its own server.keystore.jks; the truststore can be the same for all clients and brokers.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 Encryption and Authentication using SSL page (Configuring Kafka Brokers section and the truststore and keystore notes). Unsupported claims on file permissions and misconfiguration diagnosis were removed.
