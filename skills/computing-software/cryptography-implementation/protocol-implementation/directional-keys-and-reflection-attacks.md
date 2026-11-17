---
id: computing-software.cryptography-implementation.protocol-implementation.directional-keys-and-reflection-attacks
name: directional-keys-and-reflection-attacks
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, secure-channel, directional-keys, reflection-attack, key-separation, hkdf, client-write-key, server-write-key]
level: advanced
status: docs-checked
description: "Derive separate keys per direction in a secure channel so messages cannot be reflected back to their sender, as TLS 1.3 and Noise do."
sources: ["https://datatracker.ietf.org/doc/html/rfc8446#section-7.3", "https://noiseprotocol.org/noise.html#the-split-function"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directional keys and reflection attacks

If both peers encrypt with the same key, an attacker can take a message from A to B and send it
back to A. A decrypts it successfully because it is authentic under the shared key, and may act
on its own message. The fix is a separate key set for each direction.

## How real protocols do it

- **TLS 1.3 (RFC 8446 sections 5.3 and 7.3):** the record protection key and IV are derived
  separately for each sender, `[sender]_write_key = HKDF-Expand-Label(Secret, "key", "", key_length)`
  and `[sender]_write_iv = HKDF-Expand-Label(Secret, "iv", "", iv_length)`, from distinct secrets
  such as `client_application_traffic_secret_N` and `server_application_traffic_secret_N`. A
  record is protected with the sender's write key and the per-record nonce is built from the
  sequence number and that sender's write IV. The receiver decrypts with the peer's write key.
- **Noise:** after the final handshake message, `Split()` returns two `CipherState` objects: the
  first for encrypting transport messages from initiator to responder and the second for the
  other direction.

Each side encrypts with its send key and decrypts with its receive key, so a reflected message
fails authentication.

## Roles must be fixed by the protocol

Directional keys need each side to know its role. Noise's `Initialize` takes an `initiator`
boolean for the role, and TLS fixes client and server roles. In symmetric peer-to-peer designs,
assign roles from the handshake rather than from configuration that could be equal on both ends.

## Also separate by purpose

Use distinct HKDF labels for each derived key (as TLS does with "key" and "iv"); do not feed one
derived key to two algorithms.

## Verify

- [ ] Capturing a message and sending it back to its sender fails authentication.
- [ ] The two directions use different keys and different IV or nonce bases.
- [ ] Role assignment derives from handshake position, not configuration.

## Checked

Method: docs-checked 2026-11-09 against RFC 8446 (traffic key derivation and AEAD record protection passages), Noise specification (handshake and Split() sections). Removed: the invented HKDF label strings, WireGuard, the PSK selfie attack paragraph and RFC 9257 mitigation (eprint 2019/347 not readable, RFC 9257 not read), and the per-pair PSK checklist item.
