---
id: computing-software.cryptography-implementation.crypto-libraries.java-truststore-and-cacerts
name: java-truststore-and-cacerts
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, cacerts, java-truststore, jsse, keytool, javax-net-ssl-truststore, private-ca, trust-store, java]
level: practitioner
status: docs-checked
description: "Manage Java trust: cacerts and jssecacerts lookup, adding private roots with keytool, javax.net.ssl.trustStore semantics and RHEL system roots."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html", "https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html#GUID-7D9F43B8-AABF-4C5B-93E6-3AFB18B66150", "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/securing_networks/using-shared-system-certificates_securing-networks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java truststore and cacerts

## Default trust
With no `javax.net.ssl.trustStore` property, JSSE uses `<java-home>/lib/security/jssecacerts` if it exists,
otherwise `<java-home>/lib/security/cacerts`. A `jssecacerts` file lets you hold JSSE-specific roots apart from
the `cacerts` roots used for code signing.

On RHEL, system roots are managed with `update-ca-trust`, with private anchors placed in
`/etc/pki/ca-trust/source/anchors`. Check how your distro's JDK locates its `cacerts` before editing the JDK file;
distro packages may overwrite it.

## Adding a private root to a JDK store
```
keytool -importcert -cacerts -alias corp-root-2026 -file corp-root.pem -storepass <pw> -noprompt
keytool -list -cacerts -alias corp-root-2026 -storepass <pw>
```

## Application-specific truststore
```
keytool -importcert -keystore app-trust.p12 -storetype PKCS12 -alias corp-root -file corp-root.pem -storepass <pw> -noprompt
java -Djavax.net.ssl.trustStore=/etc/app/app-trust.p12 -Djavax.net.ssl.trustStorePassword=<pw> \
     -Djavax.net.ssl.trustStoreType=PKCS12 -jar app.jar
```
**When `javax.net.ssl.trustStore` is defined, that file is used instead of `jssecacerts`/`cacerts`; it does not add
to them.** If the property names a file that does not exist, the default TrustManager gets an empty keystore. The
value `NONE` is allowed for non-file stores. Include public roots too if the app also calls public endpoints, or
build an `SSLContext` with a composite TrustManager in code.

## Containers
Bake private roots into the image, or mount a truststore and pass the system properties on the command line.
Rebuild images when roots rotate.

## Gotchas
- A handshake that cannot build a path to a trusted root means a missing root or intermediate.
- Trust stores need no private keys; never put keys in them.

## Verify
- [ ] `keytool -list -cacerts` (or `-keystore` for the app store) shows the expected roots.
- [ ] App reaches both internal and public endpoints after the change.

## Checked
2026-10-28. Confirmed against the JDK 21 JSSE Reference Guide (default truststore lookup, `jssecacerts` before
`cacerts`, `trustStore` replaces the default, missing file gives an empty keystore, `NONE`), the keytool man page
(`-cacerts` option, `-importcert`, `-list`) and the Red Hat RHEL 9 shared system certificates page
(`update-ca-trust`, `/etc/pki/ca-trust/source/anchors`). Removed: default password, PKCS12-since-JDK-9, Debian
and RHEL JDK `cacerts` paths, Windows-ROOT and KeychainStore store types, `JAVA_TOOL_OPTIONS`, the PKIX error
text and the debug option (not on these pages).
Method: documentation only; no commands were run.
