---
id: creative-arts.animation.methods.stylized-series-tier
name: stylized-series-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, stylized, series, rick-and-morty, murder-drones, quality-tier, blender, eevee, cel, solo, indie, ordering, gates, acceptance-criteria]
level: advanced
status: verified
description: "Recipe: which skills to combine, in what order, with which measured gates, to reach Rick-and-Morty / Murder-Drones tier on one machine."
sources: []
licence: Apache-2.0
version: 8
updated: 2026-11-17
aliases: []
---

# Method: stylized-series tier (R&M / Murder Drones) on one machine

A **method** is a recipe, not a technique. Skills are the ingredients; this says which
ones to combine, in what order, and how you know each step is done. It owns no
technique of its own — every "how" below is a link to the skill that carries it.

**Outcome:** a 6–8 minute cel-shaded episode that reads as a finished stylized series,
produced by one person plus automation on a single workstation.

**Lesson (v7, verified 21 Oct 2026).** After 22 cuts the 3D route below (Quaternius
base meshes + EEVEE cel shading + Freestyle outlines + painted plates) hit every
measured gate and was still judged by the owner as "not visually appealing, not even
Rick and Morty level". The gap was character appeal, which this method cannot buy
with tuning: outlined 3D bases do not read as drawn characters. For drawn appeal use
`creative-arts.animation.methods.anime-dialogue-2d-tier` (one master still, traced,
parametric face, 2D puppet); keep this method for the pipeline, plates, VO, QC and
FX phases, which carry over unchanged.

**This tier is reachable.** It is bound by art direction and craft, not by compute.
The tier that is *not* reachable this way is in
`creative-arts.animation.methods.feature-cg-tier` — read it before anyone
proposes "Disney quality", because the reason is arithmetic, not effort.

---

## Ingredients (the skills this bundles)

| Phase | Skill |
|---|---|
| Story | `creative-arts.animation.storywriting.novel-to-teleplay` |
| Story | `creative-arts.animation.storywriting.shotlist-boarding` |
| Story | `creative-arts.animation.editing.animatic-assembly` |
| Plan | `creative-arts.animation.pipeline.shot-episode-structure` |
| Plan | `creative-arts.animation.pipeline.producing-scheduling` |
| System | `creative-arts.animation.pipeline.pipeline-architecture` |
| Assets | `creative-arts.animation.pipeline.asset-sourcing` |
| Assets | `creative-arts.animation.pipeline.asset-management` |
| Assets | `creative-arts.animation.pipeline.character-consistency` |
| Character | `creative-arts.animation.blender.mocap-retarget` |
| Character | `creative-arts.animation.blender.facial-rig` |
| Character | `creative-arts.animation.blender.blendshape-sculpting` |
| Sets | `creative-arts.animation.environment-design.set-building` |
| Sets | `creative-arts.animation.production-design.set-dressing` |
| Staging | `creative-arts.animation.blender.camera-cinematography` |
| Look | `creative-arts.animation.art-direction.color-script` |
| Look | `creative-arts.animation.blender.cel-shading` |
| Look | `creative-arts.animation.blender.lighting` |
| Look | `creative-arts.animation.blender.multipass-compositing` |
| Look | `creative-arts.animation.blender.compositing-grade` |
| Voice | `creative-arts.animation.voice-tts.voice-casting-consistency` |
| Voice | `creative-arts.animation.voice-tts.voice-direction` |
| Voice | `creative-arts.animation.pipeline.vo-lipsync-pipeline` |
| Render | `creative-arts.animation.pipeline.render-preflight` |
| Render | `creative-arts.animation.pipeline.shot-renderer` |
| Review | `creative-arts.animation.pipeline.dailies-review` |
| Review | `creative-arts.animation.pipeline.episode-qc-cold-viewer` |
| Review | `creative-arts.animation.blender.technical-animation-finaling` |
| Performance | `creative-arts.animation.blender.story-props-staging` |
| Audio post | `creative-arts.animation.sound-design.scoring` |
| Audio post | `creative-arts.animation.sound-design.sfx-design` |
| Audio post | `creative-arts.animation.sound-design.ambience-beds` |
| Audio post | `creative-arts.animation.sound-design.final-mix` |
| Deliver | `creative-arts.animation.encode-delivery.youtube-master` |
| Deliver | `creative-arts.animation.encode-delivery.probe` |

---

## The ordering law

**Dependency order, not importance order.** Each phase below is blocked by the one
above it. The single most common way this method fails is doing look-development on
assets that are about to be replaced.

Within that, spend the quality budget **where the eye goes**: faces, compositing,
silhouette, motion. That priority — not asset fidelity — is why the reference shows
read far above their asset budgets.

---

## Phase 0 — Story to animatic (before any 3D)

Script from the source material (`novel-to-teleplay`), shotlist with per-shot action /
emotion / line ids (`shotlist-boarding`), then a timed animatic cut to the scratch VO
(`animatic-assembly`). The animatic is the cheapest place an episode can fail; every
later phase inherits its timing.

**Gate:** the animatic plays at target runtime ±10% and every story beat lands inside
a numbered shot. No shot exists that the animatic does not justify.

## Phase 1 — Structure (before any pixel)

Shotlist JSON is the single source of truth (`pipeline-architecture`). Every shot
carries id, location, size, cast, duration, action text, emotion, line id.

**Gate:** every shot resolves to an existing set and cast id, or is explicitly queued
as missing. No rendering begins while the gate is red.

## Phase 2 — Source the assets (never model from primitives)

`asset-sourcing`. Humans and props assembled from spheres and cubes have a hard
ceiling at blockout tier that **no amount of lighting, comp or animation rescues**.
Start from an open-licence base mesh or kitbash pack.

**Gate:** a licence-cleared row exists for every asset (`asset-management`). Nothing
enters production uncatalogued.

## Phase 3 — Characters, rigged (the hard dependency)

Build on a base character that is **already skinned to a skeleton shared with an
animation library**; that sharing is what makes retarget free (`mocap-retarget`).
Then the facial rig (`facial-rig`, `blendshape-sculpting`).

**Gate — numeric, not visual:** sample a limb bone's matrix at two frames and assert
it changed; sample the evaluated face mesh between two emotions and assert it moved.
A silently unbound action and a correctly-built character that happens to be standing
still are *pixel-identical*. Never accept a render as proof of rigging.

## Phase 4 — Sets

Kitbash the shells from CC0 kits. Dressing props around a box does not fix the box:
the shell is what the frame reads. Layer **foreground / midground / background** —
a frame with nothing in front of the subject has no depth cue at all.

**Gate:** nothing solid sits between the camera's widest pull-back and the cast.
Compute that distance from the shot-size table rather than eyeballing it.

## Phase 5 — Performance from the shot data

Map each shot's **action text** to a locomotion clip, dialogue to a talking idle,
visemes to the face rig, and desync blinks per character. This is the step that
removes near-static frames; procedural bobbing is not a substitute.

**Gate:** measure it. Frame-difference the cut and require near-static frames below
~3%, with no frozen stretch over ~1.5s.

**Second gate — the beat's objects exist** (`story-props-staging`): every hand-prop
noun in the action text resolves to a placed prop, and every sequence-level
choreography the script describes (heads turning on a bell, lights popping in a wave)
is staged with extras and keyed lights. A line whose referent never renders reads as
a random word, however well it is written.

## Phase 6 — Voice

`vo-lipsync-pipeline`, `voice-casting-consistency`. Cast distinct speakers; measure
prosody rather than trusting the ear — pitch span over one sentence separates a
robotic engine from a usable one by roughly 2x. If a deterministic engine reads flat,
upgrade prosody WITHOUT recasting: clone the better engine from reference clips
synthesized by the locked voices (see voice-casting-consistency §6b), map shotlist
emotion onto the engine's expression params, and re-run lip-sync cues on the new audio.

**Gate:** every line fits its shot budget (re-check after any recast); every line
produces voiced lip-sync cues.

## Phase 7 — Look: pick the branch your benchmark is in (they are opposites)

"Rick & Morty / Murder Drones tier" names two different looks. Measured side by side
(instruments in Phase 7.0), they disagree on every axis: R&M is bright, flat and
crisp; MD is low-key, shaded and atmospheric. A pipeline tuned to MD's look (fog,
AO, haze, bloom, DOF, dark grade) scored 0.31x R&M's background sharpness, 0.41x its
brightness and 3.5x its deep shadow, and the owner's read was "badly drawn
characters, blurry backgrounds". Choose the branch from the benchmark, then tune.

### 7.0 Study the benchmark with instruments, not adjectives

Download one full official episode (the network's own channel) for private reference
and take the same numbers from it and from your cut:
- **Cuts per minute and median shot length** — ffmpeg `scdet` (threshold ~12) on a
  480 px copy. R&M measured 14.8 cuts/min, median shot 3.0 s.
- **Unique drawings per second** — `mpdecimate` (hi=768, lo=320, frac=0.33) over 60 s
  of dialogue, count surviving frames. R&M ~14/s (twos with holds). A 3D render on
  ones with camera drift measures 19–23/s and reads as floaty 3D, not drawn.
- **Look** — per frame: flat-fill share, background-band edge strength (sharpness),
  mean luma, deep-shadow share, thin-dark-line share. Average 24 spaced frames each.
- **A side-by-side sheet** of 24 benchmark frames next to yours. The numbers say how
  far; the sheet says what (layout, eyes, hands, line weight).

### 7a. Flat 2D TV branch (Rick & Morty class)

`freestyle`, `cel-shading`. Applied at render time as one pass, so every set and
character converts without rebuilding assets:
- **Two tones only**: cel ramp to shadow 0.78 / lit 1.0 with the terminator late
  (~0.12). A three-step ramp on low-poly faces draws blotchy terminators across skin
  and muscles through shirts; that is the "badly drawn" read. Zero any procedural
  noise / floor-grime mix in the materials.
- **One line on everything**: inverted-hull outlines off; Freestyle on with silhouette,
  border, crease (~100°: box corners yes, low-poly face facets no — 128° drew every
  facet as a wrinkle) and material-boundary edges; one absolute weight (~1.6 px at
  1080p), warm near-black. Hull outlines are thick, uneven and characters-only;
  R&M's line is the same weight on a cup as on a face.
- **No lens**: no DOF, fog, AO multiply, chromatic aberration, vignette or grain; keep
  only a small emission glow for screens. No rim light or face fill — on flat fills
  they only paint a light pool on the back wall.
- **On twos**: render every second frame (`frame_step = 2`) and hold each for two at
  assembly (an ffmpeg concat list with per-file `duration`). Matches the benchmark's
  drawing rate and halves render time.
- **Locked cameras**: per location, a master at eye level square to the set for
  WIDE/MED, and a single angled ~14° in from the speaker's side for CLOSE (shot /
  reverse-shot). Per-shot random orbit, height and rule-of-thirds offsets make every
  cut a new camera; the benchmark holds a handful of setups per scene.
- **Character read**: white eye discs with a small black dot pupil, sitting ON the
  white's front surface (an iris placed inside the white only ever showed through
  the old hull), red-brown mouth interior, shorter cartoon fingers.
- **Rooms laid out like rooms** — `set-dressing` §"Interiors are laid out, not scattered": one kit scale, runs
  flush to walls, uppers over counters, nothing random.

**Gate:** look metrics within ~25 % of the benchmark on sharpness, brightness and
shadow share; drawings/s within ±3 of the benchmark; side-by-side sheet reviewed.

### 7b. 3D cel with comp branch (Murder Drones class)

`multipass-compositing`, `compositing-grade`. A single flat beauty pass is *the*
blockout read. Enable AO / mist / depth / emission; multiply AO back for contact
shading (cel shading produces none, so characters look pasted on), mix toward a fog
colour by mist for atmospheric perspective, and halate the emission pass only.

**Gate:** calibrate fog on renders. Too strong flattens the whole frame instead of
separating distance.

Enforce the colour script here, per LOCATION, as a fixed table of fog colour + LGG
lift/gain keyed off the set — not per-shot hand values. Fog alone cannot carry a
palette at normal set depths (quadratic mist at 40 m leaves an 11 m backdrop ~4%
fogged); the location's colour lives mostly in the LGG gain. One cool default grade
washed an entire gold-brief town blue-grey.

**Gate:** a contact sheet per location visibly matches its colour-script swatch.

## Phase 8 — Render, gated

`render-preflight` then a one-frame-per-shot proof strip, then the full render
(`shot-renderer`). Never reverse this: preflight costs seconds, a proof strip costs
minutes, a bad full render costs a day.

**Gate:** 0 FAIL in preflight; proof strip reviewed shot-by-shot (`dailies-review`).

## Phase 9 — Audio post (score, SFX, ambience, mix)

`scoring` (motif per location/character, stems the mix can duck), `sfx-design` +
`ambience-beds` (every on-screen event and every room has a sound; silence is a
decision, not a gap), then `final-mix` with dialogue as the anchor.

**Gate:** dialogue intelligible at every point against score+ambience; mix hits the
platform loudness target (for YouTube, around −14 LUFS integrated); no clipping.

## Phase 10 — Assembly and delivery

Concatenate per-shot clips into the episode. **Normalise every clip's audio params
before concat** — mixed sample formats/rates corrupt AAC decode at the join. Then the
platform master (`youtube-master`) and verify the file itself (`probe`), not the NLE
preview.

**Gate:** the delivered file probes clean end to end (duration, streams, sync) and
plays through on a machine that did not render it.

---

## Phase 11 — Cold-viewer episode QC (the gate that shot gates cannot replace)

`episode-qc-cold-viewer`. Every phase above is per-shot or per-department; all of
them were green on a cut whose owner review was "can't tell what they're talking
about, hands incomplete, people stuck in walls, hearing a voice while looking at a
wall". Watch the whole cut with sound beside a benchmark episode of the target show
and fill the scorecard: comprehension paragraph vs synopsis, lines whose referent
never rendered, speaker off-frame while talking, action beats missing their prop,
hands/mouth/face-motion per cast member, clipping, tearing, WIDE object count vs
benchmark.

**Gate:** every scorecard row filled with counts and timestamps; zero red rows. A
probe, a decode and a contact sheet are container proof and do not satisfy this gate.
Run it as the loop in that skill: scripted rows, versioned cards diffed per run,
finaling rows from the renderer, every closed row written back to the skill that
should have caught it.

## Acceptance criteria for the tier

- near-static frames < 3%; no frozen stretch > 1.5s
- every character deforms (asserted numerically, not by eye)
- every frame has foreground/midground/background separation
- faces carry brow + mouth + blink motion in every close-up
- comp has at least AO + depth-haze + grain; never a raw beauty pass
- audio normalised per clip before concatenation
- score + SFX + ambience present; dialogue-anchored mix at platform loudness
- delivered master probes clean (streams, duration, sync)
- the next tier up is `premium-stylized-tier` — go there only after every criterion
  above holds on a full episode, not before

## Failure modes this method exists to prevent

1. **Look-dev before rigging.** Lighting a character that cannot move.
2. **Trusting renders over measurement.** Rest-pose and still-acting look identical.
3. **Dressing instead of rebuilding.** Props around a box still read as a box.
4. **Chasing feature-CG fidelity.** See `method-feature-cg-tier`; it is compute-bound.
5. **Rendering before preflight.** Discovering a defect after a day of frames.
6. **Building a set from its NAME, not its sequence.** Read every shot that plays on a
   set before building it — a location called after a street was built as an interior
   room, and every WIDE in that sequence rendered an empty box. The shot list, not the
   set list, defines what a set is.
7. **Fixing a bug in one pass and not its siblings.** The per-slot atlas restyle was
   fixed in the shell pass and recurred identically in the dress pass. A material/scale
   bug class lives in every pass that touches materials/scale; grep for the pattern.

## Verify

Re-read a finished cut against the acceptance list above with numbers in hand, not
impressions. If any figure is missing, the step was not actually done.
