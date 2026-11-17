---
id: computing-software.cryptography-implementation.crypto-libraries.go-native-fips-140-3-mode
name: go-native-fips-140-3-mode
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, golang, go-crypto, gofips140, fips-140-3, fips-approved-mode, go-cryptographic-module]
level: advanced
status: verified
description: "Build and run Go programs in native FIPS 140-3 mode: GOFIPS140 module versions, GODEBUG fips140=on/only, crypto/fips140.Enabled, and what changes or breaks."
sources: ["https://go.dev/doc/security/fips140", "https://pkg.go.dev/crypto/fips140", "https://go.dev/doc/go1.24"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go native FIPS 140-3 mode

Since Go 1.24 the standard library contains the **Go Cryptographic Module**, a pure-Go set of
FIPS 140-3 algorithms in `crypto/internal/fips140/...`. No cgo and no BoringCrypto. FIPS mode is a build and runtime
choice. It is not supported on OpenBSD, Wasm, AIX and 32-bit Windows (go.dev/doc/security/fips140).

## Select the module version at build time
```
GOFIPS140=v1.0.0 go build ./...      # frozen, submitted module snapshot
GOFIPS140=latest go build ./...      # current tree's module, FIPS mode on by default
go version -m ./app | grep -i fips  # shows GOFIPS140 and DefaultGODEBUG=fips140=on (checked, Go 1.27.3)
```
The default `GOFIPS140=off` builds the current tree with FIPS mode off. Any other value
(`latest`, a version such as `v1.0.0`, or the aliases `inprocess`/`certified`) also makes
`fips140=on` the default GODEBUG for that binary.
A `v1.0.0` build downloads the frozen module into the module cache (`golang.org/fips140@v1.0.0-...`); `go version -m`
then shows `-tags=fips140v1.0` and `GOFIPS140=v1.0.0-<hash>`, and `fips140.Version()` (Go 1.26+) returns `v1.0.0`
(`latest` for the tree module). Check the CMVP database for the validation status of the module version you pick; a
version in process is not yet validated (go.dev/doc/security/fips140 lists the status of each frozen version).

## Turn it on at run time
```
GODEBUG=fips140=on   ./app     # FIPS mode: approved algorithms, self-tests, restricted TLS
GODEBUG=fips140=only ./app     # also make non-approved algorithms return errors or panic
```
or in `go.mod`: `godebug fips140=on`, or `//go:debug fips140=on` in the main package. Check from
code with `crypto/fips140.Enabled()` and log it at startup. The setting cannot change after the program starts, and
the docs call `only` a best-effort testing mode that is not meant for production.

## What changes under fips140=on
- Per go.dev/doc/security/fips140: an integrity self-check at init, known-answer self-tests at init or first use, and
  pairwise consistency tests on generated keys (up to 2x slower for some key types, notable for ephemeral keys).
- `crypto/tls` restricts itself to approved versions, suites, groups and signature algorithms
  (TLS 1.2/1.3, AES-GCM, P-256/P-384, and X25519MLKEM768 only where allowed). In a local test with `fips140=on` a client
  restricted to `X25519` failed (`no supported key exchange methods`), a TLS 1.1 client failed, a default TLS 1.2
  connection used `CurveP256`, and a TLS 1.3 default still negotiated `X25519MLKEM768`.
- `crypto/rand` uses an approved DRBG seeded from the OS.
- In `only` mode (run on Go 1.27.3): `md5.Sum` and `sha1.Sum` panic (`use of MD5 is not allowed in FIPS 140-only mode`),
  X25519 key generation returns an error, `cipher.NewGCM` returns an error (use `NewGCMWithRandomNonce`), and
  `hkdf.Key` with a key shorter than 112 bits is refused. `x/crypto/chacha20poly1305` also returned an error
  (`use of ChaCha20Poly1305 is not allowed`), but `x/crypto` code is never inside the module boundary. P-256 ECDH and
  `NewGCMWithRandomNonce` worked.

## Migrating from BoringCrypto
Go+BoringCrypto (`GOEXPERIMENT=boringcrypto`) is, per go.dev/doc/security/fips140, the previous unsupported mechanism, meant
to be removed, and incompatible with the native mode. The Microsoft build of Go uses its own `systemcrypto` backend by
default, which picks a platform crypto library by build constraints (see the Microsoft Go FIPS docs for the matrix).
Pick one mechanism per binary; native mode needs no cgo and no shared library at run time.

## Testing approach
1. Run the full test suite with `GODEBUG=fips140=only` to find non-approved calls.
2. Replace them: `cipher.NewGCMWithRandomNonce` for random-nonce GCM, `crypto/hkdf`,
   `crypto/pbkdf2`, `crypto/sha3`, `crypto/mlkem` (all stdlib, in-boundary).
3. Ship with `fips140=on`, and alert on `fips140.Enabled() == false` in regulated environments.

## Verify
- [ ] `go version -m` on the deployed binary shows the intended GOFIPS140 version.
- [ ] Startup log records `fips140.Enabled()=true`.
- [ ] Tests pass under `fips140=only`.
