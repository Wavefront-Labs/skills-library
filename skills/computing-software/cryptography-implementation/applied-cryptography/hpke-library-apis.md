---
id: computing-software.cryptography-implementation.applied-cryptography.hpke-library-apis
name: hpke-library-apis
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ossl-hpke, hpke, rfc-9180, openssl, boringssl, evp-hpke, rust-hpke, api-usage]
level: advanced
status: docs-checked
description: "Call HPKE from OpenSSL (OSSL_HPKE_*), BoringSSL (EVP_HPKE_*) and the Rust hpke crate: suites, encap/seal/open flow and exporter use."
sources: ["https://docs.openssl.org/3.2/man3/OSSL_HPKE_CTX_new/", "https://commondatastorage.googleapis.com/chromium-boringssl-docs/hpke.h.html", "https://docs.rs/hpke/latest/hpke/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPKE library APIs

## OpenSSL 3.2+
```c
OSSL_HPKE_SUITE suite = { OSSL_HPKE_KEM_ID_X25519, OSSL_HPKE_KDF_ID_HKDF_SHA256, OSSL_HPKE_AEAD_ID_AES_GCM_128 };
/* sender */
OSSL_HPKE_CTX *s = OSSL_HPKE_CTX_new(OSSL_HPKE_MODE_BASE, suite, OSSL_HPKE_ROLE_SENDER, NULL, NULL);
size_t enclen = sizeof(enc);
OSSL_HPKE_encap(s, enc, &enclen, pub, publen, info, infolen);
OSSL_HPKE_seal(s, ct, &ctlen, aad, aadlen, pt, ptlen);
/* recipient */
OSSL_HPKE_CTX *r = OSSL_HPKE_CTX_new(OSSL_HPKE_MODE_BASE, suite, OSSL_HPKE_ROLE_RECEIVER, NULL, NULL);
OSSL_HPKE_decap(r, enc, enclen, priv_evp_pkey, info, infolen);
OSSL_HPKE_open(r, pt2, &pt2len, aad, aadlen, ct, ctlen);
```
- Key generation: `OSSL_HPKE_keygen(suite, pub, &publen, &priv, NULL, 0, NULL, NULL)`.
- Size helpers: `OSSL_HPKE_get_public_encap_size`, `OSSL_HPKE_get_ciphertext_size`.
- Exporter: `OSSL_HPKE_export(ctx, secret, len, label, labellen)`.
- A context keeps internal state (sequence number: `OSSL_HPKE_CTX_get_seq` / `OSSL_HPKE_CTX_set_seq`). Use separate
  contexts for sender and receiver, and call `OSSL_HPKE_decap` only once per context.

## BoringSSL
```c
EVP_HPKE_CTX ctx; EVP_HPKE_CTX_zero(&ctx);
EVP_HPKE_CTX_setup_sender(&ctx, enc, &enc_len, sizeof(enc), EVP_hpke_x25519_hkdf_sha256(),
                          EVP_hpke_hkdf_sha256(), EVP_hpke_aes_128_gcm(), peer_pub, peer_pub_len, info, info_len);
EVP_HPKE_CTX_seal(&ctx, out, &out_len, sizeof(out), pt, pt_len, aad, aad_len);
```
Recipient keys live in `EVP_HPKE_KEY` (`EVP_HPKE_KEY_generate`, `EVP_HPKE_CTX_setup_recipient`).

## Rust
- Rust `hpke` crate (current docs.rs example): `hpke::setup_sender::<Aead, Kdf, Kem>(&OpModeS::Base, &pk, info)`
  returns the encapsulated key and a sender context; then `ctx.seal(msg, aad)`. The receiver calls
  `hpke::setup_receiver::<Aead, Kdf, Kem>(...)`. Signatures changed between crate versions (older releases took a
  random-number generator argument), so match the docs for the version you pin.
- For other languages, check that library's own documentation; this skill did not verify them.

## Gotchas
- Single-shot APIs create a fresh context per message; multi-message use needs to keep the context and send `enc`
  once.
- Mismatched suite IDs give `Open` failures that look like corruption; log the suite on both sides.
- Do not reuse a context after an `Open` failure in streaming protocols; tear down.

## Verify
- [ ] Published HPKE test vectors for your suite pass through the library.
- [ ] Sender and recipient on different libraries interoperate.

## Checked

2026-10-31. Confirmed: OpenSSL 3.2 `OSSL_HPKE_CTX_new` page (every OSSL_HPKE_* prototype used above, with argument order;
suite constants X25519, HKDF_SHA256, AES_GCM_128; separate contexts per role; single `decap` per context; seq getters);
BoringSSL `hpke.h` (`EVP_HPKE_CTX_setup_sender` argument order, `EVP_HPKE_CTX_seal`, `EVP_hpke_x25519_hkdf_sha256`,
`EVP_hpke_hkdf_sha256`, `EVP_hpke_aes_128_gcm`, `EVP_HPKE_KEY_generate`, `EVP_HPKE_CTX_setup_recipient`); docs.rs `hpke`
(`setup_sender`/`setup_receiver` without an RNG argument, `seal`). Fixed: the Rust call no longer takes an `rng`
argument or a fourth type parameter. Removed as unconfirmed: `single_shot_seal`, the Go and Python library notes, and
the RFC 9180 appendix reference.
Method: documentation only; no commands were run.
