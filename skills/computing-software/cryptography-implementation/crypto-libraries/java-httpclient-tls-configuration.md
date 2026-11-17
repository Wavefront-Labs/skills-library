---
id: computing-software.cryptography-implementation.crypto-libraries.java-httpclient-tls-configuration
name: java-httpclient-tls-configuration
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, java-httpclient-tls, java, jsse, httpclient, sslcontext, mtls]
level: practitioner
status: docs-checked
description: "Configure TLS for java.net.http.HttpClient: custom SSLContext and SSLParameters, protocol and cipher limits, hostname verification, client certificates and HTTP/2 ALPN."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.Builder.html", "https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# java.net.http.HttpClient TLS configuration

## Custom trust and client certificate
```java
KeyStore ts = KeyStore.getInstance("PKCS12");
ts.load(Files.newInputStream(Path.of("truststore.p12")), tsPass);
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(ts);

KeyStore ks = KeyStore.getInstance("PKCS12");
ks.load(Files.newInputStream(Path.of("client.p12")), ksPass);
KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
kmf.init(ks, ksPass);

SSLContext ctx = SSLContext.getInstance("TLS");
ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

SSLParameters p = new SSLParameters();
p.setProtocols(new String[] {"TLSv1.3", "TLSv1.2"});

HttpClient client = HttpClient.newBuilder()
    .sslContext(ctx).sslParameters(p)
    .version(HttpClient.Version.HTTP_2)          // preferred version; HTTP/2 is the default
    .connectTimeout(Duration.ofSeconds(10)).build();
```

## Behaviour
- The client sets endpoint identification `HTTPS` unless the system property
  `jdk.internal.httpclient.disableHostnameVerification` is true (default false; testing only).
- Without `sslContext(...)` the client uses `SSLContext.getDefault()`; without `sslParameters(...)` it uses an
  implementation-specific default set.

## Pitfalls
- Trust-all `X509TrustManager` copied from Stack Overflow; reject in review.

## Verify
- [ ] `-Djavax.net.debug=ssl:handshake` shows TLS 1.3 and expected certificate; wrong-host test fails.

## Checked
2026-11-01. Confirmed in the OpenJDK java.net.http source: `Builder.sslContext`, `Builder.sslParameters`, `version`,
`HttpClient.Version.HTTP_2` as the default preferred version, defaults to `SSLContext.getDefault()`, the
`jdk.internal.httpclient.disableHostnameVerification` property (default false, testing only) and the `HTTPS`
endpoint identification. Removed: connection-pool and system-property precedence claims.
Method: documentation only; no commands were run.
