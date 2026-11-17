---
id: creative-arts.animation.principles.horse-gaits
name: horse-gaits
category: creative-arts
field: animation
product: principles
tags: [animation, animal-locomotion, horse-gaits, quadruped, walk, trot, canter, gallop, muybridge, footfall-pattern]
level: advanced
status: draft
description: "Animate horse gaits from their footfall patterns (walk four-beat, trot two-beat diagonal, canter three-beat, gallop four-beat with suspension) and timing."
sources:
  - https://books.google.com/books?vid=ISBN9780486202037
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Horse_gait
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Horse gaits

Goal: correct footfall order and rhythm for each gait - the thing horse riders and Muybridge
readers notice immediately.

## Footfall patterns (LH = left hind, LF = left fore, etc.)
| Gait | Beats | Order | Suspension |
|---|---|---|---|
| Walk | 4, even | LH, LF, RH, RF | none; always 2-3 feet down |
| Trot | 2 | diagonal pairs: LH+RF, then RH+LF | brief, between beats |
| Canter (right lead) | 3 | LH; then RH+LF together; then RF (leading leg) | after the leading fore |
| Gallop (right lead) | 4 | LH, RH, LF, RF | long, after RF |

## Timing at 24 fps (average riding horse, starting points)
- Walk cycle: about 1-1.2 s per full cycle (24-30 frames).
- Trot: about 0.6-0.8 s per cycle (14-18 frames).
- Canter: about 0.6 s (14-16 frames).
- Gallop: about 0.4-0.5 s (10-12 frames).

## Body motion
- **Head and neck** nod in the walk (down as each forefoot lands) and in the canter/gallop
  (counterbalance); stable in the trot.
- **Back** stays fairly level in walk and trot; rocks in the canter (rocking-horse motion);
  extends and compresses in the gallop (spine flex).
- Hind legs: hock joint bends backward (it is the ankle), fetlock flexes at contact.

## Method
1. Plan the footfall chart (frames when each hoof is down) on a timeline.
2. Key contacts and lifts per leg according to the chart.
3. Add the body's vertical and pitch motion following the footfalls.
4. Add head/neck counterbalance and tail overlap.

## Failure modes
- Lateral pairs moving together in a trot (that is a pace - a different gait).
- Even 4-beat timing on a canter.
- Front legs bending like human knees backward (the "knee" is a wrist; it bends the other way
  from the hock).

## Verify
- [ ] Footfall chart matches the table for the gait.
- [ ] Suspension frames only where the gait has them.
- [ ] Head/neck motion matches the gait.

Related: `creative-arts.animation.principles.quadruped-walk-cycles`.
