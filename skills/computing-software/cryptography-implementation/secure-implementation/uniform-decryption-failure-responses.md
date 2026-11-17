---
id: computing-software.cryptography-implementation.secure-implementation.uniform-decryption-failure-responses
name: uniform-decryption-failure-responses
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, padding-oracle, error-oracle, uniform-error-responses, timing-side-channel]
level: practitioner
status: gated
description: "Remove decryption oracles: one error for every failure (padding, MAC, format, length), same status, body, timing and side effects, and implicit rejection for RSA decryption."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://www.iacr.org/archive/eurocrypt2002/23320530/cbc02_e02d.pdf", "https://www.rfc-editor.org/rfc/rfc8446#section-6.2", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-rsa-guidance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uniform decryption failure responses

Any observable difference between failure types turns decryption into an oracle: Vaudenay
padding oracle (CBC), Bleichenbacher/ROBOT (RSA PKCS#1 v1.5), Manger (OAEP), invalid-curve
and JWE oracles. The attacker only needs a yes/no bit per query.

## One failure, everywhere
For every decrypt/verify failure - wrong length, unknown version, bad padding, bad MAC/tag,
invalid key id, deserialisation error after decrypt - the caller observes:
- the same exception type / error code (`DecryptionFailed`),
- the same HTTP status and body (e.g. 400 `{"error":"invalid_request"}`),
- the same headers, connection behaviour (do not close the socket on one failure type only),
- the same side effects (no extra DB write, cache entry or metric label an attacker can see),
- as far as possible, the same timing.

```python
def open_record(blob: bytes) -> bytes:
    try:
        version, key_id, nonce, ct = parse(blob)       # may raise
        return aead_for(key_id).decrypt(nonce, ct, aad(version, key_id))
    except Exception:
        log.info("decrypt failed", extra={"reason_class": "redacted"})
        raise DecryptionFailed() from None             # no chained cause to callers
```
Internal logs may record the detailed reason if logs are not attacker-visible; never in responses.

## Prefer constructions that cannot leak
- AEAD (GCM, ChaCha20-Poly1305) or encrypt-then-MAC: verify the tag first in constant time,
  then decrypt. No padding exists to probe.
- Legacy CBC with MAC-then-encrypt (TLS 1.0-1.2 CBC suites): even uniform errors leak through
  timing (Lucky 13). Migrate rather than patch.

## RSA decryption
- PKCS#1 v1.5 encryption cannot be made reliably safe; remove it. Where you must keep it, use
  implicit rejection: on bad padding return a pseudorandom message derived from the ciphertext
  and key (OpenSSL 3.2 CHANGES: implicit rejection "added and enabled by default" for RSA PKCS#1 v1.5 decryption, returning a random deterministic message instead of an error; TLS 1.2 premaster handling per
  RFC 5246 7.4.7.1), so failure is indistinguishable downstream.
- OAEP: check all conditions with constant-time code and return one error.

## Timing
Uniform messages are useless if failure paths take different time. Avoid early returns
between padding check and MAC check; compare with `hmac.compare_digest`,
`crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`, `MessageDigest.isEqual` (gated: unconfirmed, source is paywalled or blocked) (Java not run here).

## Verify
- [ ] Table test: each failure class produces byte-identical responses.
- [ ] Timing harness (e.g. dudect-style, many samples) shows no class separation.
- [ ] No CBC-without-MAC or PKCS#1 v1.5 decryption remains reachable from untrusted input.
