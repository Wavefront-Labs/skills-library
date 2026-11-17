---
id: computing-software.systems-network-administration.pki-tls-administration.java-keystore-keytool
name: java-keystore-keytool
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [java-keystore-keytool, pki-java, java, keytool, pkcs12, keystore, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Create, import, list and convert Java keystores with keytool: PKCS12 default, generating a key pair and CSR, importing a CA-signed reply and a chain."
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java keystores with keytool
Goal: a keystore holding a private key and its full chain.
```
keytool -genkeypair -alias app -keyalg EC -groupname secp256r1 -dname "CN=app.example.com" -ext "SAN=dns:app.example.com" -keystore app.p12 -storetype PKCS12 -validity 90
keytool -certreq -alias app -keystore app.p12 -file app.csr -ext "SAN=dns:app.example.com"
keytool -importcert -alias root  -file root.pem  -keystore app.p12 -trustcacerts
keytool -importcert -alias inter -file inter.pem -keystore app.p12
keytool -importcert -alias app   -file app.pem   -keystore app.p12     # certificate reply, after the chain
keytool -list -v -keystore app.p12
keytool -importkeystore -srckeystore old.jks -destkeystore new.p12 -deststoretype PKCS12
```
- Default keystore type is `pkcs12`, set by `keystore.type` in the `java.security` file; `-storetype` overrides it per command. Keystore types are not compatible with each other.
- `-genkeypair`: `-groupname` (for example an EC curve name) and `-keysize` are mutually exclusive; without `-signer` the result is a self-signed certificate stored as a one-element chain. `-validity` is in days from `-startdate` (default now). `-ext` can be repeated and `SAN` is a supported name. The tool does not enforce every certificate profile rule, so check `-dname` and `-ext`.
- `-certreq -ext` shows which extensions are requested in the CSR.
- Importing a certificate reply: keytool validates it against trusted certificates in the keystore (and `cacerts` with `-trustcacerts`) and builds a chain to a self-signed root. A single certificate whose chain cannot be established is not imported, so import the root and intermediates first. A PKCS #7 or multi-certificate reply is ordered user certificate first, then CAs.
- Importing a trusted certificate without `-noprompt` prints its fingerprints for you to compare with a trusted source before accepting.
- Passwords: `-storepass`, `-keypass` and the other password options accept `:env` and `:file` modifiers (`-storepass:file path`); a plain password on the command line is discouraged outside testing. Passwords must be at least six characters.
Verify:
- [ ] `keytool -list -v` shows the private key entry with the full certificate chain.
- [ ] The application starts and `openssl s_client` shows the chain.

## Checked
Confirmed 2026-11-08 against the JDK 21 keytool manual: keystore.type default, genkeypair, certreq, importcert, certificate-reply validation, importkeystore and password modifiers. Removed (not on the page): "PKCS12 is default since Java 9", the `Failed to establish chain from reply` message text, the chain-length output line, Spring/Tomcat property.
Method: docs-only read of cited pages, 2026-11-08
