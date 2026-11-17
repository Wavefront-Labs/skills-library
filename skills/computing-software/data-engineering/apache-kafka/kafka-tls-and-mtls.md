---
id: computing-software.data-engineering.apache-kafka.kafka-tls-and-mtls
name: kafka-tls-and-mtls
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, kafka-tls, mtls, ssl-listener, keystore, truststore, ssl-client-auth, certificate-rotation, ssl-endpoint-identification]
level: advanced
status: docs-checked
description: "Encrypt Kafka traffic with TLS and authenticate clients with mTLS: listener config, keystores/truststores (PKCS12/PEM), hostname verification, principal mapping and cert rotation."
sources:
  - https://kafka.apache.org/documentation/#security_ssl
  - https://kafka.apache.org/documentation/#security_authz_ssl
  - https://github.com/apache/kafka/blob/trunk/docs/security/encryption-and-authentication-using-ssl.md
  - https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/server/DynamicBrokerConfig.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka TLS and mutual TLS

**Goal:** all client and inter-broker traffic encrypted; optionally clients authenticated by certificate.

## Broker
```properties
listeners=SSL://:9093,CONTROLLER://:9094
advertised.listeners=SSL://broker1.kafka.internal:9093
listener.security.protocol.map=SSL:SSL,CONTROLLER:SSL
inter.broker.listener.name=SSL
ssl.keystore.type=PKCS12
ssl.keystore.location=/etc/kafka/tls/broker1.p12
ssl.keystore.password=${file:/etc/kafka/secrets.properties:keystore.password}
ssl.truststore.type=PKCS12
ssl.truststore.location=/etc/kafka/tls/ca.p12
ssl.truststore.password=${file:/etc/kafka/secrets.properties:truststore.password}
ssl.client.auth=required            # mTLS; default is none (TLS only; pair with SASL for authN); requested = optional
ssl.endpoint.identification.algorithm=https   # default for client and inter-broker connections; empty string disables hostname checks
```
Broker certificates need SANs for every advertised hostname. PEM can be used directly: `ssl.keystore.type=PEM` with the private key in `ssl.keystore.key` and the chain in `ssl.keystore.certificate.chain`; for trust, `ssl.truststore.type=PEM` with `ssl.truststore.certificates`.

## Client
```properties
security.protocol=SSL
ssl.truststore.location=/app/tls/ca.p12
ssl.truststore.password=...
ssl.keystore.location=/app/tls/billing-svc.p12     # only for mTLS
ssl.keystore.password=...
```

## Principals for ACLs
With mTLS the principal is the X.500 distinguished name of the client certificate (`User:CN=billing-svc,OU=data,O=Acme`). Simplify with `ssl.principal.mapping.rules` (rules are tried in order and the first match wins; ignored if a custom `principal.builder.class` is set):
```properties
ssl.principal.mapping.rules=RULE:^CN=([a-zA-Z0-9.-]+),.*$/$1/L,DEFAULT
```
-> `User:billing-svc`.

## Rotation
- Use short-lived certs from an internal CA. Broker keystore and truststore files can be reloaded through a dynamic config update without a restart (the broker source treats `ssl.keystore.location` and `ssl.truststore.location` as reloadable file configs):
```bash
kafka-configs.sh --bootstrap-server $B --entity-type brokers --entity-name 1 --alter \
  --add-config listener.name.ssl.ssl.keystore.location=/etc/kafka/tls/broker1-new.p12
```
Trust the new CA in truststores everywhere **before** issuing certs from it.

## Debugging
```bash
openssl s_client -connect broker1.kafka.internal:9093 -servername broker1.kafka.internal </dev/null | openssl x509 -noout -subject -dates -ext subjectAltName
```
Use the JVM's standard TLS debug property on the client for handshake failures. Typical causes: a certificate without a SAN for the advertised hostname, or a truststore that lacks the issuing CA.

## Verify
- [ ] `openssl s_client` shows the expected chain and SANs on each broker.
- [ ] A client without a cert (mTLS) is rejected; plaintext port is closed.
- [ ] Cert expiry is monitored with an alert well before expiry.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `ssl.client.auth` values and default `none`, `ssl.endpoint.identification.algorithm` default (https) and how to disable it, PEM keystore/truststore property names (`ssl.keystore.key`, `ssl.keystore.certificate.chain`, `ssl.truststore.certificates`), `ssl.principal.mapping.rules` syntax (`RULE:pattern/replacement/[LU]`, first match wins, ignored with a custom principal builder), listener-prefixed dynamic configs, and keystore/truststore location as reloadable file configs (DynamicBrokerConfig source). Removed: the librdkafka line, the PEM "since 2.7" version gate, the `-Djavax.net.debug` argument, named certificate tools and the 30-day figure, none of which the Kafka docs cover.

Method: documentation only; no commands were run.
