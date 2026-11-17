---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-ecdh-and-ed25519
name: go-crypto-ecdh-and-ed25519
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, go-ecdh, golang, crypto-ecdh, ed25519, x25519, key-agreement]
level: practitioner
status: verified
description: "Use Go crypto/ecdh for X25519 and NIST ECDH and crypto/ed25519 for signatures: key generation, parsing public keys, converting from crypto/ecdsa, and validation."
sources: ["https://pkg.go.dev/crypto/ecdh", "https://pkg.go.dev/crypto/ed25519", "https://pkg.go.dev/crypto/x509"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go crypto/ecdh and crypto/ed25519

## ECDH (Go 1.20+)
```go
curve := ecdh.X25519()                       // or ecdh.P256(), P384(), P521()
priv, _ := curve.GenerateKey(rand.Reader)
peer, err := curve.NewPublicKey(peerBytes)   // validates encoding and point
if err != nil { return err }
shared, err := priv.ECDH(peer)               // errors on low-order X25519 points: `bad X25519 remote ECDH input: low order point`
key, err := hkdf.Key(sha256.New, shared, salt, "myapp v1 session", 32)   // crypto/hkdf, Go 1.24+
```
- NIST curves take uncompressed points (`0x04 || X || Y`, 65 bytes for P-256); a compressed point from
  `elliptic.MarshalCompressed` is rejected by `NewPublicKey` with `invalid public key` (checked).
- Convert existing keys: `ecdsaPriv.ECDH()` and `ecdsaPub.ECDH()` return crypto/ecdh keys.
- `x509.ParsePKIXPublicKey` returns `*ecdh.PublicKey` for X25519 SPKI (checked).

## Ed25519
```go
pub, priv, _ := ed25519.GenerateKey(rand.Reader)
sig := ed25519.Sign(priv, msg)
ok := ed25519.Verify(pub, msg, sig)
priv2 := ed25519.NewKeyFromSeed(seed32)      // priv.Seed() returns the 32-byte seed
```
- `priv.Sign(nil, digest, &ed25519.Options{Hash: crypto.SHA512})` signs Ed25519ph over a 64-byte SHA-512 digest and
  `ed25519.VerifyWithOptions(pub, digest, sig, &ed25519.Options{Hash: crypto.SHA512})` returns nil on success
  (an `error`, not a bool); `Options.Context` gives Ed25519ctx (both round-trips checked).
- Go's `Verify` decodes S with `SetCanonicalBytes`, so non-canonical S is rejected (read in the Go source);
  see RFC 8032 for the verification equation.

## Pitfalls
- Never use raw `shared` as a key; derive with HKDF including both public keys or a transcript.
- Check `len(pub) == ed25519.PublicKeySize` before `Verify` (it panics with `ed25519: bad public key length`, checked).

## Verify
- [ ] Wycheproof X25519/ECDH/Ed25519 vectors via a test harness, or interop with peer stack.
