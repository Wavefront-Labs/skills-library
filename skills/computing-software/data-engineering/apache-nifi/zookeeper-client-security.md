---
id: computing-software.data-engineering.apache-nifi.zookeeper-client-security
name: zookeeper-client-security
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, zookeeper, sasl, kerberos, tls, nifi-properties]
level: sme
status: docs-checked
description: "Secure NiFi's ZooKeeper client: nifi.zookeeper.client.secure, nifi.zookeeper.security.* stores, SASL Kerberos auth type and bootstrap java.arg JAAS entries."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZooKeeper client security

TLS:
- `nifi.zookeeper.client.secure`: false by default; `nifi.zookeeper.client.ensembleTracker`: true.
- `nifi.zookeeper.security.keystore`, `.keystoreType`, `.keystorePasswd`, `.truststore`, `.truststoreType`, `.truststorePasswd`. Store type is inferred from the extension (`.p12`, `.jks`, `.pem`) when unset. If these are unset, the `nifi.security.*` values are used.

Kerberos:
- `nifi.zookeeper.auth.type=sasl`
- `nifi.zookeeper.kerberos.removeHostFromPrincipal=true` and `nifi.zookeeper.kerberos.removeRealmFromPrincipal=true` (set in the guide's example)
- bootstrap.conf JVM args, for example `java.arg.15=-Djava.security.auth.login.config=./conf/zookeeper-jaas.conf` and `java.arg.16=-Dsun.security.krb5.debug=true` (the guide's example numbers; the page does not discuss numbering).

Verify: with `nifi.zookeeper.client.secure=true`, nifi-app.log shows `ClientCnxnSocketNetty` messages such as "SSL handler added for channel".

## Checked

Checked against the NiFi Administration Guide, Securing ZooKeeper with Kerberos and Securing ZooKeeper with TLS sections: the TLS property table (ensembleTracker true, client.secure false, store types and extension inference, fallback to `nifi.security.*`), `nifi.zookeeper.auth.type=sasl`, the removeHost and removeRealm settings and the java.arg lines match. Removed the claim that the java.arg numbers only need to be unique (not on the page).

Method: docs-only read of cited pages, 2026-11-08
