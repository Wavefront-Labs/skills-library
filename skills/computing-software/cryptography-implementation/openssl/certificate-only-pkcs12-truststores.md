---
id: computing-software.cryptography-implementation.openssl.certificate-only-pkcs12-truststores
name: certificate-only-pkcs12-truststores
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pkcs12-truststore, truststore, pkcs12, java, keytool, openssl-pkcs12]
level: practitioner
status: gated
description: "Build certificate-only PKCS#12 truststores with OpenSSL or keytool: -nokeys export, Java trusted-cert attribute, passwords, and verifying entries are trustedCertEntry."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html", "https://bugs.openjdk.org/browse/JDK-8274862"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate-only PKCS#12 truststores

## Java needs a marker
Java treats a certificate in a PKCS#12 as a trusted entry only if it carries the Oracle trusted key usage
attribute (OID 2.16.840.1.113894.746875.1.1) (gated: unconfirmed, source is paywalled or blocked). OpenSSL adds it since 3.2 with `-jdktrust anyExtendedKeyUsage`
(the OpenSSL 3.2 manual lists the option; a test export on 3.2.3 contained that OID plus 2.5.29.37.0, and an export without
the option did not; `openssl pkcs12 ... -nokeys` then shows `Trusted key usage (Oracle): Any Extended Key Usage`).

```sh
openssl pkcs12 -export -nokeys -in ca-bundle.pem -jdktrust anyExtendedKeyUsage \
  -passout pass:changeit -out truststore.p12           # OpenSSL 3.2+
```
Without `-jdktrust`, Java loads the file but sees no trusted certs, and TLS fails with
`PKIX path building failed` or `the trustAnchors parameter must be non-empty` (gated: unconfirmed, source is paywalled or blocked).

## keytool route (gated: unconfirmed, source is paywalled or blocked)
```sh
keytool -importcert -noprompt -alias example-root -file root.pem \
  -keystore truststore.p12 -storetype PKCS12 -storepass changeit
```
Repeat per CA certificate with distinct aliases.

## Inspect
```sh
keytool -list -keystore truststore.p12 -storepass changeit   # entries must be trustedCertEntry (gated: unconfirmed, source is paywalled or blocked)
```

## Notes
- Java 18 added support for a null store password when saving a PKCS12 KeyStore (JDK-8274862, fix version 18); many
  tools still require a password.
- The keytool manual says the default keystore type is PKCS12 from JDK 9. Use `-Djavax.net.ssl.trustStoreType=PKCS12`
  explicitly when the default type differs (gated: unconfirmed, source is paywalled or blocked).
- keytool was not available when this skill was reviewed, so the keytool and JVM behaviours above are unrun.
- Include only CA certificates, not leaf certs, unless pinning is intended.

## Verify
- [ ] Test client connects with `-Djavax.net.ssl.trustStore=truststore.p12` and fails against an unrelated CA.
