---
id: computing-software.cryptography-implementation.protocol-implementation.noise-psk-modifiers-and-prologue
name: noise-psk-modifiers-and-prologue
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, noise-psk, noise-protocol, prologue, wireguard, pre-shared-key, handshake]
level: advanced
status: docs-checked
description: "Use Noise psk modifiers and prologue correctly: psk0 to psk2 placement, PSK mixing rules, binding context with the prologue, and WireGuard's IKpsk2 as reference."
sources: ["https://noiseprotocol.org/noise.html", "https://www.wireguard.com/protocol/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noise psk modifiers and prologue

## psk modifiers
- A `psk` token is placed by a pattern modifier: `psk0` puts it at the start of the first handshake message, and
  `psk1`, `psk2`, ... put it at the end of the first, second, ... message. Example protocol name used by WireGuard:
  `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s`.
- A `psk` token is processed with `MixKeyAndHash(psk)`, where psk is a 32-byte secret supplied by the application.
  The token can appear in message patterns only, not pre-messages.
- In a PSK handshake every `e` token is followed by `MixKey(e.public_key)`, so PSK-derived keys are randomised by
  ephemeral public keys.
- Validity rule: a party must not send encrypted data after processing a `psk` token unless it has previously sent an
  ephemeral public key (`e`), either before or after the `psk` token.
- Placement: the spec notes psk1 is recommended for pattern X, because X sends the initiator's static key and the
  responder likely cannot know the (pairwise) PSK until it has decrypted that key.
- WireGuard uses IKpsk2 and describes its pre-shared key as an optional extra layer of symmetric-key cryptography
  (for example for post-quantum resistance); with it unused the PSK is 32 zero bytes.
- Use a high-entropy 32-byte secret, not a password.

## Prologue
- Arbitrary bytes, possibly empty, that both parties hash into `h` at initialisation (`MixHash(prologue)`). If the
  prologues differ, the handshake fails with a decryption error.
- Use it to confirm a shared view of negotiation that happened before the handshake, for example the list of Noise
  protocols one side offered (downgrade protection).
- Prologue data is hashed, not mixed into encryption keys. Secret data meant to strengthen the encryption belongs in
  a PSK handshake instead.
- The prologue is not transmitted by Noise; each side must construct the same bytes.

## Pitfalls
- Using the same PSK for many peers: any holder can impersonate others to anyone sharing it.
- Changing PSKs requires coordination; carry a key identifier outside the handshake if you rotate.

## Verify
- [ ] A mismatched prologue and a wrong PSK both fail the handshake; test vectors for your pattern pass.

## Checked
2026-11-01. Confirmed against the Noise Protocol Framework specification (sections 5 to 9: prologue, pattern
modifiers, PSK handling, psk0/psk1 placement, validity rule, MixKeyAndHash, MixKey after e) and the WireGuard protocol
page (IKpsk2 construction name, optional PSK, all-zero default). Removed: the claim that earlier psk placement
protects more of the handshake, and the advice to use a PAKE for passwords (not in these sources).
Method: documentation only; no commands were run.
