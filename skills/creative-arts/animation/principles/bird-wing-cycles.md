---
id: creative-arts.animation.principles.bird-wing-cycles
name: bird-wing-cycles
category: creative-arts
field: animation
product: principles
tags: [animation, animal-locomotion, wing-cycle, flight, birds, downstroke, upstroke, flapping, gliding, creature-animation]
level: practitioner
status: draft
description: "Animate bird flight: downstroke power and upstroke recovery, wing folding and feather overlap, body bob opposite the wings, and flap rates by size."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9780486202037
  - https://en.wikipedia.org/wiki/Bird_flight
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bird wing cycles

Goal: wings that push air - a powerful downstroke and a folded, quicker recovery - with the body
reacting.

## Phases
1. **Downstroke (power)** - wing fully extended, sweeps down and slightly forward; feathers
   spread; slower and stronger. Wing tip leads a figure-eight path.
2. **Bottom** - wing below the body, tips bending up from air pressure (overlap).
3. **Upstroke (recovery)** - wing partly folds at the wrist, pulls up and back; primary
   feathers separate to let air through. Faster.
4. **Top** - wing raised, unfolding for the next downstroke.

## Body
- The body rises on the downstroke and sinks on the upstroke (opposite to the wings).
- Head stays stabilised (birds hold their head steady).
- Tail adjusts for steering and braking.

## Flap rates (real, approximate)
| Bird | Beats per second | Frames per flap at 24 fps |
|---|---|---|
| Hummingbird | 50+ | blur / smear |
| Pigeon | ~5-8 | 3-5 |
| Crow | ~3-4 | 6-8 |
| Large raptor / heron | ~2 | about 12 |
| Albatross | glides, few flaps | - |
Larger birds flap slower; animated birds are often slowed for readability.

## Gliding and landing
- Glide: wings extended, small adjustments, body steady.
- Landing: wings spread wide and tilt to brake (alula feathers out), legs extend forward, tail
  fans down, several strong back-flaps.

## Failure modes
- Up and down strokes identical in speed and shape (wings as rigid paddles).
- Body moving with the wings instead of opposite.
- Wings not folding on the upstroke.

## Verify
- [ ] Downstroke slower than upstroke; wing folds on upstroke.
- [ ] Body bob opposite to wings.
- [ ] Flap rate matches the bird's size.

Related: `creative-arts.animation.principles.wave-and-whip-action`.
