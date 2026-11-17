---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-loading-and-serialising-keys
name: pyca-loading-and-serialising-keys
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, python, pyca-cryptography, pyca-serialization, pem, der, pkcs8, private-key-encryption]
level: practitioner
status: verified
description: "Load and serialise keys with pyca/cryptography: load_pem_private_key, PKCS8 vs TraditionalOpenSSL, encrypted PEM, raw Ed25519/X25519 bytes, OpenSSH and type checks."
sources: ["https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/", "https://www.rfc-editor.org/rfc/rfc5958", "https://www.rfc-editor.org/rfc/rfc7468"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading and serialising keys (pyca/cryptography)

## Loading
```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, ed25519

with open(path, "rb") as fh:
    key = serialization.load_pem_private_key(fh.read(), password=passphrase_bytes_or_None)

if not isinstance(key, ec.EllipticCurvePrivateKey) or key.curve.name != "secp256r1":
    raise ValueError("unexpected key type")       # never assume what a file contains
```
- `load_pem_public_key` (SubjectPublicKeyInfo), `load_der_private_key`, `load_der_public_key`,
  `load_ssh_public_key`, `load_ssh_private_key`.
- A wrong password raises `ValueError`; a missing password for an encrypted key, or a password for an unencrypted key, raises `TypeError` (checked); malformed input raises `ValueError`
  or `UnsupportedAlgorithm`. Treat all as "could not load key" and do not echo the bytes.
- Public key from a certificate: `x509.load_pem_x509_certificate(data).public_key()`.

## Serialising
```python
pem = key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,                     # "BEGIN PRIVATE KEY"
    encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
)
pub = key.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
```
- Prefer `PKCS8` over `TraditionalOpenSSL` ("BEGIN RSA/EC PRIVATE KEY"); PKCS8 is the
  interop format Java and Go read.
- `BestAvailableEncryption` is a curated choice that can change with the OpenSSL version (pyca docs). `PrivateFormat.PKCS8` has no `encryption_builder()`: calling it raises `ValueError` ("only supported with PrivateFormat.OpenSSH and PrivateFormat.PKCS12"). The builder is available for `PrivateFormat.OpenSSH` (`kdf_rounds`) and `PrivateFormat.PKCS12`.
- `NoEncryption()` only when the file is protected by other means (KMS-wrapped, HSM, sealed secret).

## Raw keys (Ed25519, X25519, Ed448, X448)
```python
raw = ed_key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                           serialization.NoEncryption())          # 32-byte seed
ed_key = ed25519.Ed25519PrivateKey.from_private_bytes(raw)
pub_raw = ed_key.public_key().public_bytes_raw()                  # 40.0+ (pyca docs)
```
Raw is what libsodium, Web Crypto "raw" and most JWK `x`/`d` fields carry.

## EC points
`ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), point_bytes)` loads an
uncompressed (0x04...) or compressed SEC1 point and validates it is on the curve.
Serialise with `Encoding.X962` and `PublicFormat.UncompressedPoint`/`CompressedPoint`.

## OpenSSH
`PrivateFormat.OpenSSH` / `PublicFormat.OpenSSH` produce `ssh-ed25519 AAAA...` style keys;
OpenSSH-format encrypted private keys need the `bcrypt` package installed (without it: `UnsupportedAlgorithm: Need bcrypt module`; checked).

## Verify
- [ ] Every load path checks the key type and size after loading.
- [ ] Round trip: serialise then load yields the same public key bytes.
- [ ] No private key is written unencrypted unless an outer protection is documented.
