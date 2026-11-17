---
id: computing-software.cryptography-implementation.protocol-implementation.noise-protocol-framework
name: noise-protocol-framework
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, noise-protocol, handshake-pattern, wireguard, xx-pattern, ik-pattern, nk-pattern, cipherstate, symmetricstate, handshakestate, forward-secrecy, key-exchange-protocol]
level: sme
status: docs-checked
description: "Implementing the Noise Protocol Framework for custom secure channels: choosing a handshake pattern (XX/IK/NK), the state-machine API, and identity-hiding trade-offs."
sources: ["https://noiseprotocol.org/noise.html", "https://www.wireguard.com/protocol/", "https://noiseexplorer.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing the Noise Protocol Framework

Noise is **not a single protocol** — it's a framework of composable
handshake patterns that build a secure channel from Diffie-Hellman, AEAD,
and a hash function. WireGuard's protocol is a fixed instantiation of
Noise's `IK` pattern; this skill is for when you're implementing a Noise
pattern directly rather than consuming a complete protocol like WireGuard.

## Pick the handshake pattern by what identities are known when

Noise patterns are named by two letters, initiator first then responder.
For the initiator: `N` (no static key), `K` (static key known to the
responder in advance), `X` (static key transmitted), `I` (static key
immediately transmitted to the responder). For the responder: `N`, `K`
(static key known to the initiator in advance), `X` (transmitted).
- **`NK`:** initiator has no static key (anonymous/ephemeral client),
  responder's static key is known in advance (e.g., a client connecting to
  a server whose public key it already has pinned). One-way
  authentication — the server is authenticated, the client is not.
- **`IK`:** the initiator's static key is sent immediately in the first
  message and the responder's static key is known to the initiator in
  advance. This is the pattern WireGuard uses (its construction string is
  `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s`, IK plus a pre-shared key). The
  spec's identity-hiding section covers what a passive or active attacker
  learns for each pattern; read it before relying on identity hiding.
- **`XX`:** neither party's static key is known in advance; both are
  transmitted during the exchange. Use it when you have no out-of-band way
  to pre-distribute public keys.
- **Choosing wrong is a protocol-design mistake, not a parameter tweak** —
  choose by who knows whose static key before the handshake starts, and
  check the spec's identity-hiding section for the pattern you pick.

## The state machine: HandshakeState → CipherState

Noise implementations expose roughly: a `HandshakeState` object that
processes the handshake messages (mixing keys, running DH operations per
the chosen pattern's token sequence), which upon completion yields a pair
of `CipherState` objects — one for each direction of traffic, each wrapping
an independent AEAD key derived from the completed handshake. Practical
implementation notes:
- **Don't reuse a `HandshakeState` after completion** — once split into
  `CipherState`s, the handshake object has done its job; ongoing
  encrypt/decrypt goes through the `CipherState`s, which each maintain
  their own nonce counter (see
  `computing-software.cryptography-implementation.applied-cryptography.nonce-and-iv-management`
  — Noise mandates a monotonic counter nonce per `CipherState`, so the
  counter-persistence discipline in that skill applies directly here).
- **The two `CipherState`s are directionally asymmetric** — mixing up which
  one encrypts and which one decrypts (an easy copy-paste bug when wiring
  up initiator vs responder code paths) produces ciphertext the peer can't
  decrypt, which is at least a loud failure; the dangerous version of this
  bug is accidentally using the *same* `CipherState` for both directions,
  which reuses nonces across two independent streams and breaks AEAD
  security silently.

## Payload authentication and the handshake hash

Noise's `h` (handshake hash) accumulates a transcript of the entire
handshake and is available after completion — use it as a **channel
binding** value (e.g., bind it into an application-layer authentication
step, "prove you know a secret AND that you're on this specific handshake
instance") to prevent man-in-the-middle relay attacks where an attacker
proxies the Noise handshake itself but can't forge the final binding check.
Skipping this and only relying on the handshake's own authentication is
fine for many use cases, but if your application layer does anything
security-sensitive immediately post-handshake (like confirming a
human-readable fingerprint), bind it to `h`, not just to "the connection
succeeded."

## Verify

- [ ] The chosen handshake pattern matches the actual identity-knowledge
      model (who knows whose static key when) — not picked by copying
      another project's choice without checking the fit.
- [ ] Each `CipherState`'s nonce counter is distinct, monotonic, and never
      shared between the two directions.
- [ ] Initiator/responder `CipherState` direction assignment is verified by
      an actual interop test (encrypt on one side, decrypt on the other),
      not just "it compiles."
- [ ] If application-layer binding to the handshake is needed, it uses the
      handshake hash (`h`), not a separate unbound check.
- [ ] The implementation interoperates with an independent Noise
      implementation for the chosen pattern and cipher suite.

## Checked

2026-11-01. Confirmed against the Noise specification (handshake hash `h`
and its channel-binding use, two `CipherState` objects returned by `Split()`,
initial letter meanings N/K/X/I, 64-bit counter nonce `n`, nonce reuse is
catastrophic, identity-hiding section) and the WireGuard protocol page
(Noise_IK, construction string). Removed: the claim that XX costs an extra
round trip and gives weaker guarantees than IK, and the test-vector claim
(not in the sources). API names vary by binding; see your library's docs.
Method: documentation only; no commands were run.
