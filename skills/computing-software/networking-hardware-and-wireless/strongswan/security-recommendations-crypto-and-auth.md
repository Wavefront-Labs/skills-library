---
id: computing-software.networking-hardware-and-wireless.strongswan.security-recommendations-crypto-and-auth
name: security-recommendations-crypto-and-auth
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, security-recommendations, weak-algorithms, pfs, psk, signature-constraints]
level: advanced
status: docs-checked
description: "strongSwan security guidance: weak algorithms to exclude, recommended suites, key strengths, signature scheme constraints, strong PSKs, PFS and IKEv1 aggressive mode risks."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/securityRecommendations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# security recommendations crypto and auth
**Weak, do not use:** encryption des, 3des, cast, blowfish; integrity/PRF md5, sha1; DH groups modp512, modp768, modp1024, modp1024s160, modp1536, modp2048s224, modp2048s256, ecp192. Default proposals propose none of them except 3des and sha1, still common on Windows. Exclude them from explicit `proposals` and `esp_proposals`. Use at least 2048-bit MODP.

**Suggested suites.** `aes128-sha256-modp3072` (NIST 128-bit strength). SHA-1 only for HMACs in IKE or ESP. CNSA: `aes256-sha384-ecp384,aes256gcm16-prfsha384-ecp384`; CNSA 2.0 adds ML-KEM, e.g. `aes256-sha384-sha512-ecp384-ke1_mlkem1024`.

**Certificates.** Prefer them over PSKs. Keep the root CA offline and sign with intermediates. EdDSA is recommended when all peers support it; RSA at least 2048 (3072 end entity, 4096 CA); ECDSA at least 256-bit curves (384 preferred); signatures at least SHA-256.

**Signature constraints** in `remote.auth`: `pubkey-sha256-sha384-sha512`, `ecdsa-sha384`, `rsa-3072-sha256-sha384-sha512`. They also restrict IKEv2 signatures unless disabled with `charon.signature_authentication_constraints` or separated by an `ike:` prefix, e.g. `ike:pubkey-sha384-sha256`.

**PSKs.** Fine if random with enough entropy: `openssl rand -base64 33`. In swanctl.conf a `0s` prefix means Base64 and `0x` hex. Weak IKEv2 PSKs allow active MITM offline attacks, so prefer EAP with a server certificate. Avoid IKEv1 Aggressive Mode with PSK (a PSK hash is sent in the clear).

**PFS.** Add key exchange methods to the ESP or AH proposal; `none` makes it optional. The first IKEv2 Child SA derives keys from IKE key material unless `childless` is used. Since 6.0.2 default ESP/AH proposals include all key exchange methods plus none.

## Checked
2026-11-04. Confirmed against the Security Recommendations page: weak and recommended algorithm lists, suites, certificate key guidance, signature constraints, PSK advice and PFS notes.

Method: documentation only; no commands were run.
