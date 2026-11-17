---
id: computing-software.game-programming.game-ai-programming.squad-coordination-ai
name: squad-coordination-ai
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, squad-ai, tactical-ai, blackboard, role-assignment, flanking, suppression, token-system, game-programming, attack-tokens]
level: advanced
status: draft
description: "Coordinate squads of AI: a squad blackboard, role assignment (suppress, flank, rush), attack tokens to limit simultaneous attackers, formations and barks that sell the teamwork."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter28_Beyond_the_Kung-Fu_Circle_A_Flexible_System_for_Managing_NPC_Attacks.pdf", "https://www.gameaipro.com/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Squad coordination AI

**Goal:** enemies that act as a team (one suppresses, one flanks, they don't all rush at once)
while each agent remains an individual decision maker.

## Architecture
- **Squad manager** (one per group) with a **shared blackboard**: known threats, last-known player
  position, assigned roles, reserved cover points, squad goal (hold, advance, retreat).
- Individuals keep their own behaviour tree/utility AI; the squad layer only **assigns intents and
  constraints** (role, target area, permission to attack). FEAR's approach: squad behaviours issue
  goals to individuals, whose planners decide how (Orkin, GDC 2006).
- Update the squad layer at low frequency (2-5 Hz).

## Role assignment
Each tick, compute a score for each (agent, role) pair, e.g. flanker = good path to the threat's
side that avoids its view cone; suppressor = has line of sight from cover; rusher = closest with
melee weapon. Assign greedily by highest score (or Hungarian algorithm for small squads), with
hysteresis to keep roles stable. Roles map to behaviour parameters (suppress: fire at last-known
position even without LOS; flank: path with cost penalty inside the threat's view cone, via
influence map/tactical pathfinding, see `influence-maps`).

## Attack tokens (pacing the pressure)
Limit simultaneous attackers on one target with a token pool (the "kung-fu circle"): an agent must
acquire a token to attack; others reposition, taunt or wait. Tokens per target scale with
difficulty; tokens have cooldowns and are returned on death/interrupt. Same pattern for grenade
throws (one per 5 s per squad) and melee rushes.

## Communication that sells it
Barks tied to squad decisions ("Flanking left!", "Cover me!", "Man down!") are a large part of how
players perceive coordination; trigger them from role assignments and events, rate-limited, and make
the speaker the agent doing the action.

## Formations and movement
Move in formations with slots relative to the leader (offsets rotated by heading), with slot
re-assignment by distance; break formation on contact. Stagger move starts to avoid robotic
synchronisation.

## Pitfalls
- Perfect information: the squad should only know what its members perceived (share perception,
  not ground truth).
- All agents re-planning in the same frame after an event: time-slice and add small random delays.

## Verify
- [ ] With 4 agents, at most N attack at once (tokens) and at least one flanks when cover is available.
- [ ] Killing the flanker triggers a re-assignment within one squad update.
- [ ] Debug view shows each agent's role and token state.
