---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-rand-read-and-text
name: go-crypto-rand-read-and-text
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, go-crypto-rand, golang, crypto-rand, csprng, secure-random, tokens, math-rand]
level: practitioner
status: verified
description: "Generate secure random values in Go with crypto/rand: Read, Text, Int and Prime, Go 1.24 failure semantics, and keeping math/rand out of security paths."
sources: ["https://pkg.go.dev/crypto/rand", "https://go.dev/doc/go1.24", "https://pkg.go.dev/math/rand/v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go crypto/rand

## API
```go
import "crypto/rand"

key := make([]byte, 32)
rand.Read(key)                      // Go 1.24+: never returns an error; crashes the program if the OS RNG fails

token := rand.Text()                // Go 1.24+: 26-character base32 string (checked), at least 128 bits; docs say a future
                                    // version may return longer text, so do not hard-code the length

n, err := rand.Int(rand.Reader, big.NewInt(1_000_000))   // uniform in [0, max), no modulo bias
p, err := rand.Prime(rand.Reader, 2048)                    // rarely needed directly
```
Before Go 1.24, check the error from `rand.Read` and treat failure as fatal.

## Sources
`crypto/rand.Reader` uses `getrandom(2)` on Linux, FreeBSD and Solaris, `arc4random` on macOS and OpenBSD, and
`ProcessPrng` on Windows (read from `crypto/internal/sysrand` in the Go 1.27.3 source). In Go's FIPS 140-3 mode it is a
NIST SP 800-90A DRBG, with platform CSPRNG output still mixed in at every Read (go.dev/doc/security/fips140).

## Do not use for security
- `math/rand` ("might be easily predictable regardless of how it's seeded") and `math/rand/v2` (its PCG source is documented as
  unfit for security; the ChaCha8 source is documented as resistant to prediction, but use `crypto/rand` for keys and tokens) are for
  simulations and load balancing; `rand.Seed` patterns are common in old code.
- `rand.Intn` from math/rand for OTPs, tokens, or shuffles that matter is a finding.

```
grep -rn '"math/rand' --include=*.go . | grep -v _test.go
```

## Token formats
- URL-safe: `base64.RawURLEncoding.EncodeToString(b)` for 32 random bytes.
- Human-typable: `rand.Text()` (base32, no padding, case-insensitive alphabet).

## Verify
- [ ] No math/rand imports in packages that create secrets.
- [ ] Tokens are at least 128 bits.
