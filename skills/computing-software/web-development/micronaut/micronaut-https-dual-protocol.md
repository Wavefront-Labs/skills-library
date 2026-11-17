---
id: computing-software.web-development.micronaut.micronaut-https-dual-protocol
name: micronaut-https-dual-protocol
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, https, tls, ssl, certificates, dual-protocol, pkcs12]
level: practitioner
status: docs-checked
description: "Serve a Micronaut Netty server over HTTPS using named certificate providers (self-signed, PEM, PKCS12, JKS or SSLContext), and bind HTTP and HTTPS together with redirects."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/https.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/dualProtocol.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS and dual protocol in Micronaut

Goal: enable TLS on the embedded server. HTTPS is off by default; TLS material is defined as named certificate providers under `micronaut.certificate` and referenced from `micronaut.server.ssl.key-name`. The HTTPS port defaults to `8443` (change with `micronaut.server.ssl.port`).

## Self-signed (development)
```yaml
micronaut:
  server:
    ssl:
      enabled: true
      key-name: cert-a
  certificate:
    self-signed:
      cert-a: ""
```
Needs `io.netty:netty-pkitesting` on the runtime classpath. Browsers will warn.

## PEM files (e.g. Let's Encrypt)
```yaml
  certificate:
    file:
      cert-a:
        format: pem
        path: server.key
        certificate-path: server.crt
```

## PKCS#12 or JKS keystore
```yaml
  certificate:
    resource:
      cert-a:
        resource: classpath:server.p12      # or classpath:server.keystore
        password: mypassword
        # format: pkcs12 | jks  (optional, auto-detected)
```
Convert PEM to PKCS#12:
```
openssl pkcs12 -export -in server.crt -inkey server.key -out server.p12 -name someAlias -chain -CAfile ca.crt -caname root
```
Convert PKCS#12 to JKS (the source store password and alias must match the p12 or the conversion fails):
```
keytool -importkeystore -deststorepass newPassword -destkeypass newPassword -destkeystore server.keystore -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass mypassword -alias someAlias
```

## Provided SSLContext
A ready `javax.net.ssl.SSLContext` bean can be used instead; client authentication, protocols and ciphers still apply, and ALPN is negotiated for HTTP/2:
```yaml
micronaut:
  server:
    ssl:
      enabled: true
      context-name: mtls
      client-authentication: need
```
A context set via `ServerSslConfiguration.setSslContext(..)` wins over `context-name`. A provided context cannot be used for HTTP/3.

## Renewal
Use the Micronaut ACME module for automatic certificate refresh, or the file-based certificate provider, which picks up changed key/cert files if the file system supports watching.

## Serve HTTP and HTTPS together
```yaml
micronaut:
  server:
    ssl:
      enabled: true
      build-self-signed: true     # or any other SSL setup above
    dual-protocol: true
    http-to-https-redirect: true  # optional: redirect all HTTP to HTTPS
```
Without `dual-protocol`, only one protocol is enabled.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
