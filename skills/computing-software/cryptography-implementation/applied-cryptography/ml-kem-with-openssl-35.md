---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-with-openssl-35
name: ml-kem-with-openssl-35
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, openssl-ml-kem, ml-kem, openssl, openssl-3-5, fips-203, pkeyutl, genpkey, post-quantum]
level: practitioner
status: docs-checked
description: "Generate ML-KEM keys, encapsulate and decapsulate with OpenSSL 3.5 genpkey and pkeyutl, and choose private key storage formats (seed or expanded key)."
sources: ["https://docs.openssl.org/3.5/man7/EVP_PKEY-ML-KEM/", "https://docs.openssl.org/3.5/man1/openssl-pkeyutl/", "https://csrc.nist.gov/pubs/fips/203/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-KEM with OpenSSL 3.5

OpenSSL 3.5 implements the ML-KEM-512, ML-KEM-768 and ML-KEM-1024 key types in its default and FIPS providers.
NIST FIPS 203 (August 2024) specifies the three parameter sets.

## Keys
```
openssl genpkey -algorithm ML-KEM-768 -out mlkem.key
openssl pkey -in mlkem.key -pubout -out mlkem.pub
openssl pkey -in mlkem.key -text -noout
```
Parameter sets: ML-KEM-512, ML-KEM-768, ML-KEM-1024, in increasing security strength and decreasing performance.
Look up key and ciphertext sizes in FIPS 203 before sizing buffers or protocol fields.

## Encapsulate / decapsulate
```
openssl pkeyutl -encap -pubin -inkey mlkem.pub -out ct.bin -secret ss_sender.bin
openssl pkeyutl -decap -inkey mlkem.key -in ct.bin -secret ss_recipient.bin
cmp ss_sender.bin ss_recipient.bin && echo match
```
`-secret` names the shared-secret file; the ciphertext is written to `-out`. Feed the shared secret into a KDF with
context before use; do not use it directly as a data key.

## Private key formats
Internally ML-KEM keys are generated from a 64-byte seed, the concatenation of the 32-byte `d` and `z` values of FIPS 203.
By default OpenSSL retains the seed on generated keys and writes it into PKCS#8 files. The provider settings
`ml-kem.output_formats` / `input_formats` choose among `seed-priv` (seed and expanded key), `seed-only`, `priv-only`
(the FIPS 203 `dk` key) and `bare-seed`; `ml-kem.retain_seed=no` and `ml-kem.prefer_seed=no` change what is kept or
used on import, for example:
```
openssl genpkey -provparam ml-kem.retain_seed=no -algorithm ML-KEM-768 -out dk-only.pem
```
Confirm the format your peers (HSMs, other libraries) can import.

## Gotchas
- Older OpenSSL releases lack these commands: a local OpenSSL 3.2.3 has no ML-KEM in `openssl list -kem-algorithms`
  and its `pkeyutl` has no `-encap`/`-decap`. Check `openssl version`.
- Whether the FIPS provider's ML-KEM is covered by a validated module certificate is a CMVP question; check the
  certificate, not the provider documentation.

## Verify
- [ ] Shared secrets match between encap and decap.
- [ ] The key type you generated is the parameter set your peer expects.
- [ ] The private key file is stored in a format your tooling can re-import.

## Checked

2026-10-31. Confirmed in the OpenSSL 3.5 EVP_PKEY-ML-KEM page (three key types in default and FIPS providers; 64-byte
seed = 32-byte d and z; seed retained by default and written to PKCS#8; formats `seed-priv`, `seed-only`, `priv-only`,
`bare-seed`; `ml-kem.retain_seed`, `ml-kem.prefer_seed`, `output_formats`), the 3.5 openssl-pkeyutl page (`-encap`,
`-decap`, `-secret`) and the NIST FIPS 203 page (three parameter sets). Local read-only checks on OpenSSL 3.2.3: no
ML-KEM listed, no `-encap` option. Removed (not confirmable from readable sources): key/ciphertext/secret byte sizes,
the 2400-byte `dk` size, "LTS", the CNSA 2.0 remark, the `X25519MLKEM768` default-group and `s_client` claims, the
"3.0-3.4 lack ML-KEM" generalisation (only 3.2.3 was checked).
Method: documentation plus the local OpenSSL checks named above.
