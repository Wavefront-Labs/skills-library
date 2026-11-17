---
id: computing-software.systems-network-administration.pki-tls-administration.cipher-suite-ordering
name: cipher-suite-ordering
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cipher-suite-ordering, pki-cipher-policy, cipher-suites, openssl-ciphers, aead, forward-secrecy, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Build and test cipher strings with openssl ciphers, choose AEAD forward-secret suites and decide server versus client preference."
sources:
  - https://csrc.nist.gov/pubs/sp/800/52/r2/final
  - https://docs.openssl.org/master/man1/openssl-ciphers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cipher suite selection and ordering
Goal: a minimal cipher list that is easy to audit.
```
openssl ciphers -v 'ECDHE+AESGCM:ECDHE+CHACHA20'      # expand to suites
openssl ciphers -s -tls1_2 -v 'HIGH:!aNULL:!kRSA:!3DES'
```
- `-v` prints details per suite; `-s` with `-tls1_2` lists only the suites usable if that protocol were negotiated.
- `+` combines strings as a logical AND (`ECDHE+AESGCM`); `!` deletes suites permanently so they cannot reappear later in the list; `-` deletes but later strings may add them back; a leading `+` moves matches to the end of the list.
- `ECDHE` means authenticated ephemeral ECDH key agreement, `AESGCM` is AES-GCM (the OpenSSL page says these suites are TLS 1.2 only), `CHACHA20` is ChaCha20 suites.
- `!aNULL` removes anonymous suites (vulnerable to man-in-the-middle). `!eNULL` removes no-encryption suites; the OpenSSL page advises including it when you build lists from primitives such as `kRSA` or `aECDSA`.
- `kRSA` selects suites that use RSA key exchange, `3DES` triple DES, `RC4` RC4. Excluding RSA key exchange, 3DES and RC4 leaves ephemeral key exchange and modern ciphers.
- `CBC` is an alias for the CBC-mode suites (TLS 1.2 and earlier only) on the OpenSSL page.
- The default list is `ALL:!COMPLEMENTOFDEFAULT:!eNULL` in normal builds; `DEFAULT` cannot be combined with `+` (`DEFAULT+AES` is invalid).
- TLS 1.3 suites are set separately with `-ciphersuites`; the page's default is `TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256`. A TLS 1.2 cipher list does not change them.
- `@STRENGTH` sorts by key length and `@SECLEVEL=n` sets the security level (0 to 5).
- For compliance, use the suites NIST SP 800-52 Rev. 2 allows for your environment and check your crypto module; read the publication itself for the list.
Verify:
- [ ] The output of `openssl ciphers -v '<your string>'` lists only intended suites.
- [ ] An external scanner of your choice, run against the server, shows only those suites.

## Checked
Confirmed 2026-11-08 against the OpenSSL openssl-ciphers manual page (options, list syntax, strings, defaults, `-ciphersuites`). The NIST SP 800-52r2 link is only a landing page (a summary of 2.6k characters, not the publication), so no NIST claim is made beyond pointing to it. Removed: nginx directives (`ssl_prefer_server_ciphers`, `ssl_ecdh_curve`, `ssl_ciphers`), X25519/FIPS availability, the nmap grading check, EXPORT and SHA-1 MAC items, forward-secrecy/AEAD advice and DHE group-size guidance (none stated on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
