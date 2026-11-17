---
id: computing-software.messaging-and-integration.apache-kafka.kafka-sasl-kerberos-gssapi
name: kafka-sasl-kerberos-gssapi
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kerberos, gssapi, krb5-login-module, sasl-kerberos-service-name]
level: advanced
status: docs-checked
description: "Configure SASL/GSSAPI Kerberos with per-broker keytabs, the KafkaServer JAAS section and sasl.kerberos.service.name."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate brokers and clients through Kerberos.

Prerequisites: a Kerberos server (an existing Active Directory is fine), a principal per broker and per OS user running clients, and hosts that resolve by FQDN (a Kerberos requirement). For your own KDC: `kadmin.local -q 'addprinc -randkey kafka/{hostname}@{REALM}'` then `ktadd -k /path/to/{keytabname}.keytab kafka/{hostname}@{REALM}`. Oracle Java needs the JCE policy files.

Broker JAAS (each broker has its own keytab, readable by the broker's OS user):
```
KafkaServer {
    com.sun.security.auth.module.Krb5LoginModule required
    useKeyTab=true storeKey=true
    keyTab="/path/to/kafka_server.keytab"
    principal="kafka/kafka1.hostname.com@EXAMPLE.COM";
};
```
JVM flags: `-Djava.security.krb5.conf=/path/to/krb5.conf` and `-Djava.security.auth.login.config=/path/to/kafka_server_jaas.conf`.

server.properties:
```
listeners=SASL_PLAINTEXT://host.name:port
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=GSSAPI
sasl.enabled.mechanisms=GSSAPI
sasl.kerberos.service.name=kafka
```
The service name must match the primary of the broker principal.

Clients: `sasl.jaas.config` with Krb5LoginModule and a keytab (recommended for long-running processes), or `useTicketCache=true` after kinit for console tools; plus `security.protocol=SASL_PLAINTEXT` (or SASL_SSL), `sasl.mechanism=GSSAPI`, `sasl.kerberos.service.name=kafka`.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 Authentication using SASL page (Authentication using SASL/Kerberos section). An unsupported operational-notes paragraph was removed.
