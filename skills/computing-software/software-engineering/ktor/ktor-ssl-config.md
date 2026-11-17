---
id: computing-software.software-engineering.ktor.ktor-ssl-config
name: ktor-ssl-config
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, ssl, tls, keystore, jks, certificates, https]
level: practitioner
status: docs-checked
description: "Serve HTTPS from Ktor: make a JKS keystore (buildKeyStore, keytool, PEM conversion) and set sslPort and security properties or sslConnector in embeddedServer."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-ssl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor SSL and certificates

Usually Ktor sits behind a reverse proxy (Nginx, Apache) that handles SSL. To serve SSL directly, give Ktor a certificate in a Java KeyStore (JKS). Let's Encrypt can supply a free certificate for `https://` and `wss://`.

## Get a keystore

Ktor needs the certificate at startup, so create it before starting the server.

**In code (testing)**: add `io.ktor:ktor-network-tls-certificates` and call `buildKeyStore`, which returns a `KeyStore`; save it to a keystore file.

**With keytool**:

```bash
keytool -keystore keystore.jks -alias sampleAlias -genkeypair -keyalg RSA -keysize 4096 -validity 3 -dname 'CN=localhost, OU=ktor, O=ktor, L=Unspecified, ST=Unspecified, C=US'
```

It prompts for a keystore password and writes the JKS.

**Convert PEM to JKS** (key in `key.pem`, cert in `cert.pem`):

```bash
openssl pkcs12 -export -in cert.pem -inkey key.pem -out keystore.p12 -name "sampleAlias"
keytool -importkeystore -srckeystore keystore.p12 -srcstoretype pkcs12 -destkeystore keystore.jks
```

Each step prompts for passwords.

## Configure Ktor

**Configuration file** (`application.conf` or `application.yaml`):

1. Set the SSL port with `ktor.deployment.sslPort`.
2. Provide the keystore settings in a separate `security` group (see the `ssl-engine-main` sample for the exact keys).

**embeddedServer**: configure the engine's `ApplicationEngine.Configuration` in a custom environment and call `sslConnector` there to provide the SSL settings.

Gotcha: Ktor requires the certificate at startup, so generate or convert it before the server starts. The examples above use the alias `sampleAlias`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-ssl.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
