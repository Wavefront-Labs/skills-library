---
id: creative-arts.animation.principles.fish-and-snake-undulation
name: fish-and-snake-undulation
category: creative-arts
field: animation
product: principles
tags: [animation, animal-locomotion, undulation, fish-swim, snake, serpentine, wave-principle, spine-chain, creature-animation]
level: practitioner
status: draft
description: "Animate undulating locomotion (fish swimming, snakes slithering, eels): a travelling body wave, amplitude growing toward the tail, and contact points for snakes."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Fish_locomotion
  - https://en.wikipedia.org/wiki/Undulatory_locomotion
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fish and snake undulation

Goal: bodies that move by passing a wave along themselves.

## The wave
- A sideways bend starts at the head and travels to the tail.
- **Amplitude grows toward the tail** in most fish (the head moves least so the eyes stay steady).
- Wave speed along the body is faster than the forward speed of the animal - the wave pushes
  the water back.

## Fish types
| Type | Motion |
|---|---|
| Eel-like (anguilliform) | whole body undulates, many wavelengths |
| Typical fish (carangiform, trout) | rear half bends, head nearly still |
| Tuna-like (thunniform) | body stiff, tail fin beats fast |
| Ray | wave along the pectoral "wings" |

## Snakes
- **Lateral undulation**: the body follows the head's path, like a train on tracks; each body
  point passes through the same positions. Push points against ground irregularities.
- Animate with a path/curve: move the body along a curve and let the head draw the path
  (Blender: Curve modifier or spline IK; Maya: motion path or spline IK).
- Sidewinding and concertina are different gaits - check reference.

## Method (spine chain)
1. Head/root moves forward along the path.
2. Each segment copies the previous segment's rotation curve delayed in time (wave travel),
   with increasing amplitude to the tail (fish) or constant along the path (snake).
3. Add fins and tail fin overlap.

## Failure modes
- Whole body swinging side to side in sync: no wave.
- Snake body cutting corners instead of following the head's path.
- Head swinging as much as the tail (fish).

## Verify
- [ ] A clear wave travels head to tail.
- [ ] Tail amplitude > head amplitude (fish).
- [ ] Snake body points follow the head's track.

Related: `creative-arts.animation.principles.wave-and-whip-action`,
`creative-arts.animation.principles.offset-keys-in-the-graph-editor`.
