---
id: computing-software.software-engineering.java.sslcontext-and-tls-configuration
name: sslcontext-and-tls-configuration
category: computing-software
field: software-engineering
product: java
tags: [java, java-security, sslcontext-tls, tls-protocols, trustmanager, mtls, hostname-verification, javax-net-debug, jdk-tls-disabledalgorithms]
level: advanced
status: docs-checked
description: "Configure Java TLS: build an SSLContext with key and trust managers for mTLS, restrict protocols, keep hostname verification, enable revocation checking."
sources: ["https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSLContext and TLS configuration

## Build a context with custom stores (mTLS)
```java
KeyStore ks = KeyStore.getInstance("PKCS12");
try (var in = Files.newInputStream(Path.of(keyStorePath))) { ks.load(in, pwd); }
KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
kmf.init(ks, pwd);

KeyStore ts = KeyStore.getInstance("PKCS12");
try (var in = Files.newInputStream(Path.of(trustStorePath))) { ts.load(in, tpwd); }
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(ts);

SSLContext ctx = SSLContext.getInstance("TLS");
ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
HttpClient client = HttpClient.newBuilder().sslContext(ctx).build();
```
The JSSE guide builds contexts the same way: key and trust manager factories, then `SSLContext.getInstance("TLS")` and `init`.

## Protocols and ciphers
The JSSE guide lists the protocol names `SSLv3`, `TLSv1`, `TLSv1.1`, `TLSv1.2`, `TLSv1.3` (and DTLS variants). In JDK 21 the default `jdk.tls.disabledAlgorithms` Security Property in `java.security` lists `SSLv3, TLSv1, TLSv1.1, DTLSv1.0` among others, so those protocols are disabled; re-enabling is an anti-pattern and needs an owner-approved exception. Set client default protocols with the `jdk.tls.client.protocols` system property; it has no effect if the application uses a version-specific `SSLContext` or sets enabled protocols explicitly. Prefer the default cipher suites.

## Do not
- Install an "accept all" `X509TrustManager` or `HostnameVerifier` to silence errors. Fix the truststore.
- Skip endpoint identification: for raw `SSLSocket` or `SSLEngine`, check the peer's credentials before sending data, using `SSLParameters.setEndpointIdentificationAlgorithm`. Since JDK 7 HTTPS endpoint identification is enforced by default for `HttpsURLConnection`.

## Debugging
`java -Djavax.net.debug=help MyApp` lists the available `javax.net.debug` options (the guide documents options such as `keymanager` for key manager tracing).

## Gotchas
- Revocation checking is disabled by default. Enable it with the `com.sun.net.ssl.checkRevocation` system property set to `true`; client-driven OCSP also needs the `ocsp.enable` Security Property set to `true`, and has no effect without revocation checking.
- JSSE supports the Server Name Indication (SNI) extension.

## Checked
2026-11-09. Confirmed against the JDK 21 JSSE Reference Guide: SSLContext "TLS" with key and trust manager factories, protocol names, jdk.tls.disabledAlgorithms default entries, jdk.tls.client.protocols and its caveat, endpoint identification guidance for raw SSLSocket/SSLEngine and HttpsURLConnection, javax.net.debug=help, checkRevocation and ocsp.enable behaviour, SNI support.
Removed: the "TLS 1.3 and 1.2 by default" claim, the debug flag strings, the PKIX/SAN/handshake_failure error explanations, the IP-address SNI note, the certificate reload advice, the claim that HttpClient verifies hostnames, "highest mutually supported" and the troubleshooting-security source (no content returned).
Method: documentation only; no commands were run.
