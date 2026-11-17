---
id: computing-software.software-engineering.ocaml.cryptography-and-secure-randomness
name: cryptography-and-secure-randomness
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, crypto-randomness, mirage-crypto, digestif, secure-random, constant-time]
level: advanced
status: docs-checked
description: "Use the mirage-crypto packages for ciphers, AEAD, public-key crypto and the Fortuna RNG; seed the RNG before use."
sources: ["https://github.com/mirage/mirage-crypto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crypto in OCaml

```ocaml
(* libraries: mirage-crypto mirage-crypto-rng *)
let () = Mirage_crypto_rng_unix.use_default ()   (* seed the RNG, per the README *)
```

## Notes
- mirage-crypto is a small library emphasising applicative style and ease of use. It includes AES, 3DES, RC4, ChaCha20/Poly1305, AEAD (AES-GCM, AES-CCM, ChaCha20/Poly1305), RSA, DSA, DH, elliptic curves (NIST P-256, P-384, P-521, curve 25519) and the Fortuna RNG.
- Packages (each installable with `opam install`): `mirage-crypto` (symmetric ciphers), `mirage-crypto-ec` (elliptic curves, fiat-crypto primitives), `mirage-crypto-pk` (RSA, DSA, DH; uses zarith with GMP), `mirage-crypto-rng` (Fortuna, HMAC-DRBG), plus `-rng-mirage` and `-rng-mkernel` for unikernel entropy.
- RSA timing attacks are countered by blinding; AES timing attacks are avoided by delegating to AES-NI.
- On Unix the RNG uses `getrandom()` (and `getentropy()`) or `/dev/urandom`.
- If the RNG fails with `Fatal error: exception Unseeded_generator`, seed it with `Mirage_crypto_rng_unix.use_default ()` (README; the `mirage-crypto-rng.unix` library).
- Licences: mostly ISC; `mirage-crypto-rng` and `-rng-mirage` are 2-clause BSD; `mirage-crypto-ec` is MIT.

## Self-check
- [ ] Tokens come from the seeded crypto RNG, not the standard `Random` module.

## Checked

2026-11-08. Read in full: the mirage-crypto README.
Removed: digestif, Eqaf constant-time comparison, password-KDF advice, Random/Hashtbl.hash/Digest warnings, `generate 12` nonce call (not in the cited page); ocaml.org sources.
Method: documentation only; no commands were run.
