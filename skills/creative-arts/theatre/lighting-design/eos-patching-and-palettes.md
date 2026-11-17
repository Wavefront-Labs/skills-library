---
id: creative-arts.theatre.lighting-design.eos-patching-and-palettes
name: eos-patching-and-palettes
category: creative-arts
field: theatre
product: lighting-design
tags: [theatre, lighting-design, eos, lighting-console, etc-eos, eos-patch, patch, palettes, presets, focus-palettes, colour-palettes, beam-palettes, intensity-palettes, showfile-backup, tracking-backup]
level: practitioner
status: draft
description: "Set up an ETC Eos showfile: patching channels to addresses and fixture types, building focus/colour/beam palettes and presets, and backing up the showfile."
sources:
  - "https://www.etcconnect.com/Products/Consoles/Eos-Family/"
  - "https://www.etcconnect.com/Support/Consoles/Eos-Family/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eos patching, palettes and backup

ETC Eos family (Eos, Ion, Element, Apex, Gio; Eos software v3.x). Syntax below is
command-line; check the Eos Family Operations Manual for your version.

## Patching
1. **[Displays] > Patch** (or Tab 100... Patch tab).
2. Select a channel, set **Type** (fixture library profile — e.g. ETC Source Four
   LED Series 2 Lustr, mode), **Address** (universe/address, e.g. `2/101`),
   label, position notes.
3. Command line examples: `Chan 101 Address 2/1 Enter` (patch channel 101 to
   universe 2 address 1); multi-patch ranges `Chan 101 Thru 110 Address 2/1 Enter`
   — Eos offsets addresses by the fixture footprint automatically.
4. Set **Attributes**: invert pan/tilt, swap, preheat, curve (e.g. dimmer curve),
   **proportional patch**, preferences per fixture.
5. Check DMX output on a fixture-by-fixture basis (Flash/High-light) before
   focus.

## Palettes and presets (reference data)
- **Palettes** store one category of data: **Intensity (IP), Focus (FP),
  Colour (CP), Beam (BP)**. Cues refer to palettes, so changing a palette
  updates every cue that uses it — essential for touring/refocus.
  - Example: select moving lights, position on the DSC chair, `Record Focus
    Palette 1 Label "DSC Chair" Enter`.
- **Presets** store multiple categories together (e.g. focus + colour + beam
  for a look).
- Palettes can be **by type** (different values per fixture type) — key for
  colour matching across LED types.
- Use **Update** (with "Trace"/"Cue Only" options) to modify palettes and cues
  correctly.

## Show file backup
- **Save** frequently (`File > Save`, or `[Shift]+[Update]`); Eos keeps
  autosaves; save versions with dates (`ShowName_2026-10-16_tech2`).
- Export to USB (`File > Save As > USB`) after every session; keep copies
  off-site/cloud.
- **Tracking backup**: a second console/RPU in backup mode synchronised with the
  primary, ready to take over; test failover in tech.

## Gotchas
- Wrong fixture mode (address footprint mismatch) — channels control wrong
  parameters.
- Recording hard values into cues instead of palettes — refocus nightmare.
- Saving only to the console's internal drive.

## Verify
- [ ] Patch checked fixture by fixture.
- [ ] Focus/colour palettes used in cues.
- [ ] Showfile exported to USB and cloud after each session; backup console tested.
