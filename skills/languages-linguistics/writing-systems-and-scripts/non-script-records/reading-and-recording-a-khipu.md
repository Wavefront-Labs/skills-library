---
id: languages-linguistics.writing-systems-and-scripts.non-script-records.reading-and-recording-a-khipu
name: reading-and-recording-a-khipu
category: languages-linguistics
field: writing-systems-and-scripts
product: non-script-records
tags: [non-script-records, khipu, quipu, inca, andean, knot-records, decimal-positional, single-knot, long-knot, figure-eight-knot, pendant-cords, top-cords, subsidiary-cords, primary-cord, cord-colour, ply-direction, s-ply, z-ply, khipu-database, ascher, tally-sticks, split-tally, tally-marks, record-keeping]
level: advanced
status: draft
description: "Reading khipu (quipu) knot records: cord structure, the decimal knot system, recording attachment, ply, colour and knots in a standard form, plus how tally systems compare."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading and recording a khipu (quipu)

**Goal:** document an Andean knotted-cord record accurately and decode its numerical
content; know where interpretation is solid (numbers) and where it is still open
(possible narrative or non-numerical content).

> Draft. The numerical system described here is well established (from the work of
> Leland Locke and Marcia and Robert Ascher, among others); claims about non-numerical
> or phonetic content remain debated. Handle real specimens only under conservator
> supervision.

## 1. Anatomy
- **Primary cord:** the main horizontal cord everything hangs from.
- **Pendant cords:** hang down from the primary cord; most data lives here.
- **Top cords:** attached so they rise above the primary cord; in some khipus they appear
  to hold sums of a group of pendants.
- **Subsidiary cords:** attached to pendants (and to other subsidiaries) — a tree.
- **Groups:** pendants are often clustered with gaps between clusters; spacing is data.

## 2. The numerical knot code
Values are **base-10 positional**, read from the **bottom (units) up** a cord, with
**clusters** of knots at distinct levels:
- **Long knots** (a single knot with 2–9 turns) represent 2–9 in the **units** position.
- **Figure-eight knot** represents **1** in the units position (a long knot can't have
  one turn).
- **Single (overhand) knots** clustered at higher positions represent tens, hundreds,
  thousands: three single knots at the tens level = 30.
- An **empty position** (no knots where a cluster would be, judged by alignment with
  neighbouring cords) = **zero**.
Example, reading upward: long knot of 4 turns (4), then 2 single knots (20), then a gap
at the hundreds level (0), then 1 single knot (1000) → 1,024.

## 3. Recording protocol (one row per cord)
For every cord, record:
1. **ID** in a hierarchical scheme (pendant 12, subsidiary 12s1, …) and position on the
   primary cord (distance from one end, in cm).
2. **Attachment:** recto/verso (which way the loop faces) — may encode a binary.
3. **Ply / spin direction:** S or Z — also potentially meaningful.
4. **Colour(s):** use a consistent reference set; note mixed or barber-pole colours.
5. **Knots:** type (single, long with turn count, figure-eight), **direction** (S/Z)
   and **distance from the primary cord** for each, so positional levels can be aligned
   across cords.
6. **Length**, termination (knotted end, broken), condition.
Photograph each cord against a scale. Several khipu databases (e.g. projects building on
the Aschers' records) use comparable fields — matching an existing schema lets you
compare across collections.

## 4. Analysis moves
- **Align knot levels** across cords in a group to resolve ambiguous positions.
- **Test sums:** do top cords or particular pendants equal the sum of a group? Sum
  relationships are the strongest evidence of an accounting khipu.
- **Colour and position patterns:** recurring colours across groups may mark categories.
- **Compare to colonial documents** that transcribe khipu readings (rare but key).
- **Non-numerical cords** (knots that don't fit the decimal rules) are where open
  research questions lie; record them faithfully instead of "correcting".

## 5. Related systems
- **Tally sticks:** notches for counts; English **split tallies** divided a notched
  stick between two parties so either could prove the debt by matching halves.
- **Tally marks and knotted cords** elsewhere (e.g. Ryukyuan and other knot records)
  share the counting principle but not the khipu code.
- Pictographic records (e.g. winter counts) record events by images, not language.

## Gotchas
- Reading top-down: units are at the **bottom** of the cord.
- Mistaking a damaged long knot for single knots.
- Dropping zeros by not aligning with neighbouring cords.
- Recording colour under uncontrolled lighting.

## Verify
- [ ] Every cord has an ID, attachment, ply, colour, knot list with positions.
- [ ] Decoded values follow the rules (1 = figure-eight, 2–9 = long knot in units).
- [ ] At least one sum test was run per cord group.
- [ ] Non-conforming cords are recorded as-is, not normalised.
