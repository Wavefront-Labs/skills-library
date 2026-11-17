---
id: computing-software.game-programming.game-ai-programming.shared-team-knowledge
name: shared-team-knowledge
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, shared-knowledge, squad-ai, blackboard, game-programming]
level: practitioner
status: draft
description: "Share perception and knowledge across AI teams: team blackboards, reporting and propagating sightings, confidence decay, and avoiding omniscient enemies."
sources: ["https://www.gameaipro.com/", "https://gameprogrammingpatterns.com/observer.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared team knowledge

**Goal:** squads that coordinate on shared information, while players still feel enemies learn
things believably.

## Team blackboard
A per-team or per-squad store of facts:
```text
TargetRecord { entity, lastKnownPos, lastSeenTime, reportedBy, confidence, threat }
Claims       { coverPoint -> agent, flankRoute -> agent, targetAttackers -> count }
```
Agents write their own perception results; decisions read team records plus their own memory.

## Propagation rules (believability)
- **Communication delay and range:** a sighting reaches the team only after the spotter "calls it
  out" (bark audio) or within radio range; this gives players a window to silence the spotter.
- **Confidence decay:** last known position grows stale; confidence decreases with time, search
  behaviours spread out around it.
- Distinguish **seen** (own perception) from **told** (team info) so agents investigate told
  positions instead of firing at them.

## Coordination uses
- Claims prevent everyone using the same cover or the same flank.
- Attacker tokens: limit how many agents engage the player at once (the "kung fu circle").
- Shared danger map (grenade zones, recent deaths) for avoidance.

## Avoiding omniscience
Never let AI read the player's true position except through perception or explicit cheating
designed for difficulty. Track for debugging which agents know what and why.

## Verify
- Debug view: team knowledge overlay with stale/confident markers; stealth test where killing the
  spotter before callout keeps the team unaware.
