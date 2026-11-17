---
id: creative-arts.game-design.systems-and-mechanics.juice-and-feedback-polish
name: juice-and-feedback-polish
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, juice, screen-shake, hitstop, game-feel, polish, feedback, particles, squash-and-stretch, tweening, camera-shake, hit-pause]
level: practitioner
status: draft
description: "Add juice to game actions (screen shake, hitstop, squash and stretch, particles, sound, tweening) in proportion to impact, and keep it readable and toggleable."
sources:
  - https://www.youtube.com/watch?v=Fy0aCDmgnxg
  - https://www.routledge.com/Game-Feel-A-Game-Designers-Guide-to-Virtual-Sensation/Swink/p/book/9780123743282
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Juice and feedback polish

**Goal:** make every important action feel responsive and impactful through layered
audiovisual feedback, without obscuring the game state.

"Juice it or lose it" (Martin Jonasson and Petri Purho, GDC Europe 2012) demonstrates
taking a plain Breakout clone and layering tweening, squash and stretch, particles,
screen shake, sound and more to transform its feel. Swink calls this layer "polish".

## Toolkit
| Technique | What it does | Typical scale |
|---|---|---|
| Hitstop (hit pause) | freeze attacker/target a few frames on impact | ~2-6 frames for light hits, more for heavy |
| Screen shake | sells impact/explosions | small, short, decaying; scale with impact |
| Squash and stretch | elasticity on jump/land/hit | brief scale tweens |
| Tweening/easing | objects ease in/out instead of snapping | ease-out for arrivals |
| Particles | debris, sparks, dust on land | burst on event, fade fast |
| Flash / colour pop | hit confirmation | 1-2 frames white flash |
| Sound layering | attack + impact + material sound | pitch variation per hit |
| Camera kick / zoom | emphasise big moments | brief, return smoothly |
| Controller rumble | tactile confirmation | short, scale with impact |
Exact frame counts are tuning choices, not standards; tune by feel and test.

## Procedure
1. List core actions by **importance** (shoot, hit, land, collect, die, level up).
2. Assign a **feedback budget** per action proportional to its importance; the most
   frequent action needs crisp but light feedback (fatigue), rare big events get more.
3. Add layers one at a time and A/B against the plain version.
4. Use **trauma-based screen shake** (a common technique presented by Squirrel Eiserloh
   in GDC's "Math for Game Programmers" talks): accumulate trauma per event, shake =
   trauma squared (or cubed) x noise, decay over time - smooth, stackable, capped.
5. Add **randomised pitch/variation** to repeated sounds to avoid machine-gun repetition.

## Gotchas
- Too much juice hides information (enemies lost in particles) and causes motion
  sickness. Offer screen-shake and flash intensity sliders (accessibility; flashing can
  be a seizure risk).
- Hitstop in multiplayer must be handled carefully with netcode.
- Juice cannot fix a dull core mechanic; it amplifies what is there.

## Verify
- [ ] Each core action has feedback scaled to its importance.
- [ ] Screen shake and flash have intensity/off options.
- [ ] Testers prefer the juiced version in side-by-side comparison.
- [ ] Gameplay-critical info stays readable during the busiest effects.
