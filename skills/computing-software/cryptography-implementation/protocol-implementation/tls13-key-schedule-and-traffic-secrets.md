---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-key-schedule-and-traffic-secrets
name: tls13-key-schedule-and-traffic-secrets
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-1-3, tls13-key-schedule, hkdf, traffic-secrets, rfc8446]
level: advanced
status: docs-checked
description: "Implement or debug the TLS 1.3 key schedule: HKDF-Extract chain, Derive-Secret labels, transcript hashes, traffic key and IV derivation, and checking against RFC 8448 traces."
sources: ["https://www.rfc-editor.org/rfc/rfc8446", "https://www.rfc-editor.org/rfc/rfc8448", "https://tls13.xargs.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 key schedule and traffic secrets

Use this when writing a TLS/QUIC stack, a protocol that reuses the TLS 1.3 schedule, or a
decryption tool. Production apps should use a vetted library; this is for implementers and debugging.

## The chain (RFC 8446 7.1)
```
             0 (or PSK)
             |
   0 -> HKDF-Extract = Early Secret
             +-> Derive-Secret(., "ext binder" | "res binder", "")   = binder_key
             +-> Derive-Secret(., "c e traffic", ClientHello)        = client_early_traffic_secret
             +-> Derive-Secret(., "e exp master", ClientHello)
             v
       Derive-Secret(., "derived", "")
             |
 (EC)DHE -> HKDF-Extract = Handshake Secret
             +-> Derive-Secret(., "c hs traffic", CH..SH)
             +-> Derive-Secret(., "s hs traffic", CH..SH)
             v
       Derive-Secret(., "derived", "")
             |
   0 -> HKDF-Extract = Master Secret
             +-> "c ap traffic", "s ap traffic"  over CH..server Finished
             +-> "exp master"                    over CH..server Finished
             +-> "res master"                    over CH..client Finished
```
- `HKDF-Extract(salt, IKM)`: the left input is the salt (previous secret after "derived"),
  the right input is the IKM.
- `Derive-Secret(S, Label, Msgs) = HKDF-Expand-Label(S, Label, Transcript-Hash(Msgs), Hash.length)`.
- `HKDF-Expand-Label(S, Label, Ctx, L)` uses info = `uint16 L || uint8 len || "tls13 " + Label || uint8 len || Ctx`.
- "0" means a string of Hash.length zero bytes; "" context means Transcript-Hash of empty = Hash("").

## Traffic keys (7.3)
```
key = HKDF-Expand-Label(secret, "key", "", key_length)   # 16 for AES-128-GCM, 32 for AES-256/ChaCha
iv  = HKDF-Expand-Label(secret, "iv",  "", 12)
nonce = iv XOR (64-bit record sequence number, left-padded to 12 bytes)
```
Sequence numbers start at 0 per key and reset on every key change (handshake -> application,
KeyUpdate).

## Common bugs
- Hashing the wrong transcript: messages are the handshake messages (with 4-byte handshake
  header), not records. After HelloRetryRequest, ClientHello1 is replaced by a synthetic
  `message_hash` message (type 254 || 00 00 Hash.length || Hash(CH1)).
- Forgetting the "derived" step between stages.
- Using SHA-256 when the suite is TLS_AES_256_GCM_SHA384: the hash comes from the cipher suite.
- Label prefix: "tls13 " with a space, prepended by HKDF-Expand-Label; labels are ASCII with no trailing NUL.
- Missing secrets are Hash.length zero bytes, never skipped: with no PSK the Early Secret is HKDF-Extract(0, 0).
- The binder_key label is "ext binder" for external PSKs and "res binder" for resumption PSKs.

## Debugging
- RFC 8448 gives full byte traces (simple 1-RTT, resumed 0-RTT, HelloRetryRequest); unit-test every Derive-Secret.
- tls13.xargs.org walks a full handshake byte by byte, including each derived key.
- A key-log file from a reference client lets Wireshark confirm your secrets match.

## Verify
- [ ] All RFC 8448 intermediate secrets reproduce byte-for-byte.
- [ ] HRR path and SHA-384 suite are tested.
- [ ] Secrets are zeroised after the next stage is derived.

## Checked
Date: 2026-10-31. Confirmed in RFC 8446 section 7.1 and 7.3: the schedule diagram and every label, "tls13 " prefix,
HkdfLabel layout, zero-value rule, Transcript-Hash over messages including type and length but no record headers,
message_hash (254) with 00 00 Hash.length, `[sender]_write_key` and `_write_iv` labels, and the RFC 8448 section list.
Removed: key-log label names and the QUIC label example (not confirmed in the fetched sources).
Method: documentation only; no commands were run.
