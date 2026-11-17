---
id: computing-software.cryptography-implementation.crypto-libraries.jsse-sslparameters-configuration
name: jsse-sslparameters-configuration
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, sslparameters, jsse, java, tls-configuration, sni, alpn, named-groups, endpoint-identification, signature-schemes]
level: practitioner
status: docs-checked
description: "Configure JSSE connections with SSLParameters: protocols, cipher suites, SNI, ALPN, endpoint identification, named groups and signature schemes per socket or engine."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/net/ssl/SSLParameters.html", "https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html", "https://docs.oracle.com/en/java/javase/21/security/java-security-standard-algorithm-names.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSSE SSLParameters configuration

## Per-connection settings
```java
SSLSocket sock = (SSLSocket) ctx.getSocketFactory().createSocket(host, 443);
SSLParameters p = sock.getSSLParameters();
p.setProtocols(new String[] {"TLSv1.3", "TLSv1.2"});
p.setEndpointIdentificationAlgorithm("HTTPS");             // hostname verification
p.setServerNames(List.of(new SNIHostName(host)));
p.setApplicationProtocols(new String[] {"h2", "http/1.1"});
p.setNamedGroups(new String[] {"x25519", "secp256r1"});    // JDK 20+
p.setSignatureSchemes(new String[] {"ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "ed25519"});  // JDK 19+
sock.setSSLParameters(p);
sock.startHandshake();
System.out.println(sock.getSession().getProtocol() + " " + sock.getApplicationProtocol());
```
`SSLEngine` has the same `setSSLParameters(p)`.

## Server side
- `p.setNeedClientAuth(true)` / `setWantClientAuth(true)` for mTLS.
- `p.setUseCipherSuitesOrder(true)` to enforce server preference.
- SNI matching: `p.setSNIMatchers(List.of(SNIHostName.createSNIMatcher("(.*\\.)?example\\.com")))`.

## Process-wide alternatives
System properties: `jdk.tls.client.protocols`, `jdk.tls.namedGroups`, `jdk.tls.client.SignatureSchemes`,
`jdk.tls.server.SignatureSchemes`; security property `jdk.tls.disabledAlgorithms`.

## Gotchas
- On a raw `SSLSocket` or `SSLEngine`, set the endpoint identification algorithm yourself; `java.net.http.HttpClient`
  sets `HTTPS` for you.
- Verify the negotiated protocol, group and scheme with `-Djavax.net.debug=ssl:handshake`.

## Verify
- [ ] Debug output shows the intended protocol, group and signature scheme.
- [ ] Wrong-hostname test certificate is rejected.

## Checked
2026-11-01. Confirmed in the OpenJDK source: SSLParameters setters `setEndpointIdentificationAlgorithm` (1.7),
`setUseCipherSuitesOrder` and `setSNIMatchers` (1.8), `setApplicationProtocols` (9), `setSignatureSchemes` (19),
`setNamedGroups` (20), `setServerNames`; property names `jdk.tls.client.protocols`, `jdk.tls.namedGroups`,
`jdk.tls.client.SignatureSchemes`, `jdk.tls.server.SignatureSchemes`; security property `jdk.tls.disabledAlgorithms`
in java.security; `javax.net.debug` `ssl` and `handshake` components. Removed: silent-ignore, automatic-SNI and
precedence claims.
Method: documentation only; no commands were run.
