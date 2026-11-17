---
id: creative-arts.game-design.systems-and-mechanics.game-camera-design
name: game-camera-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, camera-design, three-cs, game-feel, camera-window, look-ahead, third-person-camera, 2d-camera, camera-collision, motion-sickness]
level: advanced
status: draft
description: "Design the game camera as part of the 3Cs: choose perspective, then tune 2D camera windows and look-ahead or 3D follow, collision and framing, with comfort settings."
sources:
  - https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Game camera design

**Goal:** a camera that shows the player what they need to make decisions, feels
smooth, and never fights the controls. Rogers' "3Cs" (character, camera, controls)
treats it as a core design element, not an afterthought.

## Choose the perspective
| Perspective | Strength | Cost |
|---|---|---|
| 2D side | clear jumps/readability | limited depth |
| Top-down / isometric | tactical overview | vertical info harder |
| Third-person follow | character presence, spatial awareness | camera collision, occlusion |
| First-person | immersion, aiming | body awareness, motion sickness |
| Fixed/cinematic | framing control | control mapping issues when cameras cut |

## 2D techniques (Itay Keren, "Scroll Back: The Theory and Practice of Cameras in Side-Scrollers")
- **Camera window:** player moves freely inside a box; camera moves when they push the edge.
- **Platform snapping:** vertical camera updates only when the player lands, avoiding
  jitter during jumps.
- **Look-ahead / forward focus:** shift view in the direction of travel.
- **Lerp smoothing** toward targets; **cues/attractors** to frame points of interest.
- **Zones** that lock the camera for arenas and set pieces.

## 3D follow camera checklist
1. Distance, height and pitch per context (exploration, combat, tight spaces).
2. **Collision:** pull in when geometry blocks; return smoothly; never clip into walls.
3. **Occlusion:** fade or dither objects between camera and player.
4. **Auto-centering:** gentle, with delay after manual input; never yank the camera
   while the player is aiming.
5. **Lock-on/targeting** framing for combat.
6. **Control-relative movement** must remain stable when the camera cuts (keep the
   previous mapping until the stick is released).

## Comfort and accessibility
Expose: field of view, camera sensitivity per axis, invert per axis, camera shake/bob
toggles, auto-centering toggle. Motion sickness triggers include low FOV, head bob and
sudden acceleration.

## Gotchas
- Tight camera smoothing hides responsiveness problems in controls and vice versa;
  tune them together.
- Camera behaviour in tight interiors is where most 3D cameras fail; test there first.

## Verify
- [ ] Perspective chosen with stated reason.
- [ ] 2D: window/snapping/look-ahead tuned; 3D: collision, occlusion, auto-centre tested.
- [ ] FOV, sensitivity, invert and shake options present.
- [ ] No camera-induced deaths observed in playtests.
