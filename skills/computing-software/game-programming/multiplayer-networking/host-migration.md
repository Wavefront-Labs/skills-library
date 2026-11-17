---
id: computing-software.game-programming.multiplayer-networking.host-migration
name: host-migration
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, host-migration, listen-server, peer-to-peer, session-resilience, state-synchronization, game-programming]
level: advanced
status: draft
description: "Design host migration for listen-server and P2P games: electing a new host, which state every client must already hold, reconnecting through relays, and when not to bother."
sources: ["https://partner.steamgames.com/doc/features/multiplayer/matchmaking", "https://partner.steamgames.com/doc/api/ISteamMatchmaking", "https://partner.steamgames.com/doc/features/multiplayer/networking", "https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host migration

**Problem:** in a listen-server or host-authoritative P2P game, the host leaving (quit, crash,
connection loss) ends the match for everyone unless another peer takes over.

## Decide first
Dedicated servers remove the need entirely. Host migration is worth it for long co-op sessions or
console P2P titles where dedicated servers aren't viable; for 5-minute matches, ending the match
gracefully (with results saved) is often the better trade.

## Requirements
1. **Every client keeps enough state to become host:** the authoritative-ish world state, not just
   what it renders. Interest management that hides state from clients conflicts with this; accept
   that or periodically replicate a compact "migration snapshot" to all peers (or a chosen backup).
2. **Deterministic election:** all peers pick the same new host without a round of negotiation,
   e.g. lowest stable player id among those still connected, or best measured connectivity reported
   earlier. Precompute and replicate a "next host" order while the host is alive.
3. **Reconnection path:** peers must reach the new host. Use a relay or a lobby service that
   republishes the host address (Steam lobbies `SetLobbyOwner`/lobby data, Unity Relay/Lobby,
   EOS P2P). Direct IP connections break when the host's NAT mapping was the only route.
4. **Resume state:** new host loads the latest migration snapshot, re-creates network ids identically
   (keep ids stable), resumes simulation, and tells clients the authoritative tick to resync from.

## Sequence
```
detect host loss (timeout ~2-5 s, or explicit leave message)
pause/freeze gameplay locally, show "Host left, migrating..."
elect: newHost = firstConnected(nextHostOrder)
newHost: start listening/register with lobby/relay, restore snapshot, mark itself authoritative
others: connect to newHost, send last acked tick, receive delta/full state
resume when all (or a quorum) reconnect; drop peers that time out
```

## Gotchas
- Server-only data (AI internal state, RNG seed, hidden inventory, timers) must be in the snapshot or
  migrated games diverge from what players saw.
- Anti-cheat: the new host is a player; same trust problem as any listen server.
- Test intentional host kill at every game phase (loading, combat, end-of-round, during a cutscene).
- Unreal has no built-in host migration; Unity's multiplayer services offer a host-migration feature
  that snapshots session state; check current SDK support before designing around it.

## Verify
- [ ] Killing the host process mid-combat resumes within the target time with no lost progress beyond the last snapshot.
- [ ] Two simultaneous disconnects (host + next host) still elect a single host.
