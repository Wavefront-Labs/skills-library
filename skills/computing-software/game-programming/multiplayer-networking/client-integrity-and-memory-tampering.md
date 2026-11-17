---
id: computing-software.game-programming.multiplayer-networking.client-integrity-and-memory-tampering
name: client-integrity-and-memory-tampering
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, memory-tampering, anti-cheat, client-integrity, game-programming]
level: practitioner
status: draft
description: "Defend against client memory tampering: server authority first, value obfuscation, integrity checks, kernel anti-cheat trade-offs and detection telemetry."
sources: ["https://dev.epicgames.com/docs/game-services/anti-cheat/using-anti-cheat", "https://partner.steamgames.com/doc/features/anticheat"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client integrity and memory tampering

**Goal:** make memory editors (Cheat Engine), speed hacks and injected DLLs ineffective or detectable.

## Priority order
1. **Server authority** removes the value of tampering: a client editing its ammo changes nothing if
   the server owns ammo. Most "memory hacks" exploit trust given to the client.
2. **Validation:** the server checks movement speed, fire rate, line of sight; tampered clients get
   rejected or flagged.
3. **Client hardening** only for what must live on the client (aim, wallhack-visible data, local
   single-player economies).

## Client hardening techniques
- **Value obfuscation:** store sensitive values XORed with a per-session random key, or split
  across two fields, with a checksum; defeats naive value scanning (Unity ObscuredTypes-style).
- **Don't send what the client shouldn't know:** server-side visibility culling (fog of war, enemies
  behind walls) defeats wallhacks fundamentally.
- **Integrity checks:** hash code sections and critical data periodically; detect debuggers and
  known injected modules. Expect bypasses; vary checks across builds.
- **Speed hack detection:** compare client-reported time deltas against server time.

## Anti-cheat services
Easy Anti-Cheat and BattlEye provide kernel-mode drivers, module scanning, and server-side ban APIs;
integrate via their SDKs (EAC: client module + server `EOS_AntiCheatServer` interface). Kernel
anti-cheat has privacy, compatibility (Linux/Steam Deck via Proton requires opting in) and stability costs.

## Detection over prevention
Send telemetry (stat anomalies, impossible accuracy) and ban in waves so cheat developers can't
correlate detection with a specific change.

## Verify
- Run Cheat Engine against a dev build: changing displayed health or currency has no server effect.
