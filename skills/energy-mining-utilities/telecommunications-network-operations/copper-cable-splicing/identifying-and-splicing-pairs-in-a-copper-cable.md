---
id: energy-mining-utilities.telecommunications-network-operations.copper-cable-splicing.identifying-and-splicing-pairs-in-a-copper-cable
name: identifying-and-splicing-pairs-in-a-copper-cable
category: energy-mining-utilities
field: telecommunications-network-operations
product: copper-cable-splicing
tags: [copper-cable-splicing, telecommunications-network-operations, cable-splicer, twisted-pair, 25-pair-colour-code, binder-group, tip-and-ring, pair-identification, tone-and-probe, talk-battery, modular-connector, 3m-ms2, 710-connector, picabond, ud-connector, bonding, shield-bond, bond-clamp, grounding, splice-case, pressurised-cable, air-pressure, encapsulant, split-pair, crossed-pair, reversed-pair, pic-cable, pulp-cable]
level: practitioner
status: draft
description: "Splice a multipair telephone cable: read the 25-pair colour code and binder groups, identify pairs live, use modular connectors, bond the shield across, and avoid split pairs."
sources: ["Telcordia/Bellcore splicing practice concepts (paraphrased)", "3M MS2 and 710 connector instructions (general)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identifying and splicing pairs in a copper cable

**Goal:** join or rearrange pairs in a multipair telephone cable (PIC, filled or
air-core, sometimes old pulp-insulated) so that every pair goes where the records say,
tip stays with tip, nothing is split, the shield is continuous and grounded, and the
splice keeps water out — without dropping customers who are live on the cable.

## 1. The colour code
North American (and widely used) 25-pair code — each pair is a **primary** (tip)
colour with a **secondary** (ring) colour:
- Primaries in order: **white, red, black, yellow, violet**.
- Secondaries in order: **blue, orange, green, brown, slate**.
- Pair 1 = white-blue, 2 = white-orange … 5 = white-slate, 6 = red-blue … 25 =
  violet-slate.
Larger cables bundle 25-pair **binder groups** wrapped with binders in the same
colour combinations (binder 1 = white-blue, etc.); 100-pair super-units may be wrapped
again. Pair number = (binder − 1) × 25 + pair within binder.
Other countries (e.g. UK, Germany) use different codes — confirm from the cable spec.

## 2. Before opening
- Get the **work order and cable records**: count (pair ranges), which pairs are
  working, which are spare, where they go.
- Check for **pressurisation** if it's an air-core cable: note pressure, bypass with a
  temporary air supply if required so you don't let water in or alarm the monitor.
- Gas-test manholes before entry and set up guarding, as for any confined space.

## 3. Open and bond
- Remove sheath per the splice case dimensions.
- **Shield bond first:** install bond clamps on the shields of each cable and connect
  them with a bond strap across the opening, and to ground where the design says. A
  broken shield causes noise, induced voltage hazards and lightning damage.
- Keep binders identified as you fan out; tie them loosely so groups don't mix.

## 4. Identify pairs
- On spare or dead pairs, use **tone and probe** from the far end (or a cable pair
  identifier).
- On working pairs, check before you move anything: listen with a test set in monitor
  (high impedance) mode, or check for battery/talk voltage — about 48 V DC on an idle
  POTS line, ringing voltage much higher (around 90 V AC) — and DSL signal. Never
  cut a pair you haven't identified.
- Watch for **split pairs**: tip of one pair with ring of another. They test fine for
  continuity but cause crosstalk and hum on DSL/voice. Always keep a pair's two
  conductors together.

## 5. Splice with modular connectors
- For bulk straight-through work, **modular connectors** (3M MS2, 710 type) splice
  25 pairs at a time: load the index strip in colour order, lay the pairs in, seat
  the body, trim and crimp with the press. Keep tip/ring order consistent.
- Single pairs: UR/UY-type filled connectors (small "beans") — no stripping, crimp
  with the right tool.
- **Bridge-then-cut** for live pairs being rearranged: bridge the new path with a
  half-tap connector first, confirm service on it, then cut the old path.

## 6. Close
- Dress connectors in banks, wrap, install splice case with encapsulant (filled
  cable) or seal for pressurisation. Restore air pressure and confirm it holds.
- Update records with the pairs moved.

## Gotchas
- Reversed (tip-ring swapped) pairs work for most voice but can upset some
  equipment; crossed pairs connect the wrong customer.
- Moisture in old air-core cable: wet pairs show low insulation resistance; a megger
  or insulation test identifies them.
- Uncertain: connector part numbers, bond specs and voltages differ by operator
  and country; follow local practice.

## Verify
- [ ] Records and work order checked; pressurisation bypassed if needed.
- [ ] Shields bonded across the splice and grounded per design.
- [ ] Every working pair identified before moving; bridge-then-cut used.
- [ ] No split pairs: each pair's tip and ring stay together.
- [ ] Splice sealed, pressure restored and holding; records updated.
