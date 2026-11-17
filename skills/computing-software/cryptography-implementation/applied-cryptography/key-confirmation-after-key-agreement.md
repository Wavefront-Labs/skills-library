---
id: computing-software.cryptography-implementation.applied-cryptography.key-confirmation-after-key-agreement
name: key-confirmation-after-key-agreement
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, key-confirmation, sp-800-56a, key-agreement, ecdh, mac-tag, finished-message, protocol-design]
level: advanced
status: docs-checked
description: "Add SP 800-56A key confirmation to key-agreement protocols: MacKey derivation, MacData layout, unilateral versus bilateral confirmation, and TLS Finished as model."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/a/r3/final", "https://www.rfc-editor.org/rfc/rfc8446#section-4.4.4", "https://csrc.nist.gov/pubs/sp/800/56/b/r2/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key confirmation after key agreement

Key agreement alone gives each side a key it believes is shared. Key confirmation proves the peer actually derived
the same key (and, with identities in the MAC input, who the peer is).

## SP 800-56A 5.9 construction
1. Run the KDF to derive `MacKey || KeyData` (MacKey first, then the session keys).
2. Party U computes `MacTag_U = MAC(MacKey, MacData_U)` with
   `MacData_U = "KC_1_U" || ID_U || ID_V || EphemPub_U || EphemPub_V {|| Text_U}`.
3. Party V checks it, and for bilateral confirmation sends `MacTag_V` over
   `"KC_2_V" || ID_V || ID_U || EphemPub_V || EphemPub_U`.
4. Destroy MacKey after confirmation; never use it for traffic.

Use an approved MAC (HMAC, AES-CMAC or KMAC); the tag must be at least 64 bits, and the full MAC output is the
simplest choice. Unilateral confirmation uses the label "KC_1_U" or "KC_1_V" for the provider; bilateral uses
"KC_2_U" and "KC_2_V".

## When you need it
- Static-key schemes (one or both parties have long-term DH keys) where the recipient must know the sender holds the
  private key.
- Before using the derived key to protect data that an attacker could otherwise use as an oracle.
- Most modern protocols already include an equivalent: TLS 1.3 `Finished` (HMAC over the transcript with a
  finished key).

## Implementation notes
- Direction labels ("KC_1_U" vs "KC_2_V") prevent reflecting a tag back.
- Include both ephemeral public keys so the tag binds to this exchange.
- Compare tags in constant time; on failure abort and erase all derived keys.

## Verify
- [ ] Changing any transcript element (ID, ephemeral key) causes confirmation to fail.
- [ ] A reflected tag is rejected.
- [ ] MacKey is distinct from all traffic keys and zeroised after use.

## Checked
2026-11-01. Confirmed in NIST SP 800-56A Rev. 3 (PDF, sections 5.9.1 to 5.9.3): MacKey || KeyData split,
MacData layout and the six-byte labels, destroy MacKey, discard all derived material on failure, MacTagBits of
at least 64, approved MACs HMAC, AES-CMAC, KMAC. TLS 1.3 Finished confirmed in RFC 8446 section 4.4.4. Removed:
Noise and SSH claims (not in fetched sources).
Method: documentation only; no commands were run.
