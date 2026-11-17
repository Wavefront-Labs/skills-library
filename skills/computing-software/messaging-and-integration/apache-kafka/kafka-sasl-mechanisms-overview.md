---
id: computing-software.messaging-and-integration.apache-kafka.kafka-sasl-mechanisms-overview
name: kafka-sasl-mechanisms-overview
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, sasl, sasl-enabled-mechanisms, sasl-mechanism-inter-broker-protocol, jaas]
level: practitioner
status: docs-checked
description: "Enable one or several SASL mechanisms (GSSAPI, PLAIN, SCRAM, OAUTHBEARER) and change them in a running cluster."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up SASL authentication on listeners. SASL runs over PLAINTEXT or SSL via the protocols SASL_PLAINTEXT and SASL_SSL; with SASL_SSL, SSL must also be configured. It is supported only by the new Java producer and consumer.

Mechanisms: GSSAPI (Kerberos), PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER.

Broker basics:
```
listeners=SASL_SSL://host.name:port
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```
The JAAS file's `KafkaServer` section is passed with `-Djava.security.auth.login.config=/path/to/kafka_server_jaas.conf`. Clients use `sasl.jaas.config` (allowing different users per client in one JVM) or the `KafkaClient` section (one user per JVM).

Multiple mechanisms: list all login modules in `KafkaServer`, then `sasl.enabled.mechanisms=GSSAPI,PLAIN,SCRAM-SHA-256,SCRAM-SHA-512,OAUTHBEARER`.

Change a mechanism live:
1. Add the new mechanism to `sasl.enabled.mechanisms` and JAAS, then bounce incrementally.
2. Restart clients on the new mechanism.
3. To change inter-broker mechanism, set `sasl.mechanism.inter.broker.protocol` and bounce again.
4. To drop the old one, remove it from both and bounce again.

Slow handshakes: clients may do reverse DNS lookups; use FQDNs in `bootstrap.servers` and `advertised.listeners`.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 Authentication using SASL page (JAAS configuration, SASL configuration, enabling multiple mechanisms and modifying the mechanism in a running cluster).
