---
id: computing-software.game-programming.gameplay-programming.hitbox-hurtbox-and-combat-timing
name: hitbox-hurtbox-and-combat-timing
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, hurtbox, frame-data, active-frames, startup-frames, recovery-frames, invincibility-frames, i-frames, combo-system, hit-stop, animation-events, combat-timing, fighting-game, action-game, game-programming]
level: advanced
status: draft
description: "Implement melee/combat hit detection with frame-accurate hitboxes and hurtboxes, startup/active/recovery timing, and invincibility windows."
sources: ["https://www.gdcvault.com/play/1025695/Math-for-Game-Programmers-Juicing", "https://glossary.infil.net/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hitboxes, hurtboxes, and combat timing

**Goal:** detect combat hits in a way that feels fair and precise, driven by
authored frame data rather than "check distance every frame," and get the
timing vocabulary (startup/active/recovery, i-frames) that every combat
designer and fighting-game-literate player expects.

## Hitbox vs hurtbox — never conflate them
- **Hitbox**: the volume that, if it overlaps an opponent's hurtbox during its
  active window, causes a hit (attached to the attacking limb/weapon).
- **Hurtbox**: the volume representing where an entity can *be* hit (usually
  closer to the actual body silhouette than the hitbox is to the weapon).
Using the same collider/layer for both is the most common cause of "I got hit
when I was clearly not in range" — a sword swing's hitbox should be shaped and
timed to the blade's swing arc, not a single capsule matching the whole
character for the whole animation.

## Frame data: startup / active / recovery
Every attack decomposes into three phases, each with a frame count:
- **Startup**: wind-up before the hitbox turns on — no hit possible yet, but
  the attacker is often already committed/vulnerable.
- **Active**: the window(s) where the hitbox is actually enabled and can
  connect. May be several discrete windows for one animation (a flurry has
  multiple active windows, not one long one).
- **Recovery**: after the hitbox turns off, before the attacker can act again
  — the vulnerability window an opponent is meant to be able to punish.
This data should be **authored explicitly** (a table per attack, or markers on
the animation timeline) and driven by **animation events**, not polled by
frame-counting in a generic Update loop — an animation event firing
`EnableHitbox()`/`DisableHitbox()` at the exact authored frame keeps hit
timing locked to whatever the animation actually shows, so a later animation
re-timing (retargeted, sped up for game feel) automatically carries the hitbox
timing with it instead of needing a parallel hardcoded frame count to be
manually kept in sync.

## Hit registration mechanics
- **One hit per activation, not per overlap-frame**: a hitbox active for 5
  frames overlapping a hurtbox the whole time must register exactly once, not
  once per physics tick it stays overlapping — track "already hit this target
  during this active window" per hitbox-instance, cleared when the hitbox
  (re)activates.
- **Multi-hit attacks** (a flurry meant to hit 3 times) need either multiple
  distinct active windows each clearing their own hit-registry, or an explicit
  hit-count/cooldown-per-target design — don't rely on the overlap naturally
  separating, since fast-moving hurtboxes can produce false double-registration
  or false misses depending on tick alignment.
- **Priority/multi-target**: decide up front whether one swing can hit
  multiple enemies simultaneously (cleave) or only the first (single-target) —
  this changes whether you process "first overlap wins" or "all overlaps this
  window."

## Invincibility frames (i-frames)
A dodge/roll typically grants a window where the hurtbox is disabled or
flagged immune to specific hit types — authored the same way as hitbox
windows (animation-event-driven, explicit frame range), not "while the dodge
animation is playing" as a loose proxy, since that couples invincibility
duration to animation length rather than to deliberately tuned game feel. Two
failure modes to design against: i-frames that are too generous relative to
their animation's visual tell (feels like cheating/unfair from the opponent's
side in PvP) and i-frames that don't cover the actual vulnerable window the
animation visually implies (feels unresponsive/broken from the dodging
player's side). Playtesting frame windows against real reaction inputs, not
just theorycrafting the numbers, is where this actually gets tuned.

## Verify
- [ ] Hitbox and hurtbox are separate colliders/shapes, never the same volume
      reused for both roles.
- [ ] Hitbox enable/disable is driven by animation events at authored frames,
      not a hardcoded frame-count timer parallel to the animation.
- [ ] A hitbox active across multiple ticks against a stationary target
      registers exactly one hit, verified with a debug overlay or hit counter.
- [ ] i-frame windows are explicit and tested against real timed inputs (not
      just "animation is playing"), confirmed to start/end where the animation
      visually suggests they should.
