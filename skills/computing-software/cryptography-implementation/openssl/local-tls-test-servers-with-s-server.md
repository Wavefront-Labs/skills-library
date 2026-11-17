---
id: computing-software.cryptography-implementation.openssl.local-tls-test-servers-with-s-server
name: local-tls-test-servers-with-s-server
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, s-client, tls-testing, s-server, mtls-testing, sni, alpn, client-certificates]
level: practitioner
status: docs-checked
description: "Stand up local TLS test servers with openssl s_server to debug clients: chains, client-cert requests, SNI second certs, ALPN, OCSP stapling and keylog output."
sources: ["https://docs.openssl.org/master/man1/openssl-s_server/", "https://docs.openssl.org/master/man1/openssl-s_client/"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Local test servers with s_server

When a client fails against production, reproduce with a server you fully control. s_server
lets you change one variable at a time.

## Basic HTTPS-ish server
```
openssl s_server -accept 127.0.0.1:8443 -cert leaf.pem -key leaf.key \
  -cert_chain intermediate.pem -www
```
- `-www` answers any GET with a page describing the session (protocol, cipher, client cert).
- `-WWW` serves files from the current directory; `-HTTP` serves files and expects a full
  HTTP response in them.
- Without `-www`/`-WWW` it's an echo server: text typed on either side appears on the other.
- Bind to `127.0.0.1:` explicitly; the default listens on all interfaces.

## Reproduce chain problems
- Omit `-cert_chain` to simulate a missing intermediate.
- `-cert_chain wrong.pem` to simulate a stale intermediate.
- `-build_chain -CAfile bundle.pem` makes s_server build the chain itself.

## Client certificates (mTLS)
```
openssl s_server -accept 8443 -cert srv.pem -key srv.key -CAfile client-ca.pem -Verify 1 -verify_return_error -www
openssl s_client -connect 127.0.0.1:8443 -cert client.pem -key client.key -CAfile srv-ca.pem
```
`-verify 1` requests a client certificate; `-Verify 1` requires one. By default s_server only logs
`verify error` lines for an untrusted or unsuitable client certificate and still completes the handshake
(the manual says errors are displayed for debugging but the command proceeds); add `-verify_return_error` to close the connection on verification errors.
The page from `-www` shows the client cert subject.

## SNI, ALPN, versions
```
openssl s_server -accept 8443 -cert a.pem -key a.key -servername b.example.com \
  -cert2 b.pem -key2 b.key -alpn h2,http/1.1 -tls1_3 -www
```
Clients sending SNI `b.example.com` get `b.pem`; everything else gets `a.pem`. Use
`-tls1_2`, `-no_tls1_3`, `-cipher`, `-ciphersuites`, `-groups` to impersonate an old or
restrictive server.

## Stapling, early data, debugging
- `-status_file ocsp.der` staples a saved OCSP response (`openssl ocsp ... -respout ocsp.der`).
- `-early_data` accepts 0-RTT (s_server refuses it combined with `-www`, `-WWW`, `-HTTP` or `-rev`); `-anti_replay` is on by default.
- `-keylogfile keys.log` writes NSS key log lines so Wireshark can decrypt the capture.
- `-msg` prints every protocol message with a hex dump; `-trace` shows verbose decoded trace output.
- `-naccept 1` exits after one connection (handy in scripts and CI).

## Gotchas
- s_server is a test tool, not a hardened server. Never expose it.
- Keylog files contain secrets for every session; delete them after use.

## Verify
- [ ] The failing client reproduces the production error against s_server with the same chain.
- [ ] Changing one setting (chain, version, client cert) flips the result, isolating the cause.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_server(1): `-accept` default `*:4433`, `-www`/`-WWW`/`-HTTP`, `-cert_chain`, `-build_chain`, `-verify`/`-Verify`, `-cert2`/`-key2`/`-servername`, `-alpn`, `-status_file` (DER), `-early_data` (not with `-www`, `-WWW`, `-HTTP`, `-rev`), `-anti_replay` default on, `-keylogfile`, `-msg`, `-trace`, `-naccept`. Also confirmed that verification errors are displayed but the handshake proceeds unless `-verify_return_error` is used. Removed the build-flag requirement for `-trace`, the version-specific observation and the `-www` page wording, which the manual does not state.

Method: documentation only; no commands were run.
