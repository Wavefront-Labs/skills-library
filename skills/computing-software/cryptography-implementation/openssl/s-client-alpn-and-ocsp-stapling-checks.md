---
id: computing-software.cryptography-implementation.openssl.s-client-alpn-and-ocsp-stapling-checks
name: s-client-alpn-and-ocsp-stapling-checks
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, s-client-alpn, ocsp-stapling, alpn, openssl-s-client, http2]
level: practitioner
status: docs-checked
description: "Check ALPN negotiation and OCSP stapling with openssl s_client: -alpn, -status, reading the output, and confirming the stapled response is fresh and valid."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-ocsp/", "https://github.com/openssl/openssl/blob/master/apps/s_client.c", "https://www.rfc-editor.org/rfc/rfc7301", "https://www.rfc-editor.org/rfc/rfc6066#section-8"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# s_client ALPN and OCSP stapling checks

## ALPN
```sh
openssl s_client -connect host:443 -servername host -alpn h2,http/1.1 </dev/null 2>/dev/null | grep -i alpn
```
- `-alpn` takes a comma-separated protocol list. s_client prints `ALPN protocol: <name>` when one is selected and
  `No ALPN negotiated` otherwise (a server that ignored ALPN or has none configured).
- Try a protocol the server should not support (`-alpn foo`) and compare the result with the server's documentation.

## OCSP stapling
```sh
openssl s_client -connect host:443 -servername host -status </dev/null 2>/dev/null \
  | sed -n '/OCSP response:/,/^---/p'
```
- `-status` sends a certificate status request (OCSP stapling) and prints the server's response if any. With TLS 1.2 and
  below the output starts `OCSP response:`, with `no OCSP response received` when there is no staple; with TLS 1.3 it
  starts `OCSP responses:` and `no responses sent` means no staple. A parsed response shows its status, cert status and
  update times; check that `Next Update` is in the future.
- Some servers staple lazily, so a missing staple on the first connection is worth repeating once (check your server's
  documentation).
- s_client prints the staple but verification options decide whether it fails the handshake. Cross-check revocation
  directly with `openssl ocsp -issuer int.pem -cert leaf.pem -url <OCSP URL from AIA>` (`-issuer` is the current issuer
  certificate, `-url` the responder).

## Combine with protocol checks
```sh
openssl s_client -connect host:443 -servername host -tls1_3 -alpn h2 -status -brief </dev/null
```

## Verify
- [ ] A monitoring check alerts when the expected ALPN protocol is not selected or the staple is missing or near expiry.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1) (`-alpn` comma-separated list, `-status` OCSP stapling request, `-brief`) and openssl-ocsp(1) (`-issuer`, `-url`); the printed strings `ALPN protocol:`, `No ALPN negotiated`, `OCSP response:`, `no OCSP response received`, `OCSP responses:` and `no responses sent` were read in apps/s_client.c on master. Removed the unconfirmed `no_application_protocol` alert claim and the nginx behaviour statement was reduced to a hedge.

Method: documentation only; no commands were run.
