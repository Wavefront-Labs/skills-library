---
id: computing-software.cryptography-implementation.applied-cryptography.deriving-keys-from-key-agreement-shared-secrets
name: deriving-keys-from-key-agreement-shared-secrets
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-derivation, shared-secret-kdf, sp-800-56c, ecdh, x25519, fixedinfo, one-step-kdf, hkdf]
level: advanced
status: docs-checked
description: "Turn an ECDH shared secret into keys per SP 800-56C: one-step versus two-step KDFs, FixedInfo context binding, and the X25519 all-zero check."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/c/r2/final", "https://www.rfc-editor.org/rfc/rfc7748#section-6.1", "https://docs.openssl.org/3.0/man7/EVP_KDF-SS/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deriving keys from a key-agreement shared secret

The raw output Z of a key-agreement scheme is not used as a key directly. Pass
it through a key-derivation method and bind the context so both sides derive
keys for the same session and roles. RFC 7748 says the two parties can use a
key-derivation function that includes K, K_A and K_B (the shared secret and
both public keys) to derive a symmetric key.

## SP 800-56C options

- **One-step KDF**: `K(i) = H(counter || Z || FixedInfo)`, where the
  auxiliary function H is a hash, HMAC (with a salt as the MAC key) or KMAC.
  OpenSSL exposes this as `SSKDF`, taking a secret, `info` (the FixedInfo),
  an optional salt and a MAC choice such as HMAC or KMAC128.
- **Two-step (extract-then-expand)**: randomness extraction with HMAC or
  CMAC produces a key-derivation key, then a PRF-based KDF from SP 800-108
  expands it. SP 800-56C notes that RFC 5869 (HKDF) specifies a version of
  this extract-then-expand procedure using HMAC for both steps. KMAC is not
  specified for the two-step procedure in revision 2.
- If a salt is omitted for HMAC-based extraction, the default salt is an
  all-zero byte string the size of the hash input block, unless the parties
  agreed otherwise.

## FixedInfo / info contents

SP 800-56C defines FixedInfo as context-specific data appropriate for the
key-establishment scheme; it does not change during the derivation and may
include the salt and the requested key length L. It defers the detailed
format and content to SP 800-56A and SP 800-56B (where it used to be called
OtherInfo). Check those documents for the layout your scheme needs.

For the two-step method, every expansion call needs a distinct FixedInfo when
you derive several keys from one key-derivation key.

```python
z = priv.exchange(peer_pub)                            # X25519
if z == bytes(32):                                    # RFC 7748 6.1 all-zero check
    raise ValueError("low-order peer key")
info = enc(b"myproto v1", init_pub, resp_pub)         # context, length-prefixed
k_i2r = HKDF(SHA256(), 32, salt=None, info=info + b"i2r").derive(z)
k_r2i = HKDF(SHA256(), 32, salt=None, info=info + b"r2i").derive(z)
```

## Pitfalls

- Using `Z` (or its x-coordinate) directly as an AES key.
- Hashing `Z` alone with SHA-256: no context binding, one key for both directions.
- Skipping the RFC 7748 check: the X25519 function returns all zeros for
  small-order input points. The RFC says implementations MAY check for this,
  by ORing all output bytes together, to avoid side channels.

## Verify

- [ ] Both sides derive identical keys in an interop test; swapping roles yields different keys.
- [ ] All-zero X25519 shared secrets are rejected.
- [ ] FixedInfo layout is in the protocol spec.

## Checked

Confirmed against SP 800-56C Rev. 2 (PDF read: one-step formula, auxiliary function options, default salt, two-step extraction and SP 800-108 expansion, RFC 5869 note, KMAC restriction, FixedInfo definition), RFC 7748 section 6.1 (all-zero check, KDF including K, K_A, K_B) and the OpenSSL 3.0 EVP_KDF-SS page (SSKDF name, info, salt and MAC parameters). Removed: the X9.63 KDF attribution, the AlgorithmID/PartyUInfo/PartyVInfo field list, the unknown-key-share claim, the ML-KEM remark and the "static-static ECDH" pitfall, none of which those pages state.

Method: docs-checked 2026-11-09 against SP 800-56C Rev. 2 PDF, RFC 7748 text and the OpenSSL EVP_KDF-SS page.
