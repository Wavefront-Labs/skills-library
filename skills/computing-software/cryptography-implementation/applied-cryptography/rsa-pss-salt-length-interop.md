---
id: computing-software.cryptography-implementation.applied-cryptography.rsa-pss-salt-length-interop
name: rsa-pss-salt-length-interop
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, rsa-pss, pss-salt-length, rsassa-pss, signatures, interoperability, rfc8017, rfc4055]
level: advanced
status: docs-checked
description: "Make RSA-PSS signatures verify across libraries: salt length conventions (digest, max, auto), MGF1 hash, PSS-restricted keys, and TLS 1.3 rules."
sources: ["https://datatracker.ietf.org/doc/html/rfc8017#section-8.1", "https://www.rfc-editor.org/rfc/rfc8446.txt", "https://docs.openssl.org/3.0/man7/EVP_SIGNATURE-RSA/", "https://datatracker.ietf.org/doc/html/rfc4055", "https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/", "https://pkg.go.dev/crypto/rsa"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA-PSS salt length and interop

RSASSA-PSS is the RSA signature padding used for RSA signatures in TLS 1.3
(`rsa_pss_rsae_sha256` etc.). Verification fails when signer and verifier
disagree on salt length or MGF1 hash.

## Parameters

- **Hash**: the message digest (SHA-256, SHA-384 or SHA-512 in TLS 1.3).
- **MGF1 hash**: set equal to the message hash (RFC 8446 requires this for the
  TLS 1.3 PSS algorithms).
- **Salt length**: the usual mismatch. Conventions:
  - `digest` length (32 for SHA-256): TLS 1.3 requires the salt length to equal
    the digest output length. pyca `PSS.DIGEST_LENGTH`, OpenSSL `digest`, Go
    `PSSSaltLengthEqualsHash`.
  - `max` (about k - hLen - 2, with k the modulus length in bytes): pyca
    `PSS.MAX_LENGTH`, OpenSSL `max`. For RSA-2048 with SHA-256 this is 222 bytes.
  - `auto` on verify: OpenSSL `auto` and Go `PSSSaltLengthAuto` detect the
    salt length from the signature (Go signs with the largest salt in that mode).
  - Go in FIPS 140-3 mode caps the salt at the hash length.

A signature made with `max` therefore fails against a verifier pinned to
`digest` (and the reverse). Default to salt = digest length on sign, and
verify with the exact expected length (or `auto` only if you must accept many
signers).

```python
padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH)
```

```bash
openssl dgst -sha256 -sign key.pem -sigopt rsa_padding_mode:pss \
  -sigopt rsa_pss_saltlen:digest -sigopt rsa_mgf1_md:sha256 -out sig.bin data
openssl dgst -sha256 -verify pub.pem -sigopt rsa_padding_mode:pss \
  -sigopt rsa_pss_saltlen:digest -signature sig.bin data
```

Go: `rsa.SignPSS(rand.Reader, k, crypto.SHA256, digest, &rsa.PSSOptions{SaltLength: rsa.PSSSaltLengthEqualsHash})`.

## PSS-restricted keys (`id-RSASSA-PSS`)

An RSA key may be encoded with the `id-RSASSA-PSS` OID (RFC 4055) and
RSASSA-PSS-params that limit the key to PSS. Some tools do not accept such
keys; test every consumer before relying on them. Use ordinary `rsaEncryption`
keys with PSS signatures unless you need the restriction.

## Verify

- [ ] Salt length, MGF1 hash and message hash recorded in the spec.
- [ ] Cross-verify: sign with library A, verify with library B, both ways.
- [ ] Known-answer test vectors for RSA-PSS pass.

## Checked

2026-10-31. Confirmed in RFC 8446 (TLS 1.3 PSS: MGF1 hash equals the digest, salt length equals the digest length;
`rsa_pss_rsae_*` names), RFC 4055 (`id-RSASSA-PSS`, RSASSA-PSS-params), the OpenSSL EVP_SIGNATURE-RSA page (`saltlen`
values `digest`, `max`, `auto`; `mgf1-digest`), the pyca RSA page (`PSS.DIGEST_LENGTH`, `PSS.MAX_LENGTH`) and pkg.go.dev
crypto/rsa (`PSSSaltLengthAuto`, `PSSSaltLengthEqualsHash`, FIPS 140-3 cap). Run locally with OpenSSL 3.2.3 (fresh
RSA-2048 key, SHA-256): the `digest` sign/verify pair above verified OK; a `max` signature failed verification with
`digest` ("expected: 32 retrieved: 222"), and verified OK with salt length 222 and with `auto`. Removed: the FIPS 186-5
salt limit and its compliance claim (NIST page is abstract only), old Java/BC defaults, the Java snippet, `PSS.AUTO`,
numeric `-1`/`-2` OpenSSL values, the keytool/browser/HSM compatibility list, the Wycheproof vector name.
Method: documentation plus the local OpenSSL runs named above.
