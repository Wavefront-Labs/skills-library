---
id: computing-software.systems-network-administration.pki-tls-administration.java-truststore-jsse
name: java-truststore-jsse
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [java-truststore-jsse, pki-java, java, jsse, truststore, javax-net-ssl, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Point a JVM app at a private-CA truststore with JSSE system properties, know the cacerts lookup order, and enable revocation checking and TLS debug."
sources:
  - https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java truststores and JSSE settings
Goal: JVM apps trust your private CA without editing the system cacerts.
```
keytool -importcert -trustcacerts -alias corp-root -file root.pem -keystore truststore.p12 -storetype PKCS12
java -Djavax.net.ssl.trustStore=/etc/app/truststore.p12 -Djavax.net.ssl.trustStorePassword=<PASSWORD> -jar app.jar
```
- Default truststore lookup when `javax.net.ssl.trustStore` is not set: `java-home/lib/security/jssecacerts` if it exists, else `java-home/lib/security/cacerts`, else a new empty truststore. If the property names a file that does not exist, no truststore is used (an empty one).
- `javax.net.ssl.trustStoreType` defaults to `KeyStore.getDefaultType()`; with no `trustStorePassword`, the password is assumed to be a blank string. The guide warns against putting the password where other users can see it, for example on the command line; prefer a prompt or a protected option file.
- The JDK ships a limited set of roots in `cacerts`; maintaining its contents is the administrator's job if it is used as the truststore. A separate truststore for your private roots avoids editing it.
- Restrict algorithms with the Security Property `jdk.tls.disabledAlgorithms` in `java.security` (for example `SSLv3, RC4`); a disabled suite cannot be re-enabled by application code.
- Protocol versions on the client: the guide lists `https.protocols` (HttpsURLConnection), `jdk.tls.client.protocols`, `SSLContext.getInstance` and `setEnabledProtocols` as the places to adjust them.
- Debug: `-Djavax.net.debug=ssl:handshake:data` (also `all`, `help`; separators between options are free).
- Revocation checking is off by default (`com.sun.net.ssl.checkRevocation` and `ocsp.enable` both default to false). Client-driven OCSP needs both: system property `com.sun.net.ssl.checkRevocation=true` and Security Property `ocsp.enable=true`; `ocsp.enable` alone has no effect.
Gotcha: a truststore that lacks the issuing chain makes the handshake fail certificate validation; use `javax.net.debug` to see which store was loaded and what the chain was.
Verify:
- [ ] A test client started with `-Djavax.net.ssl.trustStore` connects to the private service.
- [ ] `keytool -list -keystore truststore.p12` shows only the intended CAs.

## Checked
Confirmed 2026-11-08 against the JDK 21 JSSE Reference Guide: truststore lookup, store type and password defaults, properties table (checkRevocation, ocsp.enable, disabledAlgorithms), client-driven OCSP setup, debugging section. Removed (not on the page): the cacerts password, OS package rebuild commands, the `PKIX path building failed` message, and `TLSv1.3,TLSv1.2` property value format.
Method: docs-only read of cited pages, 2026-11-08
