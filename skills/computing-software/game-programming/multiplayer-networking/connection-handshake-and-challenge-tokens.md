---
id: computing-software.game-programming.multiplayer-networking.connection-handshake-and-challenge-tokens
name: connection-handshake-and-challenge-tokens
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, connection-handshake, challenge-response, client-server-connection, keep-alive, timeouts, amplification-attack, game-programming]
level: advanced
status: draft
description: "Build a UDP client-server connection handshake: stateless challenge tokens, anti-amplification padding, slots, keep-alives and timeouts."
sources: ["https://gafferongames.com/post/client_server_connection/", "https://github.com/mas-bandwidth/netcode/blob/main/STANDARD.md", "https://datatracker.ietf.org/doc/html/rfc9000#section-8"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connection handshake and challenge tokens

**Goal:** UDP has no connections; build a handshake so the server only allocates a client slot for
a real client at a real address, cannot be used to amplify attacks, and detects timeouts.

## Handshake (Gaffer / netcode.io shape)
1. **Client -> server: connection request.** Contains protocol version and (in netcode.io) the
   encrypted connect token from the backend. **Pad to ~1000+ bytes** so the request is at least as
   big as the response: prevents reflection/amplification.
2. **Server -> client: challenge.** The server does **not** allocate state yet. It returns a
   challenge token = encrypt/HMAC(serverKey, clientAddress, clientSalt, timestamp, sequence).
3. **Client -> server: challenge response** echoing the token. The server verifies the MAC, address
   and freshness, then allocates a slot, and sends **connection accepted** (client index, max clients).
4. Client is connected; both sides send keep-alives when idle.
Stateless challenges mean spoofed-source floods cost the server no memory (same idea as TCP SYN
cookies and QUIC Retry tokens).

## Server state
- Fixed array of `maxClients` slots; lookup by address -> slot. Full server replies "denied" (also
  padded/rate-limited).
- Reject duplicate connects from an address or client id already connected.
- Rate-limit requests per source address.

## Liveness
- Keep-alive every ~0.1-1 s when no other packets are sent.
- Timeout if nothing is received for N seconds (5-10 s typical; shorter for competitive games).
- Disconnect packet sent redundantly (e.g. 10 copies) so the peer learns quickly; still rely on
  timeout as the fallback.
- Treat any accepted packet from the address as liveness, not only keep-alives.

## Security notes
- Plain challenge/response only proves the client can receive at its address; it does not
  authenticate a user. Use connect tokens issued by your web backend (see
  `connect-tokens-and-packet-encryption`) for authentication and encryption.
- Never trust the client's claimed index or id after connection; key everything by address/session.

## Verify
- [ ] Spoofed-source flood of connection requests allocates no slots and no per-request memory.
- [ ] Response sizes never exceed request sizes before the address is validated.
- [ ] Pulling a client's cable frees its slot after the timeout; other clients see a disconnect event.
