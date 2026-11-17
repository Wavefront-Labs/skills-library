---
id: computing-software.data-engineering.trino.trino-tls-direct-coordinator-https
name: trino-tls-direct-coordinator-https
category: computing-software
field: data-engineering
product: trino
tags: [https-keystore, certificates, pem, jks, self-signed]
level: practitioner
status: docs-checked
description: "Enable HTTPS directly on the Trino coordinator: certificate types and formats, keystore properties, insecure-over-http switch, verification and self-signed limits."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/tls.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino tls direct coordinator https

To secure the coordinator itself you need a TLS certificate. Preferred is a globally trusted one (commercial vendor, cloud provider, registrar, or a free generator such as Let's Encrypt), which needs no client configuration. A corporate-CA certificate works if clients trust that CA. Self-signed certificates are never recommended for production: nobody trusts them, every client needs a truststore, and modern browsers reject them. An unsigned certificate (destined for a CA via a CSR) differs from a self-signed one.

Formats: PEM-encoded PKCS #1 or PKCS #8, PKCS #12 and legacy JKS. Binary formats like DER must be converted. Inspect key and certificate files before installing, to save debugging time. The file only needs to be readable by the coordinator process and protected from tampering; putting it in `etc` allows relative paths but you must move it on upgrades.

Coordinator `config.properties` (the property names still say keystore even for PEM):

```text
http-server.https.enabled=true
http-server.https.port=8443
http-server.https.keystore.path=etc/clustercoord.pem
```

Alternatives are `etc/clustercoord.jks` or a `.p12` path. Relative paths resolve from the server root, one level above `etc` in a tar.gz install. JKS always requires `http-server.https.keystore.key=<keystore-password>`; PEM files with passwords are not supported. If the key has its own password set `http-server.https.keymanager.password`.

When an authenticator and HTTPS are both enabled, plain HTTP is disabled for everyone including the Web UI. `http-server.authentication.allow-insecure-over-http=true` re-enables it, which is not recommended.

Verify: open `https://trino.example.com:8443` and log in with any username (the password box is disabled with no authentication), then run `./trino --server https://trino.example.com:8443` and `SELECT 'rocks' AS trino;`.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
