---
id: creative-arts.animation.principles.hip-shoulder-counter-rotation
name: hip-shoulder-counter-rotation
category: creative-arts
field: animation
product: principles
tags: [animation, walk-cycle, hip-shoulder-counter-rotation, arm-swing, hip-tilt, shoulder-tilt, walks, front-view, overlap]
level: practitioner
status: draft
description: "Add hip and shoulder counter-rotation, tilt and arm swing to walks: values in front and top view, timing offsets, and how they change with character."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Walk_cycle
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hip and shoulder counter-rotation

Goal: walks that move in three dimensions. Side-view walks are learned first; front and top
views reveal whether the body twists and tilts properly.

## Mechanics
- **Hip rotation (top view)**: the hip on the side of the forward leg rotates forward. Peaks at
  contact.
- **Shoulder rotation**: opposite to the hips - the shoulder of the forward arm (opposite the
  forward leg) rotates forward. The spine twists between.
- **Hip tilt (front view)**: on the down/passing position the hip of the free leg drops (the
  pelvis tilts down toward the unsupported side); shoulders tilt the opposite way to balance.
- **Lateral sway**: the body shifts over the supporting foot.
- **Arm swing**: arms swing opposite to the legs; the swing peaks slightly after contact
  (overlap). In a natural walk the elbow bends a little on the forward swing and is nearly
  straight on the back swing; the wrist drags at each change of direction.

## Starting values for a natural adult walk
- Hip rotation: about 5-10 degrees each side.
- Shoulder rotation: about 5-8 degrees opposite.
- Hip tilt: about 3-7 degrees.
- Arm swing peak offset: 1-3 frames after contact.

## Character variations
- Swagger: larger hip rotation and tilt.
- Masculine/heavy stomp: more shoulder rotation, less hip.
- Robot/soldier: little or none.
- Children: bigger lateral sway.

## Failure modes
- Hips and shoulders rotating the same way: stiff, "plank" walk.
- No tilt in front view: the walk looks like it slides on rails.
- Arm swing in sync with contacts exactly: mechanical.

## Verify
- [ ] Top view shows hips and shoulders twisting in opposition.
- [ ] Front view shows the free-leg hip dropping on passing.
- [ ] Arm swing peaks just after contact.

Related: `creative-arts.animation.principles.walk-key-poses`,
`creative-arts.animation.principles.weight-shift-in-standing-poses`.
