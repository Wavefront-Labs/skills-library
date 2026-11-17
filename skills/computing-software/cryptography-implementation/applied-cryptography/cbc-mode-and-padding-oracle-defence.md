---
id: computing-software.cryptography-implementation.applied-cryptography.cbc-mode-and-padding-oracle-defence
name: cbc-mode-and-padding-oracle-defence
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, block-cipher-modes, sp-800-38a, cbc-padding-oracle, cbc, pkcs7, padding-oracle, encrypt-then-mac, hmac, iv]
level: advanced
status: docs-checked
description: "Operate CBC safely where you must keep it: unpredictable IVs per SP 800-38A, encrypt-then-MAC ordering per RFC 7366, and no distinguishable padding errors."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://datatracker.ietf.org/doc/html/rfc7366"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CBC mode without a padding oracle

New designs should use an AEAD. Keep CBC only for interop (legacy file formats, TLS CBC suites, old
APIs), and then wrap it as below.

## Rules

1. **IV**: for CBC, SP 800-38A Appendix C requires the IV to be unpredictable: for any given plaintext it
   must not be possible to predict the IV before it is generated. The two recommended methods are
   (a) apply the forward cipher, under the same key used for the encryption, to a nonce that is unique
   to each execution (a counter or message number is fine as the nonce), or (b) generate a random
   block with a FIPS-approved random number generator. The IV need not be secret and may be
   transmitted with the ciphertext. A bare counter used directly as the IV is predictable and
   not allowed. (OFB is different: its IV must be a unique nonce, not unpredictable.)
2. **Padding**: SP 800-38A leaves padding out of scope (Appendix A gives an example method and
   notes padding bits must be removable unambiguously). Pick one unambiguous scheme and apply it
   consistently.
3. **Integrity**: CBC provides none. Add a MAC under a separate key over the header, IV and
   ciphertext. Per RFC 7366 the safer construction is encrypt-then-MAC, `encrypt(data || pad) || MAC`,
   with the MAC covering the entire packet up to the MAC value, rather than TLS's historical
   `encrypt(data || MAC || pad)`, which RFC 7366 says is no longer regarded as secure and has
   been the subject of numerous attacks.
4. **Decrypt order**: verify the MAC (constant-time compare) first; only if it passes, decrypt and
   remove padding. Return one generic error for every failure so padding errors cannot be told
   apart from MAC errors.

Derive the encryption and MAC keys from one master key with a KDF using distinct labels rather
than storing two unrelated keys.

## TLS note
RFC 7366 negotiates encrypt-then-MAC via a TLS/DTLS extension; both sides must have exchanged the
extension, and a server MUST NOT send it when it selects an AEAD cipher suite. Where CBC suites
are unavoidable, negotiate it; otherwise prefer AEAD suites.

## Verify
- [ ] Flip one bit of the IV, ciphertext, tag and header separately; all give the same error.
- [ ] Two encryptions of the same plaintext differ (unpredictable IV).
- [ ] MAC input covers header, IV and ciphertext; MAC key is distinct from the encryption key.
- [ ] No code path calls the unpadding routine before the MAC comparison.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-38A (Appendix A padding, Appendix C IV generation, mode IV requirements; downloaded PDF) and RFC 7366 (introduction, sections 2 and 3). The Vaudenay paper returned 403 and was not read. Removed unconfirmed attack folklore (BEAST, Lucky Thirteen, per-byte query counts), the example code and the Java and HTTP-status specifics.
