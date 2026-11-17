---
id: computing-software.cryptography-implementation.crypto-libraries.golang-x-crypto-packages
name: golang-x-crypto-packages
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, x-crypto, golang, argon2, bcrypt, chacha20poly1305, xchacha20poly1305, golang-ssh, autocert, go-crypto]
level: practitioner
status: verified
description: "Use golang.org/x/crypto safely: argon2.IDKey, bcrypt limits, chacha20poly1305 and XChaCha, ssh, acme/autocert, and which packages moved into the standard library."
sources: ["https://pkg.go.dev/golang.org/x/crypto", "https://pkg.go.dev/golang.org/x/crypto/argon2", "https://pkg.go.dev/golang.org/x/crypto/bcrypt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# golang.org/x/crypto packages

## Password hashing
```go
import "golang.org/x/crypto/argon2"
key := argon2.IDKey([]byte(password), salt, 2, 64*1024, 4, 32)   // time, memory KiB, threads, keyLen
```
No PHC string helper: encode `$argon2id$v=19$m=65536,t=2,p=4$<b64 salt>$<b64 key>` yourself (RawStdEncoding; `argon2.Version`
is 19) and compare with `subtle.ConstantTimeCompare` (all run against x/crypto v0.58.0).

```go
import "golang.org/x/crypto/bcrypt"
h, err := bcrypt.GenerateFromPassword(pw, 12)      // returns ErrPasswordTooLong above 72 bytes
err = bcrypt.CompareHashAndPassword(h, pw)
```

## AEAD
```go
import "golang.org/x/crypto/chacha20poly1305"
aead, _ := chacha20poly1305.NewX(key)              // 24-byte nonce: random nonces safe
nonce := make([]byte, aead.NonceSize()); rand.Read(nonce)
ct := aead.Seal(nonce, nonce, plaintext, ad)       // nonce || ciphertext || tag
```
`chacha20poly1305.New` is the RFC 8439 12-byte nonce variant.

## SSH
`golang.org/x/crypto/ssh`: never use `ssh.InsecureIgnoreHostKey()` outside tests; use
`knownhosts.New(path)` (give it a real path; `~` is not expanded) or `ssh.FixedHostKey(pub)` as `HostKeyCallback`. v0.58.0
exports `ssh.KeyExchangeMLKEM768X25519` (`mlkem768x25519-sha256`); keep the module updated.

## ACME
`golang.org/x/crypto/acme/autocert` provides automatic Let's Encrypt certificates for `tls.Config.GetCertificate`;
set `HostPolicy: autocert.HostWhitelist(...)` and a persistent `Cache` (`autocert.DirCache`) or you will hit rate
limits.

## Moved into the standard library (prefer std)
`crypto/hkdf`, `crypto/pbkdf2`, `crypto/sha3` (Go 1.24), `crypto/mlkem` (Go 1.24), `crypto/ecdh` (1.20). The x/crypto
versions remain for compatibility; std versions are covered by Go's FIPS 140-3 module.

## Deprecated or frozen
`x/crypto/openpgp` (its godoc says `Deprecated: this package is unsafe by design`; the maintained fork is
`github.com/ProtonMail/go-crypto/openpgp`), `blowfish`, `cast5`, `md4` and `ripemd160` (all carry `Deprecated:` notices in their
godoc). `x/crypto/nacl` has no deprecation notice.

## Verify
- [ ] `go list -m golang.org/x/crypto` is current; `govulncheck ./...` clean.
- [ ] No `InsecureIgnoreHostKey` in non-test code.
