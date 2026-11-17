---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-asymmetric-sign-and-verify
name: pyca-asymmetric-sign-and-verify
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, pyca-asymmetric, pyca-cryptography, python, ed25519, ecdsa, rsa-pss, signatures, prehashed]
level: practitioner
status: verified
description: "Sign and verify with pyca/cryptography: Ed25519, ECDSA (DER and raw conversions), RSA-PSS and PKCS1v15, prehashed signing, and exception-based verification."
sources: ["https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/", "https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/", "https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pyca asymmetric sign and verify

## Ed25519
```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature
sk = Ed25519PrivateKey.generate()
sig = sk.sign(b"message")
try:
    sk.public_key().verify(sig, b"message")      # returns None on success
except InvalidSignature:
    reject()
```

## ECDSA
```python
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
sk = ec.generate_private_key(ec.SECP256R1())
der_sig = sk.sign(data, ec.ECDSA(hashes.SHA256()))            # DER
r, s = utils.decode_dss_signature(der_sig)
raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")           # for JOSE/WebCrypto
der_again = utils.encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
sk.public_key().verify(der_sig, data, ec.ECDSA(hashes.SHA256()))
```
Deterministic nonces (RFC 6979): `ec.ECDSA(hashes.SHA256(), deterministic_signing=True)` in cryptography 43.0+ (changelog; the keyword is still `deterministic_signing` on 50.0.2). Without it, two signatures over the same data differ.

## RSA
```python
from cryptography.hazmat.primitives.asymmetric import padding
pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH)
sig = rsa_sk.sign(data, pss, hashes.SHA256())
rsa_sk.public_key().verify(sig, data, pss, hashes.SHA256())
```
`salt_length` is a required argument of `padding.PSS` (omitting it is a `TypeError`). `padding.PSS.MAX_LENGTH` (used in many examples) produces salts other libraries may not expect; use
`DIGEST_LENGTH` for interop. `padding.PKCS1v15()` for legacy verification.

## Prehashed
```python
h = hashes.Hash(hashes.SHA256()); h.update(chunk1); h.update(chunk2)
sig = sk.sign(h.finalize(), ec.ECDSA(utils.Prehashed(hashes.SHA256())))
```
The signature verifies against the full data with `ec.ECDSA(hashes.SHA256())` (checked). It is byte-identical to signing the full data only when `deterministic_signing=True` is set on both; otherwise random nonces make every signature differ. Use for large streams.

## Verify
- [ ] Verification failure raises `InvalidSignature` and the caller treats it as fatal.
- [ ] Raw-format conversion round-trips and verifies in the peer library.
