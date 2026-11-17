---
id: creative-arts.film-live-action.film-sound-design.ai-dialogue-tools
name: ai-dialogue-tools
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, dialogue-editing, ai-dialogue-tools, dxrevive-use, clarity-vx, dialogue-isolate, machine-learning-denoise, accentize, dxrevive, waves-clarity-vx, izotope-dialogue-isolate, goyo, voice-cloning, digital-replica, dialogue-restoration]
level: practitioner
status: draft
description: "Use machine-learning dialogue tools well: Dialogue Isolate, Clarity Vx, DxRevive and similar for noise, reverb and bandwidth repair, plus artefact checks and voice-replica consent limits."
sources:
  - "https://www.waves.com/plugins/clarity-vx-pro (Waves - Clarity Vx / Vx Pro)"
  - "https://www.accentize.com/dxrevive/ (Accentize - dxRevive)"
  - "https://www.izotope.com/en/products/rx.html (iZotope RX - Dialogue Isolate)"
  - "https://www.sagaftra.org/ (SAG-AFTRA - AI and digital replica provisions)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI dialogue tools

**Goal:** rescue dialogue that conventional noise reduction can't (heavy background,
reverb, thin lav or phone audio) while keeping the actor's voice intact and the scene
consistent.

## 1. What they do
| Tool (examples) | Job |
|---|---|
| iZotope RX **Dialogue Isolate**, Waves **Clarity Vx/Vx Pro**, Supertone Goyo-type tools | Separate voice from noise/music/reverb; real-time or offline |
| Accentize **dxRevive** | Restore missing bandwidth and studio-like timbre to degraded dialogue (phone, lav, compressed) |
| Dialogue de-reverb modules (RX Dialogue De-reverb, Clarity Vx DeReverb, others) | Reduce room ambience |
Versions change fast; trial on your own material before committing a show to one.

## 2. Workflow
- **Edit first**, process second: do the dialogue edit and fills on raw material, then
  process per scene/mic so edits match.
- Use the **lightest** setting that solves the problem; most tools have a mix/amount
  control - blend some original back to keep natural texture.
- Process consistently across a scene (same tool, similar amount); otherwise shot
  changes become obvious.
- After separation, fill: isolated dialogue leaves holes between words; lay matching
  (also lightly processed) room tone so cuts don't drop to digital silence.
- Keep unprocessed tracks on mute below for the mixer.

## 3. Listen for artefacts
- Watery/warbly tails, consonants (s, t, f) eaten, breaths removed, pitch "robot"
  sound, voice timbre change (especially with bandwidth restoration making voices sound
  like a different mic or person).
- Check on headphones **and** at mix level on speakers; artefacts hide in the edit room.
- Compare with production in context, not soloed.

## 4. Limits and ethics
- If a line is unsalvageable, ADR is still the answer.
- Generative **voice cloning/replacement** of a performer requires their consent and
  is governed by union agreements (e.g. SAG-AFTRA digital replica terms) and contracts;
  restoration tools that process the actor's own recording are different from
  generating new lines. Get production/legal sign-off for anything generative.
- Data: cloud tools upload unreleased dialogue; check the production's security policy.

## Gotchas
- Isolate at 100% in every scene: everything sounds like ADR in a dead room.
- Processing before the edit: fades/crossfades expose processed vs unprocessed seams.
- Different tool versions across editors: inconsistent results across reels.
- Removing intentional sounds (efforts, PFX) along with noise.

## Verify
- [ ] Processing consistent within each scene; amount blended, not maximum.
- [ ] Fills under processed dialogue; no dropouts to silence.
- [ ] Artefact check on speakers at mix level.
- [ ] No generative voice use without documented consent.
