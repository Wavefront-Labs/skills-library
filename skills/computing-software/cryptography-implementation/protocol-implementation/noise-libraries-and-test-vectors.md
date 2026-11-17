---
id: computing-software.cryptography-implementation.protocol-implementation.noise-libraries-and-test-vectors
name: noise-libraries-and-test-vectors
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, noise-implementation, noise-protocol, snow, test-vectors, cacophony]
level: advanced
status: docs-checked
description: "Choose and validate Noise protocol libraries: the snow example, protocol name strings, the Noise test-vector format, prologue, message limits and rekey."
sources: ["https://github.com/noiseprotocol/noise_wiki/wiki/Test-vectors", "https://github.com/mcginty/snow", "https://noiseprotocol.org/noise.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noise libraries and test vectors

## Libraries
Rust: `snow`. It tracks Noise spec revision 34, implements all features except the
`fallback` modifier, and has not received a formal audit. For other languages, pick a
library that supports your exact pattern and verify it with the test vectors below.

## Usage shape (snow)
```rust
let mut noise = snow::Builder::new("Noise_NN_25519_ChaChaPoly_BLAKE2s".parse()?)
                    .build_initiator()?;
let mut buf = [0u8; 65535];
noise.write_message(&[], &mut buf)?;     // write first handshake message
noise.read_message(&incoming, &mut buf)?; // read the response
let mut noise = noise.into_transport_mode()?;
```
- Choose a pattern with static keys (for example XX) when peers must be authenticated, and check
  the remote static key against the expected peer key; Noise authenticates keys, your application
  authorises them.
- Both sides must supply the same prologue or the handshake fails; put prior negotiation (such as
  the offered protocol list) in it to stop rollback.
- Nonces are 64-bit counters and every Noise message is at most 65535 bytes. Rekey does not reset
  the nonce, so do a new handshake before 2^64 messages.

## Test vectors
- The Noise wiki defines a JSON vector format (`protocol_name`, prologue, PSKs, static and ephemeral keys,
  `handshake_hash`, and a `messages` list of payload and ciphertext); it lists cacophony, noise-c and
  snow vector sets as examples. Run vectors for every pattern and cipher you enable.
- Interop: run initiator in one library and responder in another.

## Pitfalls
- Libraries differ in supported patterns and modifiers (snow lacks `fallback`); check the full protocol
  name works in all your implementations.

## Verify
- [ ] Vector suite passes; cross-library handshake succeeds for the chosen protocol name.

## Checked

2026-10-31. Confirmed in the Noise specification (65535-byte messages, 64-bit nonce, prologue
behaviour, Rekey leaves n unchanged), the Noise wiki test-vector page (format and example sets) and
the snow README (builder example, spec revision 34, no fallback modifier, no audit). Removed: the
library table for other languages, flynn/noise source, snow-specific method names not on those
pages, the cacophony.txt and snow.txt file names, and the single-use handshake state claim.

Method: documentation only; no commands were run.
