---
id: computing-software.data-engineering.apache-nifi.https-keystore-truststore
name: https-keystore-truststore
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, https, tls, keystore, truststore, autoreload]
level: practitioner
status: docs-checked
description: "Enable HTTPS in NiFi: nifi.security.keystore and truststore keys, types PKCS12/JKS/BCFKS, unset http port, ciphersuite include/exclude, and keystore autoreload."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTPS in nifi.properties

- `nifi.security.keystore`, `.keystoreType`, `.keystorePasswd`, `.keyPasswd` (falls back to the keystore password if unset).
- `nifi.security.truststore`, `.truststoreType`, `.truststorePasswd`. A secured instance with no truststore rejects all incoming connections.
- Types: `PKCS12`, `JKS` or `BCFKS` (JKS preferred).
- `nifi.web.https.host` (`0.0.0.0` for all interfaces), `nifi.web.https.port` (8443). `nifi.web.http.port` must be unset.
- `nifi.web.https.ciphersuites.include` replaces system defaults; `.exclude` filters.
- `nifi.security.autoreload.enabled` false by default; `nifi.security.autoreload.interval` 10 secs. Autoreload ignores changes to store paths or passwords.
- Secure site-to-site by setting `nifi.remote.input.secure` to true and cluster traffic by setting `nifi.cluster.protocol.is.secure` to true; these always require two-way SSL using each node's keystore and truststore.

Client certs: with no other login strategy NiFi requires them; with another strategy it only wants them.

Verify: the UI answers on the HTTPS port and the plain HTTP port is closed.

## Checked

Confirmed in the NiFi Administration Guide, Security Configuration and the nifi.properties Web Properties and Security Properties tables: keystore and truststore keys and types (PKCS12, JKS, BCFKS, JKS preferred), keyPasswd fallback, no-truststore refusal, https host 0.0.0.0 and port 8443, http port must be unset, cipher suite include/exclude, client certificate required or wanted, autoreload enabled false and interval 10 secs, and autoreload ignoring store path or password changes.

Method: docs-only read of cited pages, 2026-11-08
