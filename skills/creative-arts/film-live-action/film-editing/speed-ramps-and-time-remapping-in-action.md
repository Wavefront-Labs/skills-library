---
id: creative-arts.film-live-action.film-editing.speed-ramps-and-time-remapping-in-action
name: speed-ramps-and-time-remapping-in-action
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, action-speed-ramp, time-remap-action, slow-mo-action, optical-flow, frame-blending, speed-ramp, retiming, timewarp]
level: practitioner
status: draft
description: "Build speed ramps and retimes for action: shooting rates that make it possible, frame sampling vs blending vs optical flow, ramp curves, and handing retimes to the online and VFX."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/time-remapping.html (Adobe Premiere Pro - Time Remapping)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve - Retime controls and Speed Warp)"
  - "https://www.avid.com/media-composer (Avid - Timewarp effects)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Speed ramps and time remapping in action

**Goal:** slow-motion and speed changes that hit the action beats cleanly, look smooth,
and survive the conform to the online.

## 1. What the footage allows
- Footage shot **overcranked** (48-120+ fps) can be slowed with real frames - smooth.
- Footage at base rate slowed below ~70-80% needs **interpolation**: frame blending
  (ghosting) or **optical flow** (Resolve Speed Warp, Premiere Optical Flow, Twixtor) -
  good on simple motion, artefacts on complex (crossing limbs, debris, motion blur).
- Speeding up is easy (frame skipping).

## 2. Building the ramp
- Premiere: **Time Remapping** (clip keyframes in the timeline; drag the speed line,
  split keyframes for ramps, ease curves).
- Resolve: **Retime Controls** (`Ctrl/Cmd+R`) with speed points and **Retime Curve**;
  processing per clip (Nearest, Frame Blend, Optical Flow/Speed Warp).
- Avid: **Timewarp** effect with speed/position graph.
- Ramp shape: real-time into the impact, ramp **down** to slow at the key moment, ramp **up**
  out to real time - ease the transitions over 6-12 frames for organic feel.
- Sync sound design to the retime (whooshes, low-frequency slow-down) - flag for sound.

## 3. Rhythm in action
- Use slow motion sparingly - on the beat that matters (impact, decision, reveal).
- A short slow beat after fast cutting lands harder; constant slow-mo loses impact.
- Freeze frames and speed-ups (undercrank feel) for comedy or chaos.

## 4. Conform and VFX
- Retimes must translate: XML/AAF carry basic speed effects; complex ramps often don't
  round-trip reliably between NLEs - export a **retime report** (speed curves, source
  frames) and a reference movie.
- Heavy optical-flow retimes in VFX shots should be done by VFX (they need the full
  frame range: hand them the source plate with handles and the curve).
- For the online in Resolve, check every retimed clip against the reference.

## Gotchas
- Optical flow artefacts (warping limbs) unnoticed until the big screen.
- Ramps lost in the AAF to the online.
- Overusing slow motion.
- Sound not adjusted; the retime feels fake.

## Verify
- [ ] Source frame rates known; interpolation method chosen per clip.
- [ ] Ramps eased; slow moments placed on key beats.
- [ ] Retime report and reference for conform/VFX.
- [ ] Retimed clips checked in the online.
