---
id: computing-software.cryptography-implementation.crypto-libraries.java-endpoint-identification-hostname-checks
name: java-endpoint-identification-hostname-checks
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jsse, endpoint-identification, hostname-verification, sslengine, sni, java-tls]
level: advanced
status: docs-checked
description: "Turn on hostname verification in Java TLS: raw SSLSocket and SSLEngine skip it by default; set HTTPS or LDAPS endpoint identification and SNI in custom clients."
sources: ["https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/net/ssl/SSLParameters.html", "https://netty.io/wiki/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Endpoint identification for hostname checks (Java)

Certificate path validation proves the certificate came from a trusted CA. Endpoint
identification proves it's for the host you meant to reach. Java does the second only when told.

## Where it is on or off
| API | Hostname check by default |
|---|---|
| `HttpsURLConnection` | yes, enforced during the handshake since JDK 7 (override with `HostnameVerifier`) |
| raw `SSLSocket` / `SSLEngine` | **no**, unless you set an endpoint identification algorithm |
The JSSE guide says to check the peer's credentials before sending data on raw SSLSocket or SSLEngine. Check
other client libraries (HTTP clients, Netty, drivers) against their own documentation. Custom protocols over
raw sockets or SSLEngine (SMTP, database drivers, message brokers) are the usual gap.

## Fix for SSLSocket / SSLEngine
```java
SSLEngine engine = ctx.createSSLEngine(host, port);     // pass the real host and port
engine.setUseClientMode(true);
SSLParameters p = engine.getSSLParameters();
p.setEndpointIdentificationAlgorithm("HTTPS");          // "HTTPS" = RFC 2818
p.setServerNames(List.of(new SNIHostName(host)));       // explicit SNI
engine.setSSLParameters(p);
```
For SSLSocket do the same on `socket.getSSLParameters()` before `startHandshake()`. Use `"LDAPS"`
(RFC 2830) for LDAP-style matching. A non-null algorithm means identification must be handled during the
handshake, to prevent man-in-the-middle attacks. `setServerNames` also affects endpoint identification in
client mode.

## Rules
- Pass the **name the user asked for**, not the resolved IP and not the name from the server's
  certificate.
- Don't turn the check off to make a connection work; fix the certificate or the hostname.

## Test it
Point the client at a server with a valid certificate for a different name (e.g. map
`wrong.example.com` to the server's IP in `/etc/hosts`). The connection must fail.

## Verify
- [ ] Every SSLEngine/SSLSocket creation sets endpoint identification (grep `createSSLEngine`,
      `createSocket`).
- [ ] The wrong-hostname test fails for each client library in the codebase.

## Checked
2026-10-28. Confirmed against the JDK 21 JSSE Reference Guide, SSLParameters API page and the Java Security
Standard Algorithm Names page: HttpsURLConnection enforces HTTPS identification by default since JDK 7, raw
SSLSocket/SSLEngine need `setEndpointIdentificationAlgorithm`, `HTTPS` = RFC 2818, `LDAPS` = RFC 2830,
`setServerNames` affects client-mode identification. Removed: defaults for HttpClient, JNDI, Netty (the whole
Netty section), Apache and OkHttp, wildcard and IP SAN rules, internal property names and the exception text (not
on these pages). The Java code was not compiled or run.
Method: documentation only; no commands were run.
