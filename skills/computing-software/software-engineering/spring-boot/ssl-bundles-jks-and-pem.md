---
id: computing-software.software-engineering.spring-boot.ssl-bundles-jks-and-pem
name: ssl-bundles-jks-and-pem
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, ssl, ssl-bundle, jks, pkcs12, pem, keystore, truststore]
level: practitioner
status: docs-checked
description: "Define named SSL bundles with spring.ssl.bundle.jks (JKS or PKCS12) or spring.ssl.bundle.pem, for server keystores and client truststores, with Base64 and inline PEM."
sources:
  - https://docs.spring.io/spring-boot/reference/features/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Properties prefixed `spring.ssl.bundle` define named sets of trust material, applied to several types of connections.

JKS or PKCS12 (`spring.ssl.bundle.jks.<name>`), created with `keytool`. A server keystore holds a certificate and private key:
```yaml
spring:
  ssl:
    bundle:
      jks:
        mybundle:
          key:
            alias: "application"
          keystore:
            location: "classpath:application.p12"
            password: "secret"
            type: "PKCS12"
```
A client-side truststore holds the server certificate:
```yaml
spring:
  ssl:
    bundle:
      jks:
        mybundle:
          truststore:
            location: "classpath:server.p12"
            password: "secret"
```
Full property set: `JksSslBundleProperties`.

PEM (`spring.ssl.bundle.pem.<name>`): server keystore with `certificate` and `private-key`; client truststore with `certificate`:
```yaml
spring:
  ssl:
    bundle:
      pem:
        mybundle:
          keystore:
            certificate: "classpath:application.crt"
            private-key: "classpath:application.key"
          truststore:
            certificate: "classpath:server.crt"
```
Full property set: `PemSslBundleProperties`. PEM values containing `BEGIN` and `END` markers are treated as inline PEM content rather than a resource location. This applies to both `certificate` and `private-key`, and to truststore certificates.

For either type, a location can be replaced by Base64 content, with the property value starting `base64:`. With environment variables, the bundle name is always converted to lowercase.

Bundles are then referred to by name in the configuration of auto-configured connections: embedded web servers, data technologies and REST clients.

## Checked

2026-11-07. Read features/ssl.html (JKS, PEM, Applying SSL Bundles) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Removed the unconfirmed 'use a YAML block scalar |' advice; the page shows inline PEM as a plain multi-line value and applies the BEGIN/END rule to certificate and private-key. The Javadoc for JksSslBundleProperties and PemSslBundleProperties was not opened. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
