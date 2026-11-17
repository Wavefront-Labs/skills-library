---
id: creative-arts.film-live-action.film-sound-design.mix-session-template-and-routing
name: mix-session-template-and-routing
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, re-recording-mix, mix-template, mix-routing, mix-session-setup, pro-tools-template, stems, stem-routing, print-tracks, vca, folder-tracks, dolby-atmos-renderer, beds-and-objects, io-setup, dx-mx-fx]
level: advanced
status: draft
description: "Build a Pro Tools re-recording mix template: track layout by stem, bus and VCA routing, print tracks for stems and printmaster, Atmos bed/object paths and I/O naming that survives every reel."
sources:
  - "https://www.avid.com/pro-tools (Avid Pro Tools - I/O setup, folder tracks, VCAs, session templates)"
  - "https://professional.dolby.com/content-creation/dolby-atmos/ (Dolby - Atmos Renderer, beds and objects)"
  - "https://www.mpse.org/ (Motion Picture Sound Editors - re-recording mix practice)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mix session template and routing

**Goal:** one template every reel and episode opens into, where every edited track
lands on the right stem, stems print in one pass, and nothing is routed by hand at 2 am.

## 1. Stem plan first
Write the delivery stem list from the spec (e.g. DX, MX, FX, plus BG/FOL splits, VO,
and the printmaster), and the format (5.1, 7.1, 7.1.2 bed + objects). The template is
built backwards from this.

## 2. Track layout (top to bottom)
- **DX** folder: dialogue A-F, PFX, ADR, group; fills.
- **MX** folder: score stems, source music.
- **FX** folders: BG, hard FX, design, foley (feet, moves, specs).
- **Busses/aux** per stem (DX bus, MX bus, FX bus, etc.) in the mix width.
- **Print/record tracks**: one per stem plus printmaster, record-armed for the final pass.
Colour-code by stem; keep identical track names so editors' sessions import cleanly
(*Import Session Data* matching by name).

## 3. Routing
- Edit tracks > **stem aux/bus** > print tracks and > **main mix** bus > printmaster
  print track and monitor path. Stems must sum to the printmaster with no extra
  processing on the main bus (or apply that processing per stem).
- **VCAs** per stem (and per predub group) for riding levels without touching edit-track
  automation.
- Reverb/effect returns route to the stem they belong to (dialogue reverb returns to DX),
  never to the main bus, or stems won't sum.
- **Atmos**: beds route to the renderer's bed inputs; object tracks to object inputs
  with panner metadata; recent Pro Tools versions host the renderer internally,
  otherwise an external renderer over the network/Dante. Re-renders produce stems and
  the ADM master.

## 4. I/O and template hygiene
- *I/O Setup*: name busses by function (`DX 7.1.2`, `MX 7.1.2`); export the I/O settings
  with the template so other rooms load the same names.
- Save as a template (`.ptxt`) with markers for reel start/2-pop, a 1 kHz tone/ident track,
  loudness meter on the main path.
- Document the routing (one diagram in the session notes).

## Gotchas
- Reverb returns to the main bus: stems don't null against the printmaster.
- Bus processing (limiter on the main) not mirrored on stems: delivered stems differ.
- Track names that differ between editors' sessions and the template: import fails silently.
- Mismatched channel widths (5.1 aux feeding a 7.1 print track): channels missing.

## Verify
- [ ] Stems summed in a test session null against the printmaster.
- [ ] Every edit track lands on exactly one stem.
- [ ] Template opens in every mix room with the same I/O names.
- [ ] Atmos beds/objects reach the renderer; re-render produces the spec'd outputs.
