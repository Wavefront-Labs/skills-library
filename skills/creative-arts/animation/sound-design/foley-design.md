---
id: creative-arts.animation.sound-design.foley-design
name: foley-design
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, foley, footsteps, cloth, props, diegetic, sync, layering, field-recording, reaper, ffmpeg, free-tools, foley-editing]
level: advanced
status: draft
description: "Create/source foley for an animated show with free local tools: footsteps, cloth, props, diegetic counter blips, synced and layered to picture."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Foley design (performed sound, free and local)

**Goal:** give the production the layer of human, physical, synced sound that makes
an animated world feel inhabited — every footfall, cloth rustle, prop handle and
the diegetic engagement-counter blip, created or sourced with free/local means
(a USB mic, a quiet room, Reaper/Audacity, ffmpeg) and cut to picture. Foley is
the *performed, picture-synced* layer; broad designed effects and stylized hits
are `sfx-design`, room tone and backgrounds are `ambience-beds`, and the balance
of all of it is `final-mix`.

## The three foley families (Hollywood's split, still the right model)

1. **Feet** — every footstep, matched to surface (concrete alley, wood floor,
   metal catwalk) and weight/gait of the character.
2. **Moves / cloth** — the rustle a body makes moving: jacket, straps, a sleeve
   dragging a table. Low-level but it's what kills the "floating puppet" feel.
3. **Props / specifics** — anything handled or hit: a mug set down, a door, a
   switch, a casing tapping a surface. The hero, picture-locked hits.

Separate them because they mix differently (feet and props carry; cloth sits low)
and because you'll layer and process each family its own way.

## Record vs library — decide per cue

- **Record** when the action is specific and hero (a signature prop, the
  screen-face casing tapping glass, a character's particular walk). Performed-to-
  picture foley syncs and *acts* in a way a library grab never will.
- **Library** when it's generic and buried (distant footsteps, a nondescript
  cloth move). Use **CC0/public-domain** sources only for a commercial show:
  freesound.org (filter to CC0), and your own recorded library. Log the licence
  of every imported clip (see `asset-management`'s manifest discipline) — a
  CC-BY clip with a missed attribution is a legal problem at scale.

## Recording foley on a budget

You do not need a foley stage. You need a quiet room and discipline.

- **Mic:** any decent cardioident USB/XLR mic (even a dynamic) close-miked, ~15–25
  cm, pointed at the sound, off-axis from your mouth so you don't breathe into it.
- **Room:** kill reflections — record in a closet of clothes, or drape blankets.
  You want dry foley; reverb is added later per location and can't be removed.
- **Level:** peak around −12 to −6 dBFS, 48 kHz / 24-bit. Headroom for the
  transient; 24-bit means a quiet cloth move still has bits to spare.
- **Props kit:** the classic cheats work — cornstarch in a leather pouch for
  snow/crunch, a pair of shoes on a board tray for feet, gloves for cloth,
  coconut/wood for impacts, celery for breaks. Build a small surfaces tray
  (concrete offcut, wood plank, sheet metal) for feet.
- **Perform to picture:** loop the shot, watch the contact frames, perform in
  time. Record several takes in one pass; pick in the edit.

## Syncing to action (the craft)

Animation gives you exact contact frames — use them.

- **Feet:** the sound hits on the **contact frame**, not the lift. At 24 fps a
  frame is ~42 ms; a footstep landing one frame late reads as "dubbed." Zoom the
  waveform and snap the transient to the contact frame.
- **Anticipation:** a small pre-sound (cloth shift, weight transfer) a frame or
  two *before* a big move sells the physics — mirror the animation's anticipation
  from `twelve-principles`.
- **Weight = level + low end + a second layer.** A heavy character's step is
  louder, has more low-frequency thud, and often a secondary scuff/settle. A light
  character is a single higher transient. Don't just reuse one footstep at one
  level.
- **Vary everything.** Never paste the identical footstep twice — rotate 4–6
  variants and nudge pitch/level per step, or it reads as a machine gun. In Reaper,
  a folder of variants on one track, randomized, does this.

## Layering (depth per cue)

A convincing foley hit is usually 2–3 layered elements:

- **Footstep** = heel contact (transient) + sole/weight (body) + optional scuff
  or grit (surface character). Three clips, aligned on the transient, summed.
- **Prop set-down** = the contact tick + the material body (ceramic ring, metal
  resonance) + a tiny settle.
- **The engagement-counter blip** (diegetic UI, `hud-engagement-counter`) = a
  short synthesized tone + a subtle digital tick on the digit flip + the analog
  flicker modulating its level. Because it's *diegetic* (the characters' world
  emits it) it gets foley-treated — placed in space, ducked under dialogue,
  reverbed to the room — not left as a dry UI beep. Keep a locked palette of blip
  variants (idle tick, increment, milestone) so the counter sounds consistent
  across all 10 episodes (consistency law, `asset-management`).

## A surfaces/weight matrix (plan before you record)

Foley scales when you record a *grid*, not one-offs. Before a session, list the
surfaces the show actually uses and the weights of the cast, and capture the
cross-product once:

| surface  | light char | medium char | heavy char | prop body |
|----------|-----------|-------------|-----------|-----------|
| concrete | soft tick | tick + body | thud + grit | ceramic ring |
| wood     | tap       | tap + creak | boom + creak | hollow knock |
| metal    | ping      | ping + ring | clang + ring | resonant tap |

Record 4–6 variants per cell in one pass. That one afternoon covers most of the
series' feet and prop bodies; episode-to-episode you're picking from the library,
not re-recording, which is also what keeps the show's footfalls *consistent*
(the same Alley-concrete set across all 10 episodes, `asset-management`).

## Processing foley (making it sit)

In Reaper/Audacity + free plugins (ReaEQ, ReaComp, ReaVerbate, or Airwindows):

- **High-pass** everything 60–100 Hz to clear mic rumble and room thump (except
  deliberate heavy thuds).
- **Transient shaping / light compression** to control the peak and bring up the
  body so a quiet move survives the mix.
- **EQ to surface:** footsteps on metal get a resonant midrange bump; on wood a
  warmer low-mid; on concrete a drier, flatter curve.
- **Match the space:** send foley to the shot's location reverb (short, dry for a
  small room; longer for the catwalk/alley) so performed-dry foley sits in the
  same room as the dialogue and ambience. This is the single biggest
  "does it belong" factor.
- **Pan to picture:** a prop on screen-left is panned left; feet crossing frame
  pan across. Keep it subtle — foley supports, it doesn't gimmick.

## Organizing for 10 episodes

- One Reaper session per shot/scene with stems: `FEET`, `CLOTH`, `PROPS`, `UI`.
  These become the foley stem handed to `final-mix`.
- A versioned, licence-logged foley **library** of your recorded variants (feet by
  surface, cloth by weight, prop hits) so episode 7 reuses episode 1's shoe-on-
  concrete set and the show sounds continuous.
- Deliver each scene's foley as a single pre-mixed stem (48 kHz/24-bit WAV) plus
  the session, so the mix can rebalance without re-foleying.

## Reading the animation for foley

Animated foley has an advantage film foley doesn't: the performance is on exposure
sheets and curves, not a moving actor you chase. Before recording, step through
the shot and mark the **contact and accent frames** — every footfall, every
hand-to-prop, every settle, plus the anticipation frame before a big move. That
marked list is your foley cue sheet; you perform to it instead of guessing. Watch
the animation's spacing too: fast spacing (few in-between frames) wants a sharp
transient; slow, cushioned spacing wants a softer, rounder sound. Foley that
mirrors the animation's timing and weight (the `twelve-principles` reading of the
shot) is what makes a drawn character feel like it has mass.

## Gotchas

- **One-frame-late sync** is the most common tell; always snap to the contact
  frame, not "close enough."
- **Identical repeated clips** read as fake — rotate variants.
- **Over-foleying** — not every movement needs a sound; too much foley is as
  fake as none. Foley what the eye lands on.
- **Dry foley in a wet world** — un-reverbed foley floats above ambience that has
  room; always send foley to the location space.
- **Clipped transients** from recording too hot can't be fixed — re-record;
  foley lives on clean transients.
- **Licence drift** — a non-CC0 library grab slipped into a commercial series is a
  real liability; log every source clip's licence.

## Verify

1. Solo the FEET stem against picture at 24 fps: every footstep transient sits on
   the character's contact frame (zoom to the sample — within ~1 frame), and heavy
   vs light characters have audibly different weight.
2. Solo and A/B: no footstep/cloth/prop clip is the identical sample used twice in
   a row — variants rotate.
3. Mute all ambience and reverb sends: the foley is dry and clean (no room baked
   in). Enable the location reverb: the foley now sits in the same space as the
   dialogue.
4. Confirm the diegetic counter blip is panned/reverbed to its on-screen position
   and uses the locked blip palette (idle/increment/milestone), identical to a
   prior episode.
5. Check every imported library clip is logged CC0/public-domain with its source
   in the session notes/manifest.
