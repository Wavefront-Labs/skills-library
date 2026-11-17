---
id: computing-software.cryptography-implementation.applied-cryptography.rejecting-custom-and-nonstandard-crypto
name: rejecting-custom-and-nonstandard-crypto
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, custom-crypto-rejection, home-grown-crypto, rolling-your-own, xor-obfuscation, crypto-review]
level: practitioner
status: docs-checked
description: "Spot and reject home-grown or nonstandard cryptography in reviews: unpublished or invented algorithms, custom modes, and what to ask for instead."
sources: ["https://www.schneier.com/crypto-gram/archives/1998/1015.html", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/327.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rejecting custom and nonstandard crypto

## Red flags
- Algorithm names you cannot find in NIST, IETF RFCs or ISO standards ("proprietary 512-bit cipher").
- A cipher whose design is kept secret or that nobody outside the vendor has published or attacked. Schneier's
  rule: ciphers that are not published are most often very weak, and a cipher that must stay secret to be secure
  is useless once widely used.
- Hand-rolled modes: ECB per block plus custom chaining. OWASP says ECB should not be used outside very specific
  circumstances.
- Custom algorithms in general: the OWASP Cryptographic Storage Cheat Sheet's entire guidance on them is "Don't
  do this."

## What to ask for instead
- A small number of well-understood, heavily studied algorithms, used through a maintained library (CWE-327
  extended description).
- For encryption of data, an authenticated mode; OWASP names GCM and CCM as the first preference.
- For RSA encryption, RSAES-OAEP as in RFC 8017 section 7.1 from a maintained library; prepending random bytes is
  not a substitute, and RSA without an encryption padding scheme must not be used.

## Review response
Classify as CWE-327, "use of a broken or risky cryptographic algorithm or protocol". Per CWE-327, a non-standard
or known-insecure algorithm is dangerous because a determined adversary may break it. Require replacement before
release rather than a compensating mitigation. If a legacy format must still be read, isolate decrypt-only support
and re-encrypt on read (this last step is a recommended practice, not from the cited pages).

## Verify
- [ ] Every primitive in the design maps to a published standard.
- [ ] No algorithm in the design depends on its details staying secret.

## Checked
Method: docs-checked 2026-11-09 against the full Schneier Crypto-Gram 1998-10-15 page, the OWASP Cryptographic Storage Cheat Sheet (Custom Algorithms, Cipher Modes, Random Padding sections) and the CWE-327 description and extended description. Dropped as unconfirmed: the XOR/base64/rot, hash(key||msg), custom-handshake and rand() red flags, the replacement table (ChaCha20-Poly1305, HMAC, TLS 1.3/Noise/HPKE, Argon2id, Ed25519), and the Semgrep/CodeQL checks.
