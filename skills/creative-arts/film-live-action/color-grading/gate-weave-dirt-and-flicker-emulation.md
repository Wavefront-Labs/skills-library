---
id: creative-arts.film-live-action.color-grading.gate-weave-dirt-and-flicker-emulation
name: gate-weave-dirt-and-flicker-emulation
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, gate-weave-effect, dirt-overlay, flicker-emulation, film-emulation, gate-weave, film-damage, dust-and-scratches, film-flicker, scanned-dust-plates, film-look-creator, fusion, davinci-resolve, period-look]
level: practitioner
status: draft
description: "Emulate film projection artefacts digitally: subtle gate weave, dust and dirt overlays from scanned plates, and exposure flicker, kept believable and consistent across a show."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/color (Blackmagic - Resolve Film Look Creator and ResolveFX Film Damage)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Blackmagic - Colorist Guide to DaVinci Resolve)"
  - "https://www.dehancer.com/ (Dehancer - film emulation with gate weave and dust)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gate weave, dirt and flicker emulation

**Goal:** digital footage that reads as projected or scanned film (period flashback,
home movie, a full stylised look) without looking like a cheap preset.

## 1. Decide what kind of film it was
Different sources have different artefacts. Pick one and be consistent:
- **Pristine modern 35mm print**: almost invisible weave, rare dust, no flicker.
- **Worn release print / 1970s TV**: visible dust and occasional scratches, mild weave.
- **8mm/16mm home movie**: strong weave, heavy dirt, flicker, vignette, soft edges.

## 2. Gate weave
- Film moves slightly in the gate: slow, low-frequency position drift, mostly vertical,
  a fraction of a pixel to a couple of pixels at HD for 35mm; more for 8mm.
- Resolve: *Film Look Creator* (Gate Weave controls) or Dehancer; or in Fusion a
  Transform with a Perturb modifier on Center (low speed, tiny strength).
- Apply weave **after** grading but **before** titles and any frame lines; titles must
  stay steady (they were often added optically, but audiences read wobbling subtitles
  as an error).
- Oversize 2-3% or use edge-extend so frame edges never show.

## 3. Dirt and dust
- Best source: **scanned dust/scratch plates** (real film shot through a scanner on
  black or clear). Composite on top:
  - Dirt on the **negative** prints **white** on screen: Screen or Add the plate.
  - Dirt on the **print** shows **black**: Multiply an inverted plate.
- Procedural option: ResolveFX *Film Damage* (dirt, scratches, blur); keep density low.
- Vary plates per shot (offset start frame) so the same speck doesn't repeat on every cut.
- Big hairs or scratches only where they serve the moment.

## 4. Flicker
- Exposure flicker from uneven shutter/processing: small random gain changes (a few
  percent), frame-to-frame, sometimes slightly per channel.
- Fusion: Brightness/Contrast gain driven by a Perturb modifier; or a Film Look
  Creator/plugin flicker control. Keep it below the threshold where it becomes
  photosensitivity-risky; run the photosensitivity (Harding) check on strong flicker.

## 5. Order of operations
Normalise > grade > film print emulation > halation > **weave** > **flicker** > grain >
**dirt** > titles. Save as a shared node tree or PowerGrade for the whole sequence.

## Gotchas
- Too much of everything - the "Instagram filter" look. Set levels on a large screen
  at full speed, then back off.
- Dirt on the same frame-locked plate across cuts: identical specks give it away.
- Weave applied before stabilisation or tracked VFX breaks the track.
- Noise reduction placed after the dirt erases the dirt and smears grain.

## Verify
- [ ] One defined source film type for the look, written in the look notes.
- [ ] No exposed frame edges from weave; titles steady.
- [ ] Dirt plates varied across cuts.
- [ ] Flicker passes the photosensitivity check.
