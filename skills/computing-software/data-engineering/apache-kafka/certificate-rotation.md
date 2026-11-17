---
id: computing-software.data-engineering.apache-kafka.certificate-rotation
name: certificate-rotation
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-security, kafka-certificate-rotation, kafka-tls, keystore, truststore, scram-rotation, dynamic-ssl]
level: advanced
status: docs-checked
description: "Rotate Kafka TLS certificates, CAs and SCRAM credentials without downtime: dual-CA truststores, dynamic keystore reload via kafka-configs, and client rollout order."
sources:
  - https://kafka.apache.org/documentation/#dynamicbrokerconfigs
  - https://kafka.apache.org/documentation/#security_ssl
  - https://kafka.apache.org/documentation/#security_sasl_scram_credentials
  - https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/server/DynamicBrokerConfig.scala
  - https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/config/internals/BrokerSecurityConfigs.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate and credential rotation

**Goal:** replace expiring broker/client certificates (or a whole CA) and passwords with zero client disconnect storms.

## Broker leaf certificate (same CA)
Brokers can reload a listener's keystore dynamically, without a restart (per-broker dynamic config; see the Dynamic Update Mode column in Broker Configs):
1. Write the new keystore to a **new path** (or same path with new content).
2. Trigger reload per broker:
```bash
kafka-configs.sh --bootstrap-server $BS --command-config admin.properties \
  --entity-type brokers --entity-name 1 --alter \
  --add-config listener.name.external.ssl.keystore.location=/etc/kafka/tls/broker1-2026.jks
```
Kafka rejects a dynamic keystore update that changes the certificate distinguished name or subject alternative names unless `ssl.allow.dn.changes` or `ssl.allow.san.changes` is true (both default false).

## CA rotation (the risky one)
Order matters: trust before use.
1. Build truststores containing **old + new CA**. Roll them out to all clients and brokers (broker truststore is also dynamic: `listener.name.<l>.ssl.truststore.location`).
2. Reissue broker certs from the new CA; reload keystores (above). Clients already trust both.
3. Reissue client certs (mTLS) from the new CA; roll clients.
4. Once nothing presents old-CA certs, remove the old CA from truststores.
Skipping step 1 makes handshakes fail for peers that do not yet trust the new CA.

## Client certificates
Roll clients with their new keystores. Expiry monitoring for client certs belongs to the client owners; publish expiry dates.

## SCRAM password rotation
SCRAM credentials are stored per user in the metadata log; changing the password breaks clients still using the old one. Use two users:
```bash
kafka-configs.sh --bootstrap-server $BS --alter --entity-type users --entity-name billing-v2 \
  --add-config 'SCRAM-SHA-512=[iterations=8192,password=NEWSECRET]'
```
Grant same ACLs to `billing-v2`, move clients, then delete `billing-v1` credentials with `--alter --delete-config 'SCRAM-SHA-512'`. (Or accept a brief restart window with one user.)

## Monitoring expiry
```bash
echo | openssl s_client -connect broker1:9094 -servername broker1 2>/dev/null | openssl x509 -noout -enddate
keytool -list -v -keystore broker1.jks
```
Alert well before expiry.

## Gotchas
- Inter-broker listener cert changes affect replication; do one broker at a time and watch URP.
- Hostname verification (`ssl.endpoint.identification.algorithm=https`, default) requires SANs for every advertised hostname, including load balancer names.
- PEM keystores (`ssl.keystore.type=PEM`, with `ssl.keystore.key` and `ssl.keystore.certificate.chain`) avoid converting certificates to PKCS12 or JKS.

## Verify
- [ ] `openssl s_client` shows new expiry on every broker listener.
- [ ] No spike in the `failed-authentication-total` client metric (producer, consumer and connect metrics) during rollout.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: dynamic keystore and truststore location updates (DynamicBrokerConfig source), `ssl.allow.dn.changes` and `ssl.allow.san.changes` with default false (BrokerSecurityConfigs source), SCRAM add and delete via `kafka-configs.sh` with credentials in the metadata log, PEM property names, hostname verification default, and `failed-authentication-total` (documented only as a client metric, so the earlier "broker metric" was wrong). Removed: the 1.1 and 2.7 version gates, the PKIX message, the claim that Java clients load keystores only at startup, the 30-day figure and the Strimzi and cert-manager remark.

Method: documentation only; no commands were run.
