---
id: computing-software.cryptography-implementation.openssl.s-client-forcing-protocol-versions-and-ciphers
name: s-client-forcing-protocol-versions-and-ciphers
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, s-client, tls-testing, tls-version-probe, cipher-suites, tls-groups, seclevel]
level: practitioner
status: docs-checked
description: "Probe which TLS versions, cipher suites, groups and signature algorithms a server accepts using s_client -tls1_x, -cipher, -ciphersuites, -groups and -sigalgs."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man3/SSL_CONF_cmd/", "https://docs.openssl.org/master/man1/openssl-ciphers/", "https://github.com/openssl/openssl/blob/master/apps/s_client.c", "https://www.rfc-editor.org/rfc/rfc7507"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Forcing protocol versions and ciphers with s_client

## Protocol versions
```
openssl s_client -connect host:443 -servername host -tls1_3 </dev/null
openssl s_client -connect host:443 -servername host -tls1_2 </dev/null
openssl s_client -connect host:443 -servername host -tls1_1 -cipher 'DEFAULT@SECLEVEL=0' </dev/null
```
TLS 1.0/1.1 are disabled at security level 1 and above, and the compile-time default level is 2, so a "failure" there may
be your client. Add `-cipher 'DEFAULT@SECLEVEL=0'` (builds can also omit the old protocols) when proving a server still
accepts them. The `-no_tls1_x` flags are deprecated in favour of `-min_protocol` and `-max_protocol`.

Success prints a line such as `New, TLSv1.2, Cipher is ECDHE-ECDSA-AES128-GCM-SHA256` and `Protocol: TLSv1.2`;
a rejection shows a TLS alert error instead.

## Cipher suites
TLS 1.2 and below use `-cipher` (OpenSSL names); TLS 1.3 uses `-ciphersuites` (colon-separated TLS 1.3 suite names); the two lists are combined:
```
openssl s_client -connect host:443 -tls1_2 -cipher ECDHE-RSA-AES256-SHA384 </dev/null
openssl s_client -connect host:443 -tls1_3 -ciphersuites TLS_CHACHA20_POLY1305_SHA256 </dev/null
```
Enumerate TLS 1.2 acceptance:
```
for c in $(openssl ciphers 'ALL:@SECLEVEL=0' | tr ':' ' '); do
  openssl s_client -connect host:443 -servername host -tls1_2 -cipher "$c" </dev/null >/dev/null 2>&1 \
    && echo "accepted $c"; done
```
This only tests ciphers your OpenSSL build knows (`ALL` means every suite except eNULL). For audit-grade coverage use a
dedicated TLS scanner.

## Groups and signature algorithms
```
openssl s_client -connect host:443 -groups X25519MLKEM768 </dev/null   # hybrid PQ group, OpenSSL 3.5 and later
openssl s_client -connect host:443 -groups P-256 </dev/null
openssl s_client -connect host:443 -sigalgs rsa_pss_rsae_sha256 </dev/null
openssl s_client -connect host:443 -sigalgs ecdsa_secp256r1_sha256 </dev/null
```
Look for the `Peer Temp Key:` line (or `Negotiated TLS1.3 group:`) and `Peer signature type:` in the connection summary.
The first group listed is the one sent as the TLS 1.3 key share, so a server that prefers another group answers with a
HelloRetryRequest.

## Server preference and fallback checks
- Send two ciphers in both orders; if the result changes, the server follows client order.
- `-fallback_scsv` sends TLS_FALLBACK_SCSV; combined with `-tls1_2` against a server that supports TLS 1.3 it should
  be refused with an inappropriate fallback alert (RFC 7507).

## Interpreting results for policy
Map findings against your policy (e.g. TLS 1.2+ only, AEAD-only, ECDHE-only for 1.2). Record the
OpenSSL version used, because its own defaults (security level, default groups) change what you can offer.

## Verify
- [ ] TLS 1.0/1.1 attempts fail even with `@SECLEVEL=0` on the client.
- [ ] Only AEAD suites are accepted for TLS 1.2.
- [ ] The groups you rely on (X25519, P-256, hybrid PQ if deployed) negotiate.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in SSL_CONF_cmd(3) (`-cipher`, `-ciphersuites`, `-groups` with the first group used for the key share and X25519MLKEM768 from 3.5, `-sigalgs`, `-min_protocol`/`-max_protocol`, deprecated `-no_tls1_x`), openssl-s_client(1) (`-fallback_scsv`), openssl-ciphers(1) (`ALL`), SSL_CTX_set_security_level(3) (TLS 1.0/1.1 disabled at level 1, default 2), the `inappropriate fallback` reason string in crypto/err/openssl.txt, and the output lines `New, <proto>, Cipher is`, `Protocol:`, `Peer Temp Key:` and `Peer signature type:` in apps/s_client.c and apps/lib/s_cb.c. Removed the `(NONE)` output, the third-party scanner sources and the downgrade-sentinel claim.

Method: documentation only; no commands were run.
