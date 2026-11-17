---
id: creative-arts.theatre.lighting-design.dmx-addressing-and-rdm
name: dmx-addressing-and-rdm
category: creative-arts
field: theatre
product: lighting-design
tags: [theatre, lighting-design, dmx, dmx512, dmx-addressing, universes, rdm, e1-11, e1-20, terminator, daisy-chain, splitter, fixture-footprint, dimmer-load, circuit-load]
level: practitioner
status: draft
description: "Plan DMX512 and RDM for a rig: universes and start addresses by footprint, cabling, splitters and termination, RDM discovery, plus dimmer and circuit load checks."
sources:
  - "https://tsp.esta.org/tsp/documents/published_docs.php"
  - "https://en.wikipedia.org/wiki/DMX512"
  - "https://en.wikipedia.org/wiki/RDM_(lighting)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DMX addressing and RDM

## DMX512-A (ANSI E1.11)
- One **universe** = 512 channels (slots), sent serially over a daisy-chained
  cable (5-pin XLR is the standard connector; 3-pin is common but non-standard).
- Each fixture reads a block of channels starting at its **start address**;
  block size = fixture **footprint** (mode-dependent, e.g. a dimmer 1 channel,
  an LED par 4-12, a moving light 20-40+).

## Addressing plan
1. List fixtures by universe with mode and footprint.
2. Assign start addresses so blocks don't overlap: next address = previous start
   + previous footprint. Leave gaps for additions.
3. Group logically (e.g. universe 1 dimmers, universe 2 LEDs, universe 3 movers)
   and match to cable runs.
4. Record in paperwork (Lightwright/Vectorworks) and on fixture labels.

## Cabling rules
- Daisy chain up to **32 devices** per line (electrical load), cable runs
  within a few hundred metres (spec allows up to ~300 m with good cable);
  more devices or branches need **opto-isolated splitters** (also isolates
  faults).
- **Terminate** the last device with a 120 Ω terminator to prevent reflections.
- Never "Y-split" DMX with a simple cable.
- Use DMX/data cable (110-120 Ω), not microphone cable.

## RDM (ANSI E1.20)
Remote Device Management runs bidirectionally on the DMX line: discover fixtures,
read and **set addresses and modes remotely**, check lamp hours/temperatures and
errors. Requires RDM-capable splitters (non-RDM splitters block it). Eos and
other consoles/gateways offer RDM discovery in patch.

## Dimmer and circuit loads
- Each dimmer/circuit has a rated capacity (e.g. 2.4 kW or 10 A per channel
  in UK 230 V racks; 20 A circuits in US 120 V).
- Load = sum of lamp wattages on that circuit; current I = P / V (1,000 W at
  230 V ≈ 4.3 A; at 120 V ≈ 8.3 A). Stay below rating; for LED/movers on
  "non-dim" (relay/constant) circuits, check inrush current.
- Balance phases on three-phase supplies.

## Gotchas
- Overlapping addresses (two fixtures respond together).
- Missing terminator causing flicker on long runs.
- LEDs patched on dimmed circuits — must be on non-dim/constant power.

## Verify
- [ ] Address plan with no overlaps, matching fixture modes.
- [ ] Splitters and terminators in place.
- [ ] Circuit loads within ratings; phases balanced.
