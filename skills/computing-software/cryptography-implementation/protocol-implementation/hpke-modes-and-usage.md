---
id: computing-software.cryptography-implementation.protocol-implementation.hpke-modes-and-usage
name: hpke-modes-and-usage
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, hpke, hybrid-encryption, hpke-modes, rfc9180, mode-base, mode-psk, mode-auth, encapsulated-key, info-parameter, hpke-context-reuse]
level: advanced
status: docs-checked
description: "Use HPKE (RFC 9180) to encrypt to a public key: picking base/psk/auth/auth_psk mode, single-shot vs context APIs, info and AAD binding, and sequence-number limits."
sources: ["https://datatracker.ietf.org/doc/html/rfc9180", "https://github.com/cfrg/draft-irtf-cfrg-hpke", "https://commondatastorage.googleapis.com/chromium-boringssl-docs/hpke.h.html", "https://docs.openssl.org/3.2/man3/OSSL_HPKE_CTX_new/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HPKE modes and usage

HPKE (RFC 9180) is the standard "encrypt to a public key" construction: KEM
(e.g. DHKEM(X25519)) + KDF (HKDF) + AEAD. Use it instead of home-made ECIES-style
hybrids in new protocols (RFC 9180 cites TLS ECH and MLS as users).

## Modes

| Mode | Sender authenticates with | Use |
|---|---|---|
| `mode_base` (0) | nothing (anonymous sender) | Encrypt to a recipient; most common |
| `mode_psk` (1) | pre-shared key | Both hold a PSK |
| `mode_auth` (2) | sender static KEM key | Recipient is assured the sender held that private key |
| `mode_auth_psk` (3) | both | |

For the DHKEM variants in RFC 9180, auth modes are vulnerable to
key-compromise impersonation: the sender assurance fails if the recipient's
private key is compromised. If you need proof of origin, sign instead.

## API shapes

- **Single-shot**: `Seal(pkR, info, aad, pt) -> (enc, ct)`; recipient
  `Open(enc, skR, info, aad, ct)`. One message per encapsulation.
- **Context**: `SetupBaseS(pkR, info) -> (enc, ctx)` then repeated
  `ctx.Seal(aad, pt)`; nonces come from an internal sequence number. Messages
  must be opened in the same order; a lost message desynchronises the context.
  Use only on ordered, reliable channels.

BoringSSL's `hpke.h` exposes `EVP_HPKE_CTX_setup_sender`, `EVP_HPKE_CTX_seal`,
`EVP_hpke_x25519_hkdf_sha256`, `EVP_hpke_aes_128_gcm` and `EVP_HPKE_MAX_ENC_LENGTH`.
OpenSSL 3.2+ has `OSSL_HPKE_CTX_new` / `OSSL_HPKE_encap` / `OSSL_HPKE_seal`.
Libraries differ in how they serialise `enc || ct`; fix
the wire format yourself.

## Binding context

- `info`: application and protocol version, recipient identity, purpose. It
  enters the key schedule, so a ciphertext for one purpose cannot be opened
  for another.
- `aad`: per-message metadata (headers, sequence ids).
- The recipient's public key is bound via the KEM, but include identities in
  `info` if your threat model includes key confusion.

## Limits

Context mode: sequence number is AEAD nonce-sized; the spec errors at overflow.
Practically, cap messages per context and set up a new one.

## Verify

- [ ] RFC 9180 Appendix A test vectors pass for the chosen suite.
- [ ] Wire format of `enc` and ciphertext is specified with lengths.
- [ ] `info` includes app/version/purpose; tampering `info` makes Open fail.
- [ ] Context mode used only on ordered channels.

## Checked

2026-10-31. Confirmed in RFC 9180 (mode identifiers, KCI caveat for auth modes, sequence
number and MessageLimitReachedError, ordering and lost-message rules, Appendix A test
vectors), the BoringSSL `hpke.h` page (function names) and the OpenSSL 3.2 HPKE man page
(function names). Removed: the C code sample (argument order unchecked), the Go and Rust
library claims, the Oblivious HTTP and sealed-box claims, and the PSK post-quantum claim.

Method: documentation only; no commands were run.
