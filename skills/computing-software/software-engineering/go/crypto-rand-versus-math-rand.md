---
id: computing-software.software-engineering.go.crypto-rand-versus-math-rand
name: crypto-rand-versus-math-rand
category: computing-software
field: software-engineering
product: go
tags: [go, go-security, go-crypto-rand, crypto-rand, math-rand, tokens]
level: practitioner
status: docs-checked
description: "Generate secrets and tokens in Go with crypto/rand (rand.Text, rand.Read) and keep math/rand/v2 for non-security randomness."
sources:
  - https://pkg.go.dev/crypto/rand
  - https://pkg.go.dev/math/rand/v2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# crypto/rand versus math/rand

**Goal:** unguessable tokens, keys and nonces.

```go
func Token(n int) (string, error) {
    b := make([]byte, n)
    if _, err := rand.Read(b); err != nil { return "", err } // crypto/rand
    return base64.RawURLEncoding.EncodeToString(b), nil
}
// Go 1.24+: crypto/rand.Text() returns a base32 (RFC 4648) string
s := rand.Text()

idx, _ := rand.Int(rand.Reader, big.NewInt(int64(len(words)))) // uniform in [0,max)
```

`crypto/rand.Text` (added in Go 1.24) gives at least 128 bits of randomness and may return longer text in future versions, so do not hard-code its length. `crypto/rand.Int` panics if `max <= 0`.

`math/rand/v2` is documented as suitable for tasks such as simulation but not for security-sensitive work; its outputs might be easily predictable regardless of how it is seeded. Its PCG source is unfit for security, and ChaCha8 is described as resistant to prediction, but for secrets use `crypto/rand`. Use `math/rand/v2` for jitter, shuffles, sampling and tests.

`crypto/rand.Read` fills the slice entirely and never returns an error: it calls `io.ReadFull` on `Reader` and crashes the program irrecoverably if that fails. Since Go 1.26 a secure source is always used and `Reader` is ignored unless `GODEBUG=cryptocustomrand=1` is set (to be removed; tests should use `testing/cryptotest.SetGlobalRandom`).

## Gotchas
- Never derive a secret from `math/rand` or `math/rand/v2`, however it is seeded.
- Reducing random bytes with `%` skews results when the range does not divide evenly; use `crypto/rand.Int` for a uniform value in `[0, max)`.
- Store only hashes of tokens server-side.

## Verify
Check that auth and token code imports `crypto/rand`, not `math/rand`, and unit-test token uniqueness over many samples.

## Checked
2026-11-03. Confirmed on pkg.go.dev/crypto/rand (Read never returns an error and crashes irrecoverably, Text since go1.24.0 with at least 128 bits and base32, Int uniform in [0,max) and panics on max <= 0, Go 1.26 Reader note) and pkg.go.dev/math/rand/v2 (not for security, predictable regardless of seeding, ChaCha8 and PCG). Removed: byte-length thresholds, 43-char/26-char lengths, auto-seeding version history, gosec G404, ConstantTimeCompare advice, "check the return in older versions".
Method: documentation only; no commands were run.
