---
id: computing-software.game-programming.gameplay-programming.knockback-hit-reactions-and-iframes
name: knockback-hit-reactions-and-iframes
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, knockback, invincibility-frames-craft, hit-reaction, game-programming]
level: practitioner
status: draft
description: "Implement hit reactions: knockback impulses vs scripted displacement, hit-stun durations, invincibility frames, poise/super armor and avoiding stun-lock and wall-stuck states."
sources: ["https://gameprogrammingpatterns.com/state.html", "https://www.gdcvault.com/play/1023475/Combat-Design-Insights-from-the"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Knockback, hit reactions and invincibility frames

**Goal:** getting hit feels impactful and readable, never traps a player in endless stun or walls.

## Reaction pipeline (on damage accepted)
1. Determine **reaction tier** from attack data vs defender state: none (super armor/poise), flinch
   (additive anim, no movement loss), stagger (hit-stun state), knockdown/launch.
2. Apply **knockback**: direction from attacker (or attack's defined vector), magnitude from attack data,
   scaled by defender weight.
3. Enter **HitStun** state for N frames (from attack data) — blocks actions except allowed escapes.
4. Grant **i-frames** where design wants (after knockdown, on dodge, after respawn).

## Knockback implementation
- Physics-driven characters: `velocity = knockDir * force` (override, don't add, to keep consistency),
  with friction/drag to stop.
- Kinematic controllers: scripted displacement over time from a curve (distance d over t seconds),
  using collide-and-slide so walls stop it. Deterministic and designer-tunable.
- Stop knockback against walls; optionally "wall bounce/splat" state.

## Invincibility frames
- Flag or counter on the hurtbox/damage receiver: `invulnerableUntil = now + duration`. Damage pipeline
  rejects hits while active (but may still register "blocked" feedback).
- Dodge i-frames come from animation data (active frames of the roll).
- Visual tell: flashing/transparency on i-frames after damage (classic 2D), not during dodges.

## Poise / super armor
Poise meter: hits subtract poise; reaction only when poise breaks; regenerates after delay. Super armor
windows on heavy attacks (from animation events) prevent interruption but still take damage.

## Anti stun-lock
- Diminishing hit-stun with consecutive hits (combo scaling) or a max combo duration.
- Burst/escape mechanic after N hits.
- Multi-attacker games: AI attack tokens limit simultaneous attackers.

## Multiplayer
Hit reactions on the victim's own client may be delayed by latency; predict cosmetic flinch, but movement
displacement must come from the authority to avoid rubber-banding fights.

## Gotchas
- Hit-stun state and knockback both set velocity; one owner of velocity per frame.
- Re-hitting during knockback should restart/stack per rules, not leave two coroutines running.
- I-frames that also disable the collider break other systems (pickups, triggers); use a damage flag.

## Verify
- [ ] Combo tests: maximum continuous stun under design cap.
- [ ] Knockback into a wall: no clipping, no stuck state.
