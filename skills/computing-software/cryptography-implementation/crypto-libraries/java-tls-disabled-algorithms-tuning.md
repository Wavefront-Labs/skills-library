---
id: computing-software.cryptography-implementation.crypto-libraries.java-tls-disabled-algorithms-tuning
name: java-tls-disabled-algorithms-tuning
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jsse, disabledalgorithms, java-security, certpath-constraints, tls-policy, java-tls]
level: advanced
status: docs-checked
description: "Tune jdk.tls.disabledAlgorithms and jdk.certpath.disabledAlgorithms safely: read the defaults, edit or set them before JSSE initialises, and diagnose blocked handshakes."
sources: ["https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html", "https://www.java.com/en/configure_crypto.html", "https://docs.oracle.com/en/java/javase/21/security/java-security-overview1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jdk.tls.disabledAlgorithms tuning

Java's TLS and certificate policy lives in `$JAVA_HOME/conf/security/java.security`. Oracle and
OpenJDK tighten it in updates (the JRE crypto roadmap lists changes), so a JDK patch can break a
connection to a legacy peer.

## The properties
- `jdk.tls.disabledAlgorithms`: protocols, cipher suites, key exchange and key sizes for TLS.
  Recent defaults include `SSLv3, TLSv1, TLSv1.1, DTLSv1.0, RC4, DES, MD5withRSA,
  DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL, ECDH` (JDK 21 JSSE guide).
- `jdk.certpath.disabledAlgorithms`: what certificate chains may use, e.g. `MD2, MD5,
  SHA1 jdkCA & usage TLSServer, RSA keySize < 1024, ...` (Oracle's crypto roadmap page shows `SHA1 jdkCA & usage
  TLSServer` as a constraint to add).
- `jdk.tls.legacyAlgorithms`: legacy algorithms are not negotiated unless there are no other candidates; default
  `NULL, anon, RC4, DES, 3DES_EDE_CBC`.
- Print the effective value: `Security.getProperty("jdk.tls.disabledAlgorithms")`.

## Override narrowly
Edit `<java-home>/conf/security/java.security`, or set the Security Property dynamically before JSSE is
initialised (`Security.setProperty`). Keep the full default list and change only the items you need; a typical
entry is
`jdk.tls.disabledAlgorithms=SSLv3, RC4, DES, MD5withRSA, DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL`.
- You can also tighten: add protocols or raise `DH keySize`.
- Protocol choice per process without editing policy: `-Djdk.tls.client.protocols=TLSv1.3,TLSv1.2`; the
  `jdk.tls.namedGroups` system property sets enabled groups in preference order.
- A suite containing a disabled component is not used even if the application enables it explicitly.

## Diagnose a blocked handshake
| Exception text | Meaning |
|---|---|
| `Received fatal alert: handshake_failure` | alert sent when negotiation fails, e.g. no common cipher suite or group |
Turn on `-Djavax.net.debug=ssl:handshake` to see the offered and rejected items. (Messages such as "No appropriate
protocol" or "algorithm constraints" also point at a disabled item; search the debug output for the rejected name.)

## Re-enabling something old (a legacy peer)
1. Confirm the peer can't be upgraded and document it.
2. Override only that item for the one service that needs it, ideally a dedicated process or
   gateway in front of the legacy system.
3. Add a removal date and a monitoring check; the next JDK may remove the code path anyway.

## Verify
- [ ] Effective properties are printed in startup logs.
- [ ] Overrides are version-controlled with the app.
- [ ] A JDK upgrade test suite connects to every external TLS dependency.

## Checked
2026-10-28. Confirmed against the Oracle JSSE Reference Guide (JDK 21) and java.com crypto roadmap page: default
`jdk.tls.disabledAlgorithms` and `jdk.tls.legacyAlgorithms` values, `java.security` location, dynamic
Security.setProperty before JSSE init, disabled suites stay disabled when re-enabled by the app,
`jdk.tls.client.protocols`, `jdk.tls.namedGroups`, `SHA1 jdkCA & usage TLSServer`. Removed: the
`java.security.properties` override mechanics, `TLS_RSA_*` default, `-XshowSettings`, `jdk.security.legacyAlgorithms`,
`jdk.jar.disabledAlgorithms` and exact exception texts (not on these pages).
Method: documentation only; no commands were run.
