---
id: computing-software.cryptography-implementation.crypto-libraries.debugging-java-tls-with-javax-net-debug
name: debugging-java-tls-with-javax-net-debug
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jsse, javax-net-debug, tls-debugging, pkix-path-building, java-tls, jfr-tls-events]
level: practitioner
status: draft
description: "Debug Java TLS failures with javax.net.debug and java.security.debug=certpath: useful option sets, reading handshake logs, common failure signatures and JFR TLS events."
sources: ["https://docs.oracle.com/en/java/javase/21/security/java-secure-socket-extension-jsse-reference-guide.html#GUID-31B7E142-B874-46E9-8DD0-4E18EC0EB2CF", "https://docs.oracle.com/en/java/javase/21/security/troubleshooting-security.html", "https://docs.oracle.com/en/java/javase/21/jfapi/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging with javax.net.debug

## Turn it on
```
java -Djavax.net.debug=ssl:handshake -jar app.jar          # handshake messages, readable size
java -Djavax.net.debug=ssl:handshake:verbose -jar app.jar  # plus message contents
java -Djavax.net.debug=all -jar app.jar                    # everything incl. records (huge)
java -Djava.security.debug=certpath -jar app.jar           # path building and validation detail
```
Other `ssl` sub-options: `keymanager`, `trustmanager`, `session`, `sslctx`, `record`,
`plaintext`. Output goes to stderr as `javax.net.ssl|DEBUG|...` lines. Debug output can include
plaintext application data with `plaintext`/`all`; use it only in test environments and delete logs.

## Read the flow
Search for, in order: `Produced ClientHello` (versions, suites, groups, SNI offered),
`Consuming ServerHello` (what was chosen), `Consuming server Certificate`, then
`Consuming CertificateVerify` and `Finished`. The last message before the exception is where it broke.

## Failure signatures
| Log / exception | Cause | Fix |
|---|---|---|
| `PKIX path building failed: unable to find valid certification path to requested target` | issuer not in the truststore, or server didn't send intermediate | add the CA to the truststore; fix the server chain |
| `No subject alternative DNS name matching X found` | hostname not in SAN | correct cert or hostname |
| `No appropriate protocol` | version disabled on one side | align versions (see disabledAlgorithms) |
| `Received fatal alert: handshake_failure` | no shared suite/group, or server required a client cert | compare ClientHello with server config |
| `Received fatal alert: certificate_required` / `bad_certificate` | mTLS: no or wrong client cert sent | check `keymanager` lines: "No X.509 cert selected" |
| `Certificates do not conform to algorithm constraints` | SHA-1/weak key in chain | reissue |
| `Remote host terminated the handshake` | server closed: SNI mismatch, protocol mismatch, middlebox | compare with `openssl s_client` |

`certpath` debug shows each candidate chain and why it was rejected (expired, constraint,
missing issuer), which `javax.net.debug` often hides.

## Truststore actually in use
Look for `trustStore is:` / `Reloaded ... trust anchors` lines (wording varies by JDK) or the
`trustmanager` option, which lists every loaded anchor. Surprises: the container's JDK `cacerts`
instead of your file, or a `-Djavax.net.ssl.trustStore` that points to a missing file (JDK
silently falls back in some versions).

## Low-overhead production signal: JFR
`jdk.TLSHandshake`, `jdk.X509Certificate` and `jdk.X509Validation` JFR events (JDK 20+, backported
to some 11/17 updates) record peer host, protocol, cipher suite and certificate IDs with little
overhead: `java -XX:StartFlightRecording:settings=custom.jfc` with those events enabled.

## Verify
- [ ] The failing handshake is reproduced with `ssl:handshake` and the breaking message identified.
- [ ] Debug flags are removed from production launch configs afterwards.
