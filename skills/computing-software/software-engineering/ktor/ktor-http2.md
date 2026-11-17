---
id: computing-software.software-engineering.ktor.ktor-http2
name: ktor-http2
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, http2, alpn, netty, jetty, h2c, tls]
level: advanced
status: docs-checked
description: "Enable HTTP/2 in a Ktor server: self-signed keystore, ALPN for Jetty versus Netty tcnative, and cleartext h2c on Netty with enableHttp2 and enableH2c."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-http2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor HTTP/2

Ktor supports HTTP/2 on the Jetty and Netty engines only, each with its own setup. Once the host is configured, HTTP/2 is activated automatically.

HTTP/2 over TLS needs (1) an SSL certificate (may be self-signed) and (2) an ALPN implementation supported by the engine. HTTP/2 over cleartext (h2c) is Netty-only and needs neither.

## 1. Certificate

Browsers typically speak HTTP/2 only over encrypted connections. For testing:

```bash
keytool -keystore test.jks -genkeypair -alias testkey -keyalg RSA -keysize 4096 -validity 5000 -dname 'CN=localhost, OU=ktor, O=ktor, L=Unspecified, ST=Unspecified, C=US'
```

You can also build a keystore programmatically with `buildKeyStore()`. Point Ktor at the keystore in `application.conf` or `application.yaml`.

## 2. ALPN

**Jetty**: no extra Ktor config. Create a server with the Jetty engine, configure the certificate, and configure `sslPort`.

**Netty**: add the Netty `tcnative` OpenSSL bindings to the build (the page's Gradle example uses the statically linked BoringSSL build). The `tc.native.classifier` can be `linux-x86_64`, `osx-x86_64`, or `windows-x86_64`.

## 3. Cleartext h2c (Netty)

Useful inside private networks. Clients can connect with h2c directly or upgrade an HTTP/1.1 connection. Set both options:

```kotlin
embeddedServer(Netty, configure = {
    connector {
        port = 8080
    }
    enableHttp2 = true
    enableH2c = true
})
```

h2c and HTTP/2 over TLS can run on the same server: cleartext connectors accept h2c, SSL connectors use HTTP/2 over TLS.

Runnable samples: `http2-netty` and `http2-jetty` in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-http2.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
