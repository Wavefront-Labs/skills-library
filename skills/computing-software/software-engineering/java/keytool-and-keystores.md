---
id: computing-software.software-engineering.java.keytool-and-keystores
name: keytool-and-keystores
category: computing-software
field: software-engineering
product: java
tags: [java, java-security, keytool-keystore, keystore, truststore, pkcs12, cacerts, certificate-import]
level: practitioner
status: docs-checked
description: "Manage Java keystores and truststores with keytool: PKCS12 default, import CA/server certs, inspect a live server chain, and set javax.net.ssl.* properties safely."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html", "https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keytool and keystores

The keytool manual states the default keystore type is **pkcs12** (set by the `keystore.type` security property); JKS is the older type.

## Commands
```bash
# list / inspect
keytool -list -v -keystore keystore.p12 -storetype PKCS12
keytool -printcert -file server.crt
keytool -printcert -sslserver example.com:443          # read the certificate from a live SSL server (port defaults to 443)

# generate a key pair + self-signed cert (dev only)
keytool -genkeypair -alias app -keyalg RSA -keysize 3072 -sigalg SHA256withRSA \
  -validity 365 -dname "CN=app.example.com" -ext SAN=dns:app.example.com -keystore keystore.p12

# trust an internal CA in an app-specific truststore
keytool -importcert -alias corp-ca -file corp-ca.pem -keystore truststore.p12 -storepass <PASSWORD> -noprompt

# CSR for a CA to sign
keytool -certreq -alias app -file app.csr -keystore keystore.p12
# import the CA's reply (-importcert imports a trusted certificate or a certificate reply received from a CA after a CSR)
keytool -importcert -alias app -file app-signed.pem -keystore keystore.p12

# copy entries between keystores / convert type
keytool -importkeystore -srckeystore a.p12 -destkeystore b.jks -deststoretype JKS
```
`-genkeypair` options include `-keyalg`, `-keysize` (only one of `-groupname` and `-keysize` may be given), `-sigalg` (must be compatible with the key algorithm), `-validity` (days), `-dname`, `-ext` (X.509 extension, repeatable) and `-storetype`. `-printcert` accepts `-file` or `-sslserver`, not both. Without `-destkeystore`, `-importkeystore` writes to the default keystore in your home directory.

## Using them
```
-Djavax.net.ssl.keyStore=<path> -Djavax.net.ssl.keyStorePassword=<from secret>
-Djavax.net.ssl.trustStore=<path> -Djavax.net.ssl.trustStorePassword=<from secret>
```
Per the JSSE reference guide, if `javax.net.ssl.trustStore` is defined the TrustManagerFactory uses that file as the truststore; if it is not defined the default is `jssecacerts` if it exists, otherwise `cacerts`. If `javax.net.ssl.keyStoreType` is not given, the default type is `KeyStore.getDefaultType()`.

## Gotchas
- A custom `javax.net.ssl.trustStore` is used in place of the default lookup, so include the CAs you still need, or build a custom `SSLContext`.
- The JSSE guide calls it inadvisable to pass passwords in a way other users can discover, for example on the command line; keytool accepts `-storepass:env` and `-storepass:file` forms.
- Without `-keypass`, keytool prompts, and pressing Return sets the key password equal to the keystore password.

## Verify
`keytool -list -keystore truststore.p12` shows the alias; a TLS test (`sslcontext-and-tls-configuration`) connects to an HTTPS endpoint signed by the imported CA.

## Checked
Read the keytool manual (Java 21) and the JSSE reference guide: default keystore type, -printcert/-sslserver, -genkeypair options, -importcert purposes, -importkeystore default destination, -storepass env/file forms, trustStore/keyStore property behaviour, password-exposure warning. Removed (not on the cited pages): the OpenSSL conversion, Spring Boot properties, the cacerts default password, the PKIX error text, alias case-sensitivity and PKCS12 store/key password equality claims, and the "Java 9+" default-change date.
Method: docs-only read of cited pages, 2026-11-08
