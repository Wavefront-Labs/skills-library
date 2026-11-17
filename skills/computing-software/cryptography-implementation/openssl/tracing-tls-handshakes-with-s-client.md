---
id: computing-software.cryptography-implementation.openssl.tracing-tls-handshakes-with-s-client
name: tracing-tls-handshakes-with-s-client
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, s-client-trace, s-client, tls-debugging, keylogfile, sslkeylogfile, handshake-trace, tls-extensions]
level: practitioner
status: docs-checked
description: "Debug TLS handshakes with s_client -msg, -trace, -state, -tlsextdebug, -status and -keylogfile, and read the output to pinpoint negotiation failures."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man3/SSL_get_error/", "https://github.com/openssl/openssl/blob/master/crypto/err/openssl.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracing TLS handshakes with s_client

## Flags
| Flag | Shows |
|---|---|
| `-state` | SSL session states (where it stopped) |
| `-msg` | Protocol messages, with a hex dump |
| `-trace` | Verbose decoded trace output of protocol messages |
| `-tlsextdebug` | Hex dump of any TLS extensions received from the server |
| `-status` | OCSP stapled response |
| `-keylogfile keys.log` | Appends TLS secrets to a keylog file so external programs such as Wireshark can decrypt the connection |
| `-brief` | A brief summary of connection parameters instead of the normal verbose output |

```
openssl s_client -connect host:443 -servername host -trace -tlsextdebug -status </dev/null 2>&1 | less
openssl s_client -connect host:443 -servername host -keylogfile keys.log </dev/null
```

## Reading a failure
1. Find the last message sent and the alert that ended the handshake (the trace names the alert, for example a fatal
   handshake failure).
2. Compare the ClientHello offers (`supported_groups`, `signature_algorithms`, `cipher_suites`, ALPN) with what the
   server chose or rejected.
3. Typical patterns:
   - Alert right after ClientHello: no common version, cipher or group (try `-tls1_2`, `-groups`, `-cipher`).
   - HelloRetryRequest then failure: server wants a group you listed in supported_groups but cannot do.
   - Failure after Certificate: verification (check `Verify return code`).
   - `unexpected eof while reading`: the peer closed the connection without a close_notify alert (since OpenSSL 3.0
     this is reported as an SSL error with that reason).

## Decrypting with Wireshark
Point Wireshark's TLS settings at the keylog file (see Wireshark's documentation), then open the capture. Delete key logs
afterwards; they contain secrets that decrypt the session.

## Verify
- [ ] You can name the exact message and alert where a failing handshake stops.
- [ ] Decrypted capture shows HTTP inside TLS for a test session.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1): `-state`, `-msg`, `-trace`, `-tlsextdebug`, `-status`, `-keylogfile`, `-brief` descriptions; SSL_get_error(3) and crypto/err/openssl.txt for the `unexpected eof while reading` reason (SSL_R_UNEXPECTED_EOF_WHILE_READING, since 3.0). Removed the build-flag requirement for `-trace`, the sample alert line and the Wireshark menu path, which were not checked.

Method: documentation only; no commands were run.
