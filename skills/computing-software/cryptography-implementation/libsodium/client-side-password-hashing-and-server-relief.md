---
id: computing-software.cryptography-implementation.libsodium.client-side-password-hashing-and-server-relief
name: client-side-password-hashing-and-server-relief
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, server-relief, client-side-hashing, argon2id, libsodium, password-hashing, opaque]
level: advanced
status: verified
description: "Offload password hashing to clients (server relief) safely: client Argon2id plus server hash of the result, salt retrieval, and why OPAQUE is better."
sources: ["https://doc.libsodium.org/password_hashing/default_phf", "https://www.rfc-editor.org/rfc/rfc9807", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side password hashing and server relief

Server relief moves the expensive memory-hard hash to the client, so servers can use strong parameters without
melting under login load. libsodium.js and mobile bindings make Argon2id feasible on clients.

## Construction
1. Client fetches a per-user salt (`GET /salt?user=...`). Return a deterministic fake salt for unknown users
   (`HMAC(server_key, username)`) to avoid user enumeration.
2. Client computes `h = crypto_pwhash(32, pw, salt, OPS, MEM, ALG_ARGON2ID13)`.
3. Client sends `h` over TLS.
4. Server stores and verifies `crypto_generichash(h)` or a fast hash of `h` (never `h` itself): the
   client-side output is effectively the password; a leaked DB of raw `h` values allows direct login.

## Tradeoffs
- Weak clients (old phones) take seconds with server-grade parameters; pick parameters for the slowest supported
  client, which may be weaker than server-side would be.
- Pre-computation: because the salt is served before authentication, an attacker who can query salts can pre-grind guesses offline before any breach; still requires a
  full Argon2 per guess per user.
- Changing parameters needs a migration protocol.

## Better option
OPAQUE (RFC 9807, July 2025, informational) is an aPAKE with security against pre-computation attacks on server compromise, and it hides the password from the server even during registration (RFC abstract). Prefer it where libraries exist.

## Verify
- [ ] Server never stores client output directly; unknown-user salt responses are indistinguishable.
