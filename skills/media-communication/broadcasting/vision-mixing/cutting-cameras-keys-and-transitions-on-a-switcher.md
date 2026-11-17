---
id: media-communication.broadcasting.vision-mixing.cutting-cameras-keys-and-transitions-on-a-switcher
name: cutting-cameras-keys-and-transitions-on-a-switcher
category: media-communication
field: broadcasting
product: vision-mixing
tags: [vision-mixing, vision-mixer, production-switcher, switcher, video-switcher, atem, blackmagic-atem, atem-software-control, tricaster, ross-carbonite, sony-switcher, grass-valley, program-bus, preview-bus, cut, auto-transition, mix, wipe, dsk, downstream-keyer, upstream-keyer, chroma-key, luma-key, lower-third, strap, media-player, macros, tally, multiview, live-production, broadcasting]
level: practitioner
status: draft
description: "Operate a production switcher (ATEM, TriCaster, broadcast panels) live: preview/program workflow, cutting to the director's calls, upstream vs downstream keys, transitions, macros and safe habits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cutting cameras, keys and transitions on a switcher

**Goal:** put the right picture on air at the exact moment the director calls it, with
graphics keyed cleanly — and never put something on air by accident.

## 1. The mental model (true on almost every switcher)
- **Program (PGM) bus:** what's on air now. Its tally light is red.
- **Preview (PVW) bus:** what's next. Tally often green.
- **CUT** swaps preview and program instantly. **AUTO/Take** runs the selected transition
  (mix/dissolve, wipe, DVE) at its set rate. The **T-bar** does the same manually.
- **Multiview** monitor shows all sources plus PVW and PGM — your main screen. Watch
  PGM and PVW; glance at sources.
- Larger switchers have multiple **M/E (mix/effects) banks** feeding each other; small
  ones (e.g. many ATEM Mini models) have one. Terminology varies by make: Blackmagic
  ATEM, NewTek/Vizrt TriCaster, Ross, Sony and Grass Valley all follow this model but label
  buttons differently.

## 2. Cutting to calls
- On **"standby 2"** select camera 2 on preview. On **"cut 2"** press CUT. Preparing on
  preview is the habit that prevents wrong-source accidents.
- **Hot-punching** directly on the program row is fast but risky; reserve it for
  experienced, fast-moving shows where your director expects it.
- Cut on action or on the end of a sentence; don't cut mid-word unless called.
- Before cutting, check the preview shot is **ready** (camera operator has framed and
  focused; tally will warn them when you go).

## 3. Transitions
- Default to **cuts**. Dissolves signal passage of time or a softer mood; use them when called.
- Set the **mix rate** in frames (e.g. 25 or 30 frames ≈ 1 second depending on your frame
  rate). Know your standard rate before the show.
- **Fade to black (FTB)** takes everything to black, including downstream keys on most
  switchers — use it at programme start/end, and know where the button is in an emergency.

## 4. Keys
- **Upstream keys (USK)** sit on an M/E and **transition with the background**: picture-in-
  picture, chroma-key (green screen), DVE boxes. When you cut cameras, a USK set to
  transition with the background may change too — check its "next transition" selection.
- **Downstream keys (DSK)** sit after the M/E and **stay on regardless of cuts**: lower
  thirds/straps, bugs/logos. Toggle them with their own CUT/AUTO buttons.
- **Luma key** keys out by brightness; **linear/key+fill** uses a separate alpha channel
  from the graphics system (best quality); **chroma key** removes a colour. Graphics from a
  CG system usually arrive as fill + key pair.
- Set **pre-multiplied** correctly for key+fill sources; a wrong setting gives dark or
  light fringes around graphics.

## 5. Media players, macros and shortcuts
- Load stills/clips into media players before the show; check the right frame is cued.
- **Macros** record button sequences (e.g. "intro: DSK logo on + cut to cam 1 + fade
  audio"). Build and test them in rehearsal; never edit macros mid-show.
- Label sources in software (e.g. ATEM Software Control) so multiview names match the
  director's language ("Cam 2 Wide").

## 6. Safe habits
- Keep your hand off the T-bar unless using it — a nudge starts a transition.
- After each take, set up the next likely shot on preview.
- Save the switcher state/config file before the show so you can restore it.
- If you put the wrong thing on air, cut back to the safe shot (usually the presenter
  wide) immediately; don't freeze.

## Verify
- [ ] All sources labelled and visible in multiview.
- [ ] Each call executed from preview with CUT/AUTO, not hot-punched by accident.
- [ ] DSK graphics stay up across cuts; USKs behave as expected on transition.
- [ ] Key fringes clean (pre-multiply set correctly).
- [ ] Macros tested in rehearsal; switcher state saved.
