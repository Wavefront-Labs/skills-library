---
id: computing-software.messaging-and-integration.apache-zookeeper.client-and-server-tls
name: client-and-server-tls
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, tls, ssl, keystore, truststore, clientauth, secureclientport, netty]
level: advanced
status: docs-checked
description: "ZooKeeper TLS settings: ssl.keyStore and trustStore properties, store types, protocols, clientAuth default need, hostname verification, and Netty requirement."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS for clients and quorum

- SSL is not supported by NIO: set `serverCnxnFactory=org.apache.zookeeper.server.NettyServerCnxnFactory` (clients use `zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty`). `secureClientPort` is the SSL client port; `clientPort` stays plaintext, and specifying both enables mixed mode. Quorum TLS is switched on with `sslQuorum=true` (3.5.5+).
- Properties: `ssl.keyStore.location`, `ssl.keyStore.password`, `ssl.trustStore.location`, `ssl.trustStore.password` (3.5.5+); quorum equivalents use `ssl.quorum.*`. The Java system property form adds the `zookeeper.` prefix.
- `ssl.keyStore.passwordPath` / `ssl.trustStore.passwordPath` (3.8.0+) name a file holding the password and take precedence over the explicit password property.
- `ssl.keyStore.type` / `ssl.trustStore.type`: JKS, PEM, PKCS12 or null (detect by filename); default null. BCFKS was added in 3.5.10, 3.6.3 and 3.7.0.
- `ssl.protocol` default TLSv1.3 or TLSv1.2 depending on the Java runtime. `ssl.enabledProtocols` default is TLSv1.3 and TLSv1.2 if protocol is TLSv1.3, or TLSv1.2 if protocol is TLSv1.2.
- `ssl.ciphersuites`: JDK defaults since 3.9.6, hard-coded lists in 3.9 and earlier (see the TLS Cipher Suites section).
- `ssl.clientAuth` / `ssl.quorum.clientAuth`: `none`, `want` or `need`; default `need` (added in 3.5.5, broken until 3.5.7).
- `ssl.hostnameVerification` default true; disabling is recommended for testing only. `ssl.clientHostnameVerification` (3.9.4+) default true for quorum, false for clients, and needs hostnameVerification true.
- `ssl.crl` and `ssl.ocsp` default false (`ssl.ocsp` currently implies `ssl.crl`; the page says a future feature release will require setting both). `ssl.sslProvider` (3.9.0+) default `JDK`.
- `client.certReload` (3.7.2, 3.8.1, 3.9.0+) and `sslQuorumReloadCertFiles` (3.5.5, 3.6.0+) default false; they reload keystores and truststores without a restart.
- `client.portUnification` default false: the client port also accepts SSL connections.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (Encryption, Authentication, Authorization options; Netty and Quorum TLS sections). Removed: the "Verify" scenario (a client connecting with a truststore and refusal without a certificate) as it is not a documented test.
