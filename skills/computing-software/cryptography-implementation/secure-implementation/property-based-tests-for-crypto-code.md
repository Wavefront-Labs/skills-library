---
id: computing-software.cryptography-implementation.secure-implementation.property-based-tests-for-crypto-code
name: property-based-tests-for-crypto-code
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, property-based-crypto-tests, property-based-testing, hypothesis, proptest, go-fuzz, crypto-testing, negative-testing, round-trip]
level: practitioner
status: verified
description: "Write property-based tests for crypto wrappers with Hypothesis, proptest and Go fuzzing: round trips, tamper and wrong-context rejection, nonce uniqueness, signatures."
sources: ["https://hypothesis.readthedocs.io/en/latest/", "https://docs.rs/proptest/latest/proptest/", "https://go.dev/doc/security/fuzz/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based tests for crypto code

Known-answer tests prove the primitive matches the spec; properties prove your wrapper behaves correctly for all
inputs: lengths at boundaries, empty inputs, arbitrary associated data.

## Properties to test
1. **Round trip:** `decrypt(k, encrypt(k, m, ad), ad) == m` for all m, ad (including empty and large).
2. **Tamper rejection:** flipping any single bit of the ciphertext, nonce, tag or header makes decryption fail.
3. **Context binding:** different `ad`, key id or version byte makes decryption fail.
4. **Wrong key:** decryption under another key fails.
5. **Freshness:** two encryptions of the same input differ (nonce/IV uniqueness).
6. **Signatures:** `verify(pk, m, sign(sk, m))` is true; false for any other message or a mutated signature.
7. **Parsers:** arbitrary bytes into `decrypt`/`parse` never crash, hang or return plaintext.

## Python (Hypothesis)
```python
from hypothesis import given, strategies as st
@given(m=st.binary(max_size=4096), ad=st.binary(max_size=64), bit=st.integers(min_value=0))
def test_tamper(m, ad, bit):
    blob = box.encrypt(m, ad)
    assert box.decrypt(blob, ad) == m
    i = bit % (len(blob) * 8)
    bad = bytearray(blob); bad[i // 8] ^= 1 << (i % 8)
    with pytest.raises(DecryptionError):
        box.decrypt(bytes(bad), ad)
```

## Rust (proptest)
```rust
proptest! {
    #[test]
    fn roundtrip(m in proptest::collection::vec(any::<u8>(), 0..4096), ad in any::<Vec<u8>>()) {
        let ct = seal(&key, &m, &ad);
        prop_assert_eq!(open(&key, &ct, &ad).unwrap(), m);
    }
}
```

## Go native fuzzing
```go
func FuzzOpen(f *testing.F) {
    f.Add(validBlob)
    f.Fuzz(func(t *testing.T, b []byte) {
        if pt, err := Open(key, b, ad); err == nil && !bytes.Equal(b, validBlob) {
            t.Fatalf("accepted forged input: %x -> %x", b, pt)
        }
    })
}
```
Run `go test -fuzz=FuzzOpen -fuzztime=60s` in CI nightly (run here with Go 1.22.5 against a stub `Open`; the Python Hypothesis test ran against pyca AESGCM, and the proptest block against the aes-gcm crate with proptest 1).

## Verify
- [ ] All seven properties have tests for every wrapper you own.
- [ ] Fuzzers run in CI with a corpus checked into the repo.
