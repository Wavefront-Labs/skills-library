---
id: computing-software.software-engineering.spring-boot.ssl-bundles-usage-and-reloading
name: ssl-bundles-usage-and-reloading
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, ssl, sslbundles, sslcontext, reload-on-update, lets-encrypt, certbot, tomcat, netty]
level: practitioner
status: docs-checked
description: "Use the SslBundles bean to obtain stores, managers and SSLContext, and reload bundles on certificate change with reload-on-update, including Let's Encrypt PEM files."
sources:
  - https://docs.spring.io/spring-boot/reference/features/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot auto-configures an `SslBundles` bean giving access to each named bundle from `spring.ssl.bundle`. An `SslBundle` offers layers:
- `getStores()`: key store and trust store `KeyStore` instances plus the key store password.
- `getManagers()`: `KeyManagerFactory`, `TrustManagerFactory` and the `KeyManager[]` / `TrustManager[]` they create.
- `createSslContext()`: a new `SSLContext`.
It also gives details of the key, the protocol and options for the SSL engine.

Reloading: bundles can be reloaded when key material changes, but the consuming component must support it. Currently compatible: Tomcat and Netty web servers. Opt in:
```yaml
spring:
  ssl:
    bundle:
      pem:
        mybundle:
          reload-on-update: true
          keystore:
            certificate: "file:/some/directory/application.crt"
            private-key: "file:/some/directory/application.key"
```
A file watcher then reloads the bundle on change, which makes the consumer reload (Tomcat rotates the certificates in its SSL connectors). Set the watcher's quiet period with `spring.ssl.bundle.watch.file.quiet-period`.

Let's Encrypt: Boot does not request or renew certificates. If an external ACME client such as Certbot renews them, point a PEM bundle at its files (typically under `/etc/letsencrypt/live/<domain>/`) and enable reloading:
```yaml
spring:
  ssl:
    bundle:
      pem:
        webserver:
          reload-on-update: true
          keystore:
            certificate: "file:/etc/letsencrypt/live/example.com/fullchain.pem"
            private-key: "file:/etc/letsencrypt/live/example.com/privkey.pem"
server:
  ssl:
    bundle: "webserver"
```
The files in `live` are typically symbolic links into `/etc/letsencrypt/archive`; the file watcher follows symbolic links so updates to the targets trigger a reload.

## Checked

2026-11-07. Read features/ssl.html (Using SSL Bundles, Reloading, Let's Encrypt) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
