---
id: creative-arts.game-design.narrative-design.social-simulation-stories
name: social-simulation-stories
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, social-simulation, emergent-narrative, relationship-systems, npc-relationships, story-sifting]
level: practitioner
status: draft
description: "Design simulation-driven social stories: traits, relationship values, social actions with preconditions, gossip, and surfacing emergent stories players can retell."
sources:
  - https://www.routledge.com/Procedural-Storytelling-in-Game-Design/Short-Adams/p/book/9781138595309
  - https://emshort.blog/
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simulation-driven social stories

**Goal:** characters whose relationships change through simulated social actions, so
stories emerge that players retell (The Sims, Dwarf Fortress, Crusader Kings, the Nemesis
system, Prom Week, Versu).

## Building blocks
| Block | Example |
|---|---|
| Traits | brave, jealous, gossip, ambitious |
| Relationship values per pair | affection -100..100, respect, rivalry flag |
| Social actions / exchanges | flirt, insult, apologise, recruit; each with preconditions, intent, effects |
| Memories | "Ana insulted me at the feast" with salience that decays |
| Norms / practices | what is appropriate in a context (Versu's social practices) |
| Propagation | gossip spreads memories to friends, with distortion |

## Action schema
```
action: insult
pre: rivalry(a,b) or affection(a,b) < -30
volition: +20 if a.trait == hot_headed; +10 if audience contains b.friend
effects: affection(b,a) -= 25; memory(b, "insulted by a", salience 0.8)
         if witness w: affection(w,a) -= 5 if w.likes(b)
```
Prom Week's Comme il Faut used social exchanges like this with volition rules computed from traits and history.

## Making stories legible
1. **Surface causes:** show why someone acted ("Ana is still angry about the feast").
2. **Story sifting:** detect interesting patterns in the event log (betrayal after
   friendship, revenge loops) and highlight them in notifications or recaps.
3. **Player hooks:** give the player social actions in the same system so they can
   intervene.
4. **Anchor with authored arcs** at key moments; pure simulation rarely builds a climax.

## Tuning
- Start with few traits and relationship axes; every new axis multiplies emergent noise.
- Clamp and decay values so states do not lock permanently.
- Run headless simulations for hundreds of days and read the event logs for absurd
  outcomes (everyone marries everyone, one NPC hated by all).

## Gotchas
- Emergence the player cannot see did not happen; invest in presentation as much as simulation.
- Text generated per action repeats; author variants and context-sensitive lines.
- Players exploit social systems (gift spam); add diminishing returns.

## Verify
- [ ] Headless runs produce varied, explainable relationship outcomes.
- [ ] Every NPC action can show its cause in the UI.
- [ ] Playtesters retell at least one emergent story unprompted.
