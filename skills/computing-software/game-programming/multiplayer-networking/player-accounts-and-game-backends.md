---
id: computing-software.game-programming.multiplayer-networking.player-accounts-and-game-backends
name: player-accounts-and-game-backends
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, game-backend, player-accounts, authentication, game-programming]
level: practitioner
status: draft
description: "Design player identity and backend services: platform auth tickets, account linking, session tokens, inventory and economy services, and choosing PlayFab, EOS or Nakama."
sources: ["https://learn.microsoft.com/en-us/gaming/playfab/", "https://dev.epicgames.com/docs/epic-account-services", "https://heroiclabs.com/docs/nakama/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Player accounts and identity backends

**Goal:** know who a player is across platforms and sessions, and keep economy data safe server-side.

## Identity flow
1. Client gets a **platform auth ticket** (Steam `GetAuthTicketForWebApi`, Xbox XSTS token, PSN auth
   code, Epic auth).
2. Backend verifies it with the platform's web API (e.g. Steam
   `ISteamUserAuth/AuthenticateUserTicket`) and maps platform id -> internal account id.
3. Backend issues its own **session token** (short-lived JWT) used for game services and passed to
   game servers in connect tokens.
Never trust a client-sent user id.

## Account linking
One internal account can link several platform identities (cross-progression). Handle conflicts
(two accounts both with progress) with a merge or choose flow; platforms restrict some data
(entitlements) to their own store.

## Backend services
- Profiles and saves (cloud save), inventory/currency (server-authoritative, transactional, with
  idempotency keys on purchase grants), leaderboards, friends/presence, matchmaking tickets, telemetry.
- Receipt validation for in-app purchases happens server-side against store APIs.

## Build vs buy
| Option | Notes |
|---|---|
| PlayFab (Microsoft) | Accounts, economy v2, CloudScript, matchmaking, multiplayer servers |
| Epic Online Services | Free, cross-platform auth, lobbies, P2P relay, voice |
| Nakama (Heroic Labs) | Open source, self-hostable, server runtime in Go/Lua/TS |
| Custom | Full control; you own security, scaling, GDPR deletion |

## Must-haves
- GDPR/CCPA data export and deletion endpoints.
- Rate limiting and anomaly detection on currency grants.
- Ban system keyed on account and platform id.

## Verify
- Replay a captured auth request with a modified user id: rejected.
- Grant the same purchase twice with one idempotency key: one grant.
