---
id: computing-software.cryptography-implementation.openssl.openssl-security-levels-and-crypto-policies
name: openssl-security-levels-and-crypto-policies
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cnf, providers, seclevel, crypto-policies, key-too-small, tls-policy]
level: advanced
status: docs-checked
description: "Diagnose and set OpenSSL security levels and distro crypto policies: what SECLEVEL 0-5 forbid, 'ee key too small' errors, RHEL update-crypto-policies and per-app overrides."
sources: ["https://docs.openssl.org/master/man3/SSL_CTX_set_security_level/", "https://docs.openssl.org/master/man1/openssl-ciphers/", "https://github.com/openssl/openssl/blob/master/crypto/err/openssl.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security levels and system crypto policies

OpenSSL refuses keys, signatures and protocols below a configurable **security level**. Distros
raise it centrally, so the same app can work on one image and fail on another.

## The levels (SSL_CTX_set_security_level)
| Level | Strength | Effect (cumulative) |
|---|---|---|
| 0 | none | everything allowed (testing only) |
| 1 | 80-bit | RSA/DSA/DH >= 1024, ECC >= 160, no MD5 MACs, no CCM with a 64-bit tag, no SHA-1/MD5 signatures, TLS 1.0/1.1 and DTLS 1.0 disabled |
| 2 | 112-bit | RSA/DSA/DH >= 2048, ECC >= 224, no RC4, no compression |
| 3 | 128-bit | RSA/DH >= 3072, ECC >= 256, forward secrecy required, session tickets disabled |
| 4 | 192-bit | RSA >= 7680, ECC >= 384, SHA-1 MACs disallowed |
| 5 | 256-bit | RSA >= 15360, ECC >= 512 |
Signatures using SHA-1 and MD5 are forbidden from level 1, and TLS 1.0/1.1 are disabled from level 1, so reaching
such peers needs level 0. The compile-time default level is 2 unless the build sets `-DOPENSSL_TLS_SECURITY_LEVEL`.
Distributions can set the level centrally (config file or policy tooling); read your distribution's documentation for what
it does, which is not covered here.

## Error messages and what they mean
| Error | Cause |
|---|---|
| `ee key too small` | peer/leaf key under the level (e.g. RSA-1024 at level 2) |
| `ca md too weak` | a chain certificate signed with a digest the level rejects |
| `dh key too small` | server's DHE group under the level |
| `no protocols available` / `unsupported protocol` | every protocol version requested is excluded, for example TLS 1.0/1.1 at level >= 1 |
| `legacy sigalg disallowed or unsupported` | the signature algorithm is legacy or not allowed at this level |
Fix the peer (rotate the key, reissue the cert). Lowering the level is a temporary exception.

## Distribution crypto policies
Some distributions manage TLS settings system-wide through policy tooling that generates the OpenSSL settings. Those
tools and their file locations are not part of OpenSSL and are not covered here; check your distribution's
documentation before changing anything, and prefer the scoped overrides below.

## Scoped overrides (prefer these to system-wide downgrades)
- Cipher string: `DEFAULT@SECLEVEL=1` in the app's TLS config (`@SECLEVEL=n` is accepted anywhere in an OpenSSL cipher
  string).
- C: `SSL_CTX_set_security_level(ctx, 1)` on the one context that talks to the legacy peer.
- An app-specific `OPENSSL_CONF` that includes the system config and overrides `system_default`.
Document every exception with the peer, the reason and a removal date.

## Raising the level
Before moving services to level 3: inventory RSA-2048 certificates (level 3 prohibits RSA keys under 3072 bits), DH groups,
and partner endpoints. Test with
`openssl s_client -connect peer:443 -cipher DEFAULT@SECLEVEL=3`.

## Verify
- [ ] Each environment's effective level/policy is known (the config file or your distribution's policy tool).
- [ ] Every downgrade exception is per-connection, documented and dated.
- [ ] No SHA-1-signed or RSA-1024 certificates remain in your own PKI.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in SSL_CTX_set_security_level(3): level 0 to 5 descriptions and key-size thresholds (1024/160, 2048/224, 3072/256, 7680/384, 15360/512), the level 1 prohibition of SHA-1 and MD5 signatures and TLS 1.0/1.1, level 3 forward secrecy and disabled tickets, level 4 SHA-1 MACs, and the compile-time default of 2 (`OPENSSL_TLS_SECURITY_LEVEL`); the SSL error reason strings `ee key too small`, `ca md too weak`, `dh key too small`, `no protocols available`, `unsupported protocol` and `legacy sigalg disallowed or unsupported` in crypto/err/openssl.txt; and `@SECLEVEL` in openssl-ciphers(1). Corrected the claim that level 1 is the upstream default. Removed the RHEL and Debian specifics, which could not be read from public documentation.

Method: documentation only; no commands were run.
