---
id: computing-software.cryptography-implementation.protocol-implementation.opaque-asymmetric-pake
name: opaque-asymmetric-pake
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, pake, opaque-pake, rfc9807, oprf, password-authentication, aucpace, server-never-sees-password, ksf]
level: sme
status: docs-checked
description: "Deploy OPAQUE (RFC 9807) so servers never see passwords: registration and login flows, the OPRF and key stretching function, configuration choices, and library options."
sources: ["https://datatracker.ietf.org/doc/html/rfc9807", "https://datatracker.ietf.org/doc/html/rfc9497", "https://github.com/facebook/opaque-ke"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPAQUE asymmetric PAKE

With password-over-TLS login, the server sees every password in plaintext
(logs, memory dumps, TLS-terminating proxies) and stores a hash that can be
attacked offline after a breach. OPAQUE (RFC 9807) is an augmented PAKE:
the server stores a per-user record and never learns the password, and the
RFC cites a proof of security against precomputation attacks.

## How it works (simplified)

- **OPRF**: client blinds the password, server evaluates with a per-client OPRF
  key (derived from a server seed), client unblinds the result. The server
  learns nothing about the password.
- **Key stretching function (KSF)**: the client stretches the OPRF output
  before deriving the randomized password; the RFC names Argon2id, scrypt and
  PBKDF2 as examples.
- **Envelope**: at registration, the client derives keys from the randomized
  password and stores a registration record (client public key, masking key,
  envelope) on the server.
- **Login**: a 3-message AKE (3DH in the RFC) authenticates both sides and
  yields a session key.

## Flows

```
Registration: C -> S RegistrationRequest; S -> C RegistrationResponse;
              C -> S RegistrationRecord (store per user)
Login:        C -> S KE1; S -> C KE2; C -> S KE3; both derive session_key
```

## Configuration choices (must match on both sides)

- OPRF suite: the RFC's examples are ristretto255-SHA512 and P256-SHA256; the
  AKE group SHOULD match the OPRF's group.
- KDF/MAC/hash: per the chosen configuration (for example HKDF-SHA-512,
  HMAC-SHA-512, SHA-512 with ristretto255).
- KSF: chosen by the application with fixed parameters; it runs on the client,
  so budget for low-end devices.
- Context: 3DH can include application-specific context in the transcript;
  bind your application name and version.

## Implementation notes

- Libraries: `opaque-ke` (Rust; its README says an NCC Group audit was
  sponsored by WhatsApp for end-to-end encrypted backups) and
  `@serenity-kit/opaque` (WebAssembly package built on it). Do not implement
  from scratch.
- Prevent client enumeration: for an unknown client, the server SHOULD answer
  the credential request using a fake client record (random masking key),
  ideally created once and stored beside real records, and use the same OPRF
  seed for all clients.
- Registration is not covered by that mitigation: servers react differently to
  registered and unregistered identities, so rate-limit or restrict the
  registration flow.
- Rate-limit login attempts per account; OPAQUE does not stop online guessing.

## Verify

- [ ] Server logs, memory and TLS proxies never contain the password (test with a canary password).
- [ ] RFC 9807 Appendix C test vectors pass for the chosen configuration.
- [ ] Unknown-client responses use a fake record and look like known-client responses.

## Checked

2026-11-01. Confirmed against RFC 9807 and the opaque-ke README: 3DH as a
3-message AKE, ristretto255-SHA512 and P256-SHA256 as OPRF examples, KSF
examples (Argon2id, scrypt, PBKDF2), registration-record contents, fake
client record and shared OPRF seed for enumeration prevention, registration
flow enumeration caveat, Appendix C test vectors, audit sponsored by WhatsApp
for E2EE backups, the @serenity-kit/opaque WASM package. Removed: the claim
that each stolen-database guess costs an online-style evaluation, P-256 as
"FIPS-friendly", "common", "password change = new registration", and the
opaque-ts and bytemare/opaque library names (not in the sources).
Method: documentation only; no commands were run.
