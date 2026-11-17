---
id: computing-software.game-programming.multiplayer-networking.connect-tokens-and-packet-encryption
name: connect-tokens-and-packet-encryption
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, server-authority, connect-token, packet-encryption, netcode-io, aead, libsodium, dtls, dedicated-server-security, replay-protection, game-programming, replay-attack]
level: advanced
status: draft
description: "Secure UDP game servers: backend-issued connect tokens, AEAD packet encryption with per-session keys, replay protection, and challenge handshakes (netcode.io model)."
sources: ["https://gafferongames.com/post/why_cant_i_send_udp_packets_from_a_browser/", "https://github.com/mas-bandwidth/netcode/blob/main/STANDARD.md", "https://doc.libsodium.org/secret-key_cryptography/aead"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connect tokens and packet encryption

**Goal:** only clients your backend authorised can connect to a dedicated server, and their
traffic cannot be read, forged or replayed. Model: Glenn Fiedler's netcode.io standard.

## Flow
1. Client logs in to your **web backend** over HTTPS (normal auth).
2. Backend picks a server (matchmaking) and generates a **connect token**:
   - public part: server addresses, expiry, client-to-server key, server-to-client key,
     protocol id, timeout;
   - **private part** encrypted with a key shared only between backend and game servers: client id,
     the same two keys, user data (e.g. account id, entitlements).
3. Client sends a *connection request* packet containing the private token to the server over UDP.
4. Server decrypts the private part (rejects if expired, wrong protocol, or its own address not
   listed), sends back a **challenge** packet; client echoes the challenge; only then the server
   allocates a slot. The challenge round trip stops spoofed-source-IP floods from consuming slots.
5. All later packets are encrypted with the session keys.

## Packet encryption
- Use an AEAD cipher (ChaCha20-Poly1305 or AES-GCM via libsodium): encrypts and authenticates in one
  step; the header (packet type, sequence) is authenticated as associated data.
- **Nonce** = packet sequence number (64-bit, never reused for the same key). Separate keys per
  direction avoid nonce collisions between client and server.
- **Replay protection:** keep a window (e.g. 256 entries) of recently received sequence numbers;
  drop duplicates and packets older than the window.
- Drop any packet that fails authentication silently (no reply, no logging per packet: log rates).

## Why bother for games
- Without tokens, anyone who learns a server IP can connect, flood slots, or impersonate players.
- Without authentication, spoofed packets with a victim's IP and sequence can inject input.
- Encryption also hides chat and keeps cheat tools from trivially reading/modifying traffic (it does
  not stop memory-reading cheats).

## Operational details
- Token expiry short (e.g. 30-45 s); keys never logged.
- Rotate the backend/server private key; support two keys during rotation.
- Rate-limit connection requests per source IP before decryption to bound CPU.
- Engines: Unity Transport supports DTLS/secure connections with Relay; Steam Datagram Relay and Epic
  Online Services provide authenticated relays; Unreal supports packet handler components (e.g.
  AESGCM handler) for encryption.

## Verify
- [ ] Expired or modified token is rejected without allocating a client slot.
- [ ] Replayed captured packets are dropped (test with a packet capture and replay tool).
- [ ] Load test of spoofed connection requests keeps CPU bounded and real clients connecting.
