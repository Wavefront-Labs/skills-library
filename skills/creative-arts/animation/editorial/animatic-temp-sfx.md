---
id: creative-arts.animation.editorial.animatic-temp-sfx
name: animatic-temp-sfx
category: creative-arts
field: animation
product: editorial
tags: [animatic-sfx, temp-sfx, animatic, story-reel, temp-sound, sound-library, editorial-sound, track-layout]
level: practitioner
status: draft
description: "Cut temp sound effects into an animatic so gags and beats read in screenings, keep them on their own tracks, and stop temp SFX from becoming the final design brief."
sources:
  - https://www.routledge.com/Producing-Animation/Winder-Dowlatabadi-Miller-Zarneke/p/book/9781138479937
  - https://freesound.org/help/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temp sound effects in the animatic

**Goal:** a story reel that plays like a show. Silent boards make comedy die in screenings; a few well-placed
effects make timing judgments honest.

## What to cut

Only effects that carry story or timing: impacts that land a gag, a door that motivates a look, a phone ring that
starts a scene, a whoosh on a whip pan. Skip footsteps and cloth; they add noise and editorial time.

## Where they live

Use the editorial track layout (see `creative-arts.animation.editorial.editorial-track-layout`): temp SFX on their
own tracks (e.g. A5-A6), never mixed onto dialogue tracks. Name clips `TEMP_` so the AAF to sound
(see `creative-arts.animation.editorial.aaf-audio-turnover`) shows them as references, not deliverables.

## Sources

- The studio's licensed library, searched by metadata (see `creative-arts.animation.sound-design.sound-library-management`).
- CC0 libraries (Freesound CC0 filter) for the stylized-series pipeline; log the licence with each file.
- Mouth sounds by the editor are fine for a first reel.

## Levels

Dialogue at about -12 dBFS peaks; temp SFX sit under it except for hard gag hits. Normalise each temp effect with
clip gain, no plug-in chains on an animatic.

## The temp-love trap

Directors get used to temp sounds the same way they do to temp music
(see `creative-arts.animation.sound-design.music-edit-to-picture` for temp-track risk). In the spotting session
(`creative-arts.animation.editorial.spotting-sessions`) tell sound which temp effects are intent ("this hit must be
cartoony") and which are placeholders.

## Verify

Screen the animatic with temp SFX muted and unmuted: every effect you kept changes how a beat lands; any that
do not are removed.
