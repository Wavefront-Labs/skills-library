---
id: computing-software.cryptography-implementation.secure-implementation.differential-fuzzing-crypto-libraries
name: differential-fuzzing-crypto-libraries
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, known-answer-tests, differential-fuzzing, cryptofuzz, libfuzzer, oss-fuzz, atheris, cargo-fuzz, test-vectors]
level: advanced
status: draft
description: "Fuzz crypto code by comparing implementations: Cryptofuzz, writing a differential harness (yours vs a reference), parser fuzzing, sanitizers, and running it in OSS-Fuzz/CI."
sources: ["https://github.com/guidovranken/cryptofuzz", "https://llvm.org/docs/LibFuzzer.html", "https://google.github.io/oss-fuzz/", "https://github.com/google/atheris"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Differential fuzzing of crypto code

Crypto bugs often produce wrong-but-plausible output (a carry bug that fails
1 in 2^40 inputs, a bignum edge case) that unit tests never hit. Differential
fuzzing feeds the same random inputs to two implementations and flags any
disagreement; it found dozens of bugs in OpenSSL, Go, BoringSSL, libgcrypt,
and others via Cryptofuzz on OSS-Fuzz.

## Cryptofuzz

Supports many libraries as "modules" (OpenSSL, BoringSSL, libsodium, Botan,
Go, Rust crates, mbedTLS, wolfCrypt, ...). It generates operations (digest,
HMAC, cipher, ECDSA sign/verify, bignum ops) and cross-checks results.

```bash
git clone https://github.com/guidovranken/cryptofuzz && cd cryptofuzz
# build each module per docs/<module>.md with -fsanitize=fuzzer,address, then:
./cryptofuzz --operations=Digest,HMAC,SymmetricEncrypt -max_len=4096 corpus/
```

If you maintain a crypto library, add a Cryptofuzz module.

## Your own differential harness

For application wrappers or a new implementation, compare against a trusted
reference:

```python
# atheris harness: our AEAD wrapper vs pyca reference
import atheris, sys
with atheris.instrument_imports():
    from myapp.crypto import seal_raw, open_raw          # code under test
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    key, nonce = fdp.ConsumeBytes(32), fdp.ConsumeBytes(12)
    aad, pt = fdp.ConsumeBytes(fdp.ConsumeIntInRange(0, 64)), fdp.ConsumeBytes(256)
    if len(key) != 32 or len(nonce) != 12: return
    assert seal_raw(key, nonce, pt, aad) == AESGCM(key).encrypt(nonce, pt, aad)
    assert open_raw(key, nonce, AESGCM(key).encrypt(nonce, pt, aad), aad) == pt
atheris.Setup(sys.argv, TestOneInput); atheris.Fuzz()
```

Equivalents: libFuzzer (C/C++), `cargo fuzz` (Rust), Go native fuzzing
(`go test -fuzz=FuzzX`), Jazzer (Java).

## Also fuzz the parsers

ASN.1/DER, PEM, JWK/JWS, certificate and protocol message parsers are where
memory-safety bugs live. Fuzz with structure-aware inputs (seed corpus of
real certificates/messages) under AddressSanitizer and UndefinedBehaviorSanitizer.

## Running it

- Keep a corpus in the repo; run short fuzzing (5-10 min) on every PR, long
  runs nightly or via OSS-Fuzz / ClusterFuzzLite.
- Every crash or mismatch becomes a regression test vector.
- Seed with Wycheproof and CAVP vectors so the fuzzer starts near edge cases.

## Verify

- [ ] Harness compares against an independent reference implementation.
- [ ] Sanitizers enabled in fuzz builds; parsers fuzzed with realistic seeds.
- [ ] CI runs fuzzing; findings converted to regression tests.
