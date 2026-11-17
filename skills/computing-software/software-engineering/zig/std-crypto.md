---
id: computing-software.software-engineering.zig.std-crypto
name: std-crypto
category: computing-software
field: software-engineering
product: zig
tags: [zig, std-crypto, zig-security, sha256, blake3, hmac, chacha20poly1305, ed25519, argon2, timing-safe]
level: advanced
status: docs-checked
description: "Use std.crypto for SHA-2/3, Blake3, HMAC, AES-GCM, ChaCha20-Poly1305, Ed25519, argon2 and constant-time comparison in Zig."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto/hmac.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto/sha2.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto/chacha20.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto/timing_safe.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fmt.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.crypto: hashing, AEAD, signatures and randomness
**Goal:** safe crypto calls with the std primitives.

```zig
var digest: [32]u8 = undefined;
std.crypto.hash.sha2.Sha256.hash("data", &digest, .{});
const hex = std.fmt.bytesToHex(digest, .lower);

var mac: [32]u8 = undefined;
std.crypto.auth.hmac.sha2.HmacSha256.create(&mac, msg, key);

const Aead = std.crypto.aead.chacha_poly.ChaCha20Poly1305;
var nonce: [Aead.nonce_length]u8 = undefined;
std.crypto.random.bytes(&nonce);
Aead.encrypt(ct[0..msg.len], &tag, msg, ad, nonce, key);
try Aead.decrypt(out, ct, tag, ad, nonce, key);        // error.AuthenticationFailed on tamper

const ok = std.crypto.timing_safe.eql([32]u8, a, b);   // constant-time compare
```
- Ed25519: `std.crypto.sign.Ed25519`; password hashing: `std.crypto.pwhash.argon2` / `bcrypt` / `scrypt` with explicit params and allocator.
- Key exchange: `std.crypto.dh.X25519`; TLS client in `std.crypto.tls`.
- Random: always `std.crypto.random` for secrets.

## Gotchas
- Never reuse a nonce with the same key for ChaCha20-Poly1305 or AES-GCM.
- `std.mem.eql` on MACs is not constant time.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `hash.sha2.Sha256.hash(bytes, &out, .{})`, `auth.hmac.sha2.HmacSha256.create`, `aead.chacha_poly.ChaCha20Poly1305` `encrypt`/`decrypt` signatures and `error.AuthenticationFailed`, `nonce_length`, `timing_safe.eql`, `sign.Ed25519`, `pwhash.argon2/bcrypt/scrypt`, `dh.X25519`, `crypto.tls`, `crypto.random`, `fmt.bytesToHex(input, .lower)`. Removed: the audit-status claim and the release-drift remark.

Method: documentation only; no commands were run.

## Self-check
Hash "abc" with SHA-256 and compare to ba7816bf...15ad (known vector).
