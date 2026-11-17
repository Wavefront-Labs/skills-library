---
id: computing-software.game-programming.multiplayer-networking.dedicated-server-matchmaking-and-session-architecture
name: dedicated-server-matchmaking-and-session-architecture
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, dedicated-server, matchmaking, lobby, session-management, server-browser, game-server-fleet, skill-based-matchmaking, elo, backfill, headless-server, listen-server, autoscaling, game-programming]
level: advanced
status: draft
description: "Architect matchmaking and dedicated-server session lifecycle: lobby vs matchmaker, server fleet allocation, skill-based matching, and reconnect/backfill."
sources: ["https://www.gdcvault.com/play/1025357/Shared-Server-Architecture-in", "https://aws.amazon.com/gamelift/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dedicated-server matchmaking and session architecture

**Goal:** the systems around the netcode — how players end up in a match
together on a server that actually exists and is ready for them — which is
infrastructure as much as it is gameplay code, and is where most "my netcode
works but the game doesn't" problems actually live.

## Listen server vs dedicated server — pick deliberately
A **listen server** (one player's machine hosts and plays) is simple to set up
and free to run, but gives that player a latency/authority advantage (their
inputs round-trip zero distance) and the whole match dies if the host quits
or their connection degrades — fine for small co-op, a liability for
competitive play. A **dedicated server** (headless build running on
infrastructure, no player is "the host") removes the host advantage and
survives any single player disconnecting, at the cost of running/paying for
server infrastructure and needing a session-allocation system to spin one up
per match. Most competitive multiplayer games use dedicated servers for
exactly the fairness reason; listen servers remain common for casual co-op
where that cost isn't justified.

## Lobby vs matchmaker — different jobs
- **Lobby**: players explicitly group together (invite friends, join a named
  room/server-browser entry) before the match starts; the lobby itself isn't
  gameplay-authoritative, it's a pre-match holding state tracking who's in,
  ready-up status, and settings.
- **Matchmaker**: a backend service that takes a pool of players wanting a
  match and a criteria (skill rating, region, game mode) and groups them
  automatically, then requests a server be allocated for the resulting match.
  These compose: a party formed in a lobby enters matchmaking together as one
  unit the matchmaker must keep intact, not split across separate matches.

## Skill-based matchmaking basics
Most implementations use some Elo-family rating (Elo itself, or a variant
like Glicko/TrueSkill that also tracks rating *uncertainty*, not just a point
estimate) updated after each match based on actual outcome vs the rating-
predicted expected outcome. Practical gotchas: a pure skill-first matcher
with no time-based widening of the acceptable skill range produces very long
queue times for players at the rating tails (very new or very high skill, with
few comparably-rated players online) — widen the acceptable skill delta the
longer a player has waited, trading match quality for queue time, with the
tradeoff curve tuned and monitored, not fixed at launch and forgotten.

## Server allocation and lifecycle
A dedicated-server fleet needs: a pool of warm or on-demand server processes,
an allocator that claims one for a formed match (and releases it back to the
pool when the match ends — a leaked "claimed but never released" server
silently shrinks fleet capacity over time, a real production incident class),
and health/heartbeat checks so a crashed server's claim is detected and the
match migrated or the players refunded a queue attempt rather than left
waiting indefinitely on a server that's already dead. Autoscaling (spin up
more server processes as concurrent-match demand rises) needs a startup-time
budget — if a fresh server instance takes 90 seconds to become ready and
demand spikes faster than that, players queue past the allocator's capacity
regardless of how good the matching logic is.

## Reconnect and backfill
A player disconnecting mid-match (not quitting deliberately) should be able to
**reconnect** to the same server/match session within a grace window, keeping
their in-match state — this requires the server to hold a disconnected
player's state (not immediately destroy their entity) for that window.
**Backfill** (replacing a player who leaves and doesn't return with a new
matchmade player) keeps match quality from degrading in team-based modes but
needs care: a backfilled player joining a match already in progress needs a
fast-forward/catch-up path (current score, time remaining, teammates) and the
matchmaker must know to treat an in-progress-with-an-open-slot match as a
valid backfill target, not just new full-lobby matches.

## Verify
- [ ] Claimed-but-abandoned dedicated server instances are detected and
      released back to the pool (tested by killing a server process mid-match
      and confirming the fleet capacity recovers).
- [ ] Matchmaking queue-time-vs-skill-delta widening is tuned against real
      population data, not left at a launch default indefinitely.
- [ ] A player who disconnects and reconnects within the grace window resumes
      with their prior state intact; one who doesn't is either backfilled or
      the match adjusts (bot fill, score handicap) per design.
- [ ] Autoscaling startup-time budget is measured and compared against
      realistic demand-spike rate, not assumed adequate.
