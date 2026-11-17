---
id: computing-software.cryptography-implementation.secure-implementation.negative-tests-for-crypto-code
name: negative-tests-for-crypto-code
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, known-answer-tests, negative-testing, tamper-tests, malformed-input, property-based-testing, hypothesis, test-design]
level: practitioner
status: verified
description: "Write the tests crypto code usually lacks: tampering every byte, wrong keys, truncation, replay, wrong AAD/context, malformed encodings, and property-based round-trip tests."
sources: ["https://github.com/C2SP/wycheproof", "https://hypothesis.readthedocs.io/en/latest/", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Negative tests for crypto code

Round-trip tests ("encrypt then decrypt returns the plaintext") pass even
when authentication is completely broken: a code path that skips the tag
check, ignores AAD, or accepts truncated input still round-trips. The tests
that matter assert that bad inputs are **rejected**.

## The minimum set

For an encrypt/decrypt or sign/verify API:

1. **Every-byte tamper**: flip a bit in each byte position of the output
   (header, nonce, ciphertext, tag); every variant must fail.
2. **Truncation and extension**: drop the last byte, drop the tag, append a
   byte, empty input; all fail without exceptions leaking details.
3. **Wrong key** and **wrong key id**: fail; no fallback to "try other keys"
   unless designed.
4. **Wrong context/AAD**: same ciphertext opened with another record id,
   tenant, or purpose fails.
5. **Replay/reorder** (protocols): duplicate and out-of-order messages
   rejected per spec.
6. **Downgrade**: change version/algorithm byte to an older or unknown value;
   must fail, not decrypt via a legacy path.
7. **Malformed encodings**: invalid base64, wrong lengths, non-canonical DER,
   invalid curve points.
8. **Uniform errors**: all of the above produce the same error type/message
   at the API boundary. Raw pyca `AESGCM` does not: a tampered tag raises `InvalidTag` while input too short to hold a nonce raises `ValueError`, so wrap the primitive and map both to one `DecryptError`.

```python
# Run with pyca AESGCM (seal = nonce || ct, DecryptError = InvalidTag): 4 tests passed
import pytest
def test_every_bit_flip_rejected(sealed, key, aad):
    for i in range(len(sealed)):
        for bit in (0x01, 0x80):
            bad = bytearray(sealed); bad[i] ^= bit
            with pytest.raises(DecryptError):
                open_(key, bytes(bad), aad)
```

## Property-based tests

```python
from hypothesis import given, strategies as st
@given(st.binary(max_size=4096), st.binary(max_size=64))
def test_roundtrip_and_context_binding(pt, aad):
    ct = seal(KEY, pt, aad)
    assert open_(KEY, ct, aad) == pt
    with pytest.raises(DecryptError):
        open_(KEY, ct, aad + b"x")
```

Also assert non-determinism where expected (two encryptions of the same
plaintext differ) and determinism where designed (SIV, signatures with
Ed25519).

## Use external vectors

Wycheproof JSON files include `"result": "invalid"` cases (modified tags,
invalid points, malleable signatures); iterate them in a parametrised test.

## Verify

- [ ] Tests for items 1-8 exist for each crypto API boundary.
- [ ] Mutation check: temporarily disable the tag comparison - tests must fail.
- [ ] Wycheproof invalid cases run in CI.
