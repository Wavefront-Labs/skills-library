---
id: computing-software.cryptography-implementation.openssl.expanding-cipher-strings-and-iana-names
name: expanding-cipher-strings-and-iana-names
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-ciphers-v, cipher-name-mapping, cipher-strings, openssl-ciphers, iana-cipher-names, tls12, tls13]
level: practitioner
status: docs-checked
description: "Expand and audit OpenSSL cipher strings with openssl ciphers -v -s -stdname, convert IANA names with -convert, and map TLS 1.2 and 1.3 suites across tools."
sources: ["https://docs.openssl.org/master/man1/openssl-ciphers/", "https://docs.openssl.org/master/man3/SSL_CTX_set_security_level/", "https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expanding cipher strings and IANA names

## See what a string really enables
```
openssl ciphers -v 'ECDHE+AESGCM:ECDHE+CHACHA20:!aNULL:!SHA1'
openssl ciphers -s -v -tls1_2 'DEFAULT'      # -s: only suites consistent with the security level and protocol limits
openssl ciphers -v -stdname 'HIGH'           # adds IANA names (TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384)
openssl ciphers -convert TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256   # IANA -> OpenSSL name
```
`-v` prints the details given by SSL_CIPHER_description(3); `-V` adds the hex suite values.

## TLS 1.3 vs TLS 1.2
- TLS 1.3 suites (`TLS_AES_128_GCM_SHA256` etc.) are set separately with `-ciphersuites` / `SSL_CTX_set_ciphersuites`
  and are combined with the TLS 1.2-and-below list; the classic cipher string does not change them.
- TLS 1.2 names are OpenSSL-specific (`ECDHE-RSA-AES128-GCM-SHA256`); the standard (IANA) names are shown by `-stdname`.

## Name mapping cheat sheet
| IANA | OpenSSL |
|---|---|
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | ECDHE-ECDSA-AES128-GCM-SHA256 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | ECDHE-RSA-AES256-GCM-SHA384 |
| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 | ECDHE-RSA-CHACHA20-POLY1305 |
| TLS_RSA_WITH_AES_128_CBC_SHA | AES128-SHA |
| TLS_AES_128_GCM_SHA256 (1.3) | TLS_AES_128_GCM_SHA256 |

## Auditing
- Diff `openssl ciphers -v` output for the configured string between OpenSSL versions when upgrading.
- `@SECLEVEL=N` (0 to 5) in the string sets the security level; level 2 prohibits RSA, DSA and DH keys under 2048 bits,
  ECC keys under 224 bits, RC4 suites and compression, and signatures using SHA-1 or MD5 are already forbidden from level 1.

## Verify
- [ ] Expanded list contains only ECDHE + AEAD suites for TLS 1.2.
- [ ] Names in non-OpenSSL configs are converted correctly (spot-check with -convert).

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-ciphers(1) and SSL_CTX_set_security_level(3): options `-s`, `-v`, `-V`, `-stdname`, `-convert`, `-tls1_2`, `-ciphersuites`; the `AESGCM` keyword; `@SECLEVEL` range 0 to 5 and the level 1 and 2 restrictions; and the IANA-to-OpenSSL mapping rows in the table (lines for ECDHE-ECDSA-AES128-GCM-SHA256, ECDHE-RSA-AES256-GCM-SHA384, ECDHE-RSA-CHACHA20-POLY1305, AES128-SHA, TLS_AES_128_GCM_SHA256). Removed the sample output line and the third-party lookup site.

Method: documentation only; no commands were run.
