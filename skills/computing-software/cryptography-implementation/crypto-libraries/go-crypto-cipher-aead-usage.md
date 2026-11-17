---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-cipher-aead-usage
name: go-crypto-cipher-aead-usage
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, golang, go-crypto, go-cipher-aead, aes-gcm, chacha20poly1305, nonce-management]
level: practitioner
status: verified
description: "Use Go's cipher.AEAD safely: NewGCM and NewGCMWithRandomNonce, XChaCha20-Poly1305, Seal/Open slice aliasing, nonce prefixing and handling Open errors."
sources: ["https://pkg.go.dev/crypto/cipher", "https://pkg.go.dev/golang.org/x/crypto/chacha20poly1305", "https://go.dev/doc/go1.24"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto/cipher AEAD usage (Go)

## AES-GCM with an explicit random nonce
```go
func Encrypt(key, plaintext, aad []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)          // 16/24/32-byte key
    if err != nil { return nil, err }
    aead, err := cipher.NewGCM(block)
    if err != nil { return nil, err }
    nonce := make([]byte, aead.NonceSize())   // 12
    rand.Read(nonce)                          // crypto/rand; Go 1.24+: never returns an error, crashes the program if the OS RNG fails
    return aead.Seal(nonce, nonce, plaintext, aad), nil // nonce || ciphertext || tag
}

func Decrypt(key, blob, aad []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)
    if err != nil { return nil, err }
    aead, err := cipher.NewGCM(block)
    if err != nil { return nil, err }
    ns := aead.NonceSize()
    if len(blob) < ns+aead.Overhead() { return nil, errors.New("decrypt failed") }
    return aead.Open(nil, blob[:ns], blob[ns:], aad)
}
```

## Go 1.24+: let the library manage the nonce
```go
aead, _ := cipher.NewGCMWithRandomNonce(block)
ct := aead.Seal(nil, nil, plaintext, aad)       // nonce generated and prepended for you
pt, err := aead.Open(nil, nil, ct, aad)
```
`NonceSize()` returns 0 and `Overhead()` is 28 (12-byte nonce plus 16-byte tag; checked). The cipher must come from
`aes.NewCipher`. Under `GODEBUG=fips140=only` plain `cipher.NewGCM` returns an error (`use of GCM with arbitrary IVs is
not allowed in FIPS 140-only mode, use NewGCMWithRandomNonce`) and its nil result panics if the error is ignored; this
variant works (checked on Go 1.27.3).

## Long-lived keys and many messages
Random 96-bit nonces allow about 2^32 messages per key. For more, use XChaCha20-Poly1305:
```go
aead, _ := chacha20poly1305.NewX(key)            // golang.org/x/crypto/chacha20poly1305, 32-byte key
nonce := make([]byte, aead.NonceSize())          // 24, safe to pick at random
```
Or derive a per-message/per-file key with HKDF.

## Slice semantics
- `Seal(dst, nonce, plaintext, aad)` **appends** to `dst`. Passing `nonce` as `dst` is the idiom
  for prefixing. To encrypt in place use `plaintext[:0]` as `dst`.
- `Open`: `dst` and ciphertext may overlap exactly (`ct[:0]`) or not at all; partial overlap
  panics with `crypto/cipher: invalid buffer overlap of output and input` (checked).
- Don't reuse the returned slice after mutating the input buffer it aliases.

## Errors
`Open` returns a single opaque error (`cipher: message authentication failed`, checked) for any tag
mismatch. Return a generic error upward, discard any output, and don't log the ciphertext.

## Things to avoid
- `cipher.NewCBCEncrypter`, `NewCTR`, `NewCFBEncrypter` without a MAC: unauthenticated.
- `NewGCMWithTagSize` below 16 (sizes 12 to 16 are accepted; 8 returns `incorrect tag size given to GCM`, checked) and
  `NewGCMWithNonceSize` (the docs call `NewGCM` faster and more resistant to misuse; use these only for compatibility).
- `math/rand` for nonces or keys.

## Verify
- [ ] Tests flip a byte in nonce, ciphertext, tag and AAD and expect `Open` to fail.
- [ ] Nonce strategy is documented (random with message budget, or counter, or XChaCha).
- [ ] Cross-language vector decrypts (a Go `nonce||ct||tag` blob and a `NewGCMWithRandomNonce` blob both decrypted with
      Python `cryptography` `AESGCM(key).decrypt(blob[:12], blob[12:], aad)`, checked).
