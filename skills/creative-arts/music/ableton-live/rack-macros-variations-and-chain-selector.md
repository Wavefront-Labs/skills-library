---
id: creative-arts.music.ableton-live.rack-macros-variations-and-chain-selector
name: rack-macros-variations-and-chain-selector
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, instrument-rack, drum-rack, effect-rack, macro-variations, chain-selector, macros, macro-mapping, randomize-macros, zones, key-zones, velocity-zones]
level: practitioner
status: docs-checked
description: "Build Live racks for performance: grouping devices, mapping and naming macros, macro variations and randomisation, chain select zones, key and velocity zones."
sources:
  - https://www.ableton.com/en/live-manual/12/instrument-drum-and-effect-racks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rack macros, variations and the chain selector (Live)

**Goal:** one rack that holds many sounds or effect states, controlled by a few knobs.

## 1. Build the rack
- Right-click a device's title bar and choose **Group** (or **Group to Drum Rack**). The **Chain List** is the branching point for incoming signals.

## 2. Macros
- A Rack can have up to **16 Macro Controls**; a new Rack shows eight by default. View selector buttons change how many are visible.
- Turn on **Map Mode**: a **Map** button appears under each Macro dial. Map a parameter, then refine its range with the Min/Max sliders in the Mapping Browser. Set Min greater than Max, or right-click the entry and choose **Invert Range**, to invert.
- Macros can have custom names, colours and info text (Edit or context menu).

## 3. Macro Variations
- **New** stores the current macro state as a variation; the **Launch Macro Variation** button recalls one.
- The **Rand** button in the Rack title bar randomises mapped macros; the context-menu option **Exclude Macro from Randomization** protects a macro.
- A Show/Hide Macro Variations view selector button reveals the variations view.

## 4. Chain select zones
- The **Chain** button displays the Chain Select Editor, with a 0 to 127 Chain Select Ruler and a draggable chain selector indicator.
- Chain select zones let you filter chains with a single parameter.

## 5. Key and velocity zones
- With the **Key** button selected the Key Zone Editor appears. Instrument and MIDI Effect Racks also have velocity zones.
- Key zone fade ranges attenuate the velocities of notes entering a chain.

## Gotchas
- Check Min/Max when one macro drives several parameters, to avoid jumps.

## Verify
- Sweep each macro through its full range and recall each variation.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Instrument, Drum and Effect Racks (first 100,000 characters): Group commands, Chain List, 16 macros and default eight, Map Mode, Min/Max and Invert Range, naming, Variations New/Launch/Rand/Exclude, Chain Select Editor and 0-127 ruler, Key zones, velocity zones, fade ranges. Removed: Group shortcut, "Live 11+", mapping the chain selector to a macro, variation count, zone example numbers, freeze/flatten claim (not stated on the page).
Method: documentation only; no commands were run.
