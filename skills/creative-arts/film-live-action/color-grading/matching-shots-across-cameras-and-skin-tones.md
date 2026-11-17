---
id: creative-arts.film-live-action.color-grading.matching-shots-across-cameras-and-skin-tones
name: matching-shots-across-cameras-and-skin-tones
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, colorist, colourist, shot-matching, scene-matching, multi-camera, camera-matching, skin-tones, skin-tone-line, vectorscope, waveform, rgb-parade, balance, exposure-matching, white-balance, log-footage, look-development, hero-shot, reference-still, split-screen, wipe, primaries, secondaries, qualifier, hsl, mixed-lighting, davinci-resolve, baselight, matching-with-scopes, parade-matching, mixed-camera-match, camera-profile-match, exposure-shift-match, wb-shift-match, within-scene-match, skin-match, skin-consistency, skin-across-shots, skin-secondary, skin-isolation]
level: practitioner
status: draft
description: "Make a live-action scene feel like one moment: balance per shot, pick a hero shot, match by scopes and split-screen, keep skin tones natural across cameras and lighting, then apply the look."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching shots across cameras and skin tones

**Goal:** a scene shot over a day, on more than one camera, with changing light, must
cut together without the audience noticing jumps — and faces must look like living
people throughout. Matching comes before look. The general grading vocabulary (lift,
gamma, gain, scene- vs display-referred) overlaps with
`creative-arts.animation.color.color-grading`; this skill is about live-action problems:
real skin, mixed cameras, drifting daylight. Tool examples assume DaVinci Resolve
(see `creative-arts.film-live-action.davinci-resolve.colour-managed-project-and-node-tree`);
the method is the same in Baselight or others.

## 1. Normalise first
Convert every camera's log into one working space with the correct input transform
for that camera and its settings (a wrong input transform cannot be "graded away"
cleanly). Then for each shot do a technical **balance**: exposure so the key subject sits
where intended, and neutral greys/whites neutral (unless the scene is meant to be
warm/cool — then match to the intent, not to neutral).

## 2. Choose a hero shot
Pick the shot in the scene that is best exposed, most representative and probably on
screen longest (often the wide or main single). Grade it to the scene's intended
feel. Grab a still. Everything else matches to it.

## 3. Match: scopes then eyes
1. **Exposure/contrast:** on the waveform, compare black floor, key face level and
   highlights against the hero (split the viewer with the reference still, or use a wipe).
   Match the face level first; viewers judge by faces.
2. **Balance:** on the RGB parade, compare channel heights in neutral areas. Small offsets
   in shadows (lift) and highlights (gain) remove casts that camera models and lights introduce.
3. **Saturation:** vectorscope spread vs hero.
4. Then **eye check** in sequence, full screen, playing — not paused. Back-and-forth between
   adjacent shots; trust the cut, not the side-by-side.

## 4. Skin tones
- On the vectorscope, healthy skin of all complexions tends to cluster near the
  **skin-tone indicator line** (between red and yellow); complexion changes the
  saturation/brightness much more than the hue. Use it as a guide for hue drift, not a
  rule — some looks push skin deliberately.
- Isolate faces (qualifier on skin hues + a soft window) on a parallel node to correct
  hue/saturation without shifting the background. Keep qualifiers soft to avoid edges and
  chatter; check in motion.
- Mixed lighting (window daylight + tungsten practical + green-tinted LEDs) puts different
  casts on one face; correct the dominant cast globally, then fix the face locally.
- Different camera sensors render skin differently (one redder, another more yellow-green).
  Match skin to the hero camera specifically, after the global balance.
- Don't over-smooth or over-saturate skin; check on a calibrated reference monitor.

## 5. Then the look
Apply the creative look **after** matching, on a common node/group for the whole scene,
so one adjustment affects all shots equally. If the look breaks a shot (clipping, noise),
fix that shot's balance underneath rather than making a different look.

## 6. Moving light and continuity
For a scene shot as the sun moved, decide whether time should progress (allow a gradual
shift) or be frozen (match all to hero). Clouds passing within a shot may need a keyframed
or dynamic exposure correction.

## Gotchas
- Matching on a paused frame with different content — compare similar elements (faces to faces).
- Matching with a display LUT on one camera and not another.
- Chasing tiny scope differences the eye can't see in motion.
- Grading from the edit's order of discovery instead of building the scene's hero first.

## Verify
- [ ] All cameras in one working space with correct input transforms.
- [ ] Hero shot graded and stilled; every shot matched to it on waveform, parade, vectorscope.
- [ ] Skin tones consistent across cameras and sit naturally (near the skin line unless stylised).
- [ ] Look applied scene-wide after matching.
- [ ] Scene plays without visible jumps at full speed on a reference monitor.
