---
id: computing-software.networking-hardware-and-wireless.strongswan.encryption-integrity-and-prf-keywords
name: encryption-integrity-and-prf-keywords
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, encryption-algorithms, aead, aes-gcm, chacha20poly1305, prf, integrity]
level: practitioner
status: docs-checked
description: "Reference to strongSwan proposal keywords for encryption, AEAD (aes-gcm, ccm, chacha20poly1305), integrity and PRF algorithms, with deprecation flags and support columns."
sources:
  - https://docs.strongswan.org/docs/latest/config/proposals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# encryption integrity and prf keywords
The proposals page tabulates each keyword with IANA id, IKE and ESP support, and implementing plugins. Support letters: `s` deprecated for security reasons, `x` custom plugin, `b` Botan, `w` wolfSSL, `o` OpenSSL or AWS-LC; for ESP `k`, `m`, `n` mark the Linux kernel versions (2.6, 2.6.33, 4.2).

**Classic encryption (CBC/CTR):** `3des`, `cast128`, `blowfish128/192/256` (all deprecated), `null`, `aes128`, `aes192`, `aes256` (CBC), `aes128ctr`..`aes256ctr`, `camellia128`..`camellia256` and ctr variants.

**AEAD** cannot be combined with classic ciphers in one proposal, no separate integrity algorithm is proposed, and PRFs must be listed explicitly in IKE proposals:
- `aes128gcm16` / `aes128gcm128` style names: GCM with ICV 8, 12 or 16 bytes (`gcm8`, `gcm12`, `gcm16`, with bit-based aliases `gcm64`, `gcm96`, `gcm128`) for 128, 192 or 256-bit keys
- the same pattern for `ccm` (`ccm8`, `ccm12`, `ccm16`), Camellia-CCM, and `aes128gmac` (null encryption with GMAC)
- `chacha20poly1305`

**Integrity:** `md5` and `sha1` (deprecated), `aesxcbc`, `aescmac`, the SHA-2 HMACs (e.g. `sha256`), and AES-GMAC.

**PRFs** are optional in IKEv2 proposals (e.g. `prfsha256`, `prfsha384`); if none is given, the integrity algorithms map to PRFs. With AEAD ciphers PRFs must be included.

## Checked
2026-11-04. Confirmed against the strongSwan Algorithm Proposals page: keyword tables (encryption, AEAD, integrity, PRF), support letters s, x, b, w, o and k, m, n, GCM and CCM ICV aliases, the AEAD and PRF rules. Nothing removed.

Method: documentation only; no commands were run.
