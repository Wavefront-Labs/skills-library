---
id: energy-mining-utilities.telecommunications-network-operations.network-test-instruments.otdr-setup-and-trace-reading-for-fault-location
name: otdr-setup-and-trace-reading-for-fault-location
category: energy-mining-utilities
field: telecommunications-network-operations
product: network-test-instruments
tags: [network-test-instruments, telecommunications-network-operations, otdr, optical-time-domain-reflectometer, exfo, viavi, anritsu, yokogawa-aq, launch-cable, receive-cable, pulse-width, dead-zone, event-dead-zone, attenuation-dead-zone, refractive-index, ior, group-index, backscatter, reflective-event, non-reflective-event, ghost, gainer, splice-loss, connector-reflectance, fibre-break, macrobend, 1310nm, 1550nm, 1625nm, light-source-power-meter, olts, fault-location]
level: practitioner
status: draft
description: "Set up an OTDR (launch cable, pulse width, range, IOR) and read the trace: splices, connectors, bends, breaks and ghosts, then turn trace distance into a dig or splice point in the field."
sources: ["OTDR vendor application notes (EXFO, VIAVI — general principles, paraphrased)", "IEC 61746 (OTDR calibration concepts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OTDR setup and trace reading for fault location

**Goal:** use an OTDR to find *where* and *what* a fibre fault is — break, bad splice,
dirty connector, tight bend — and translate the trace distance into a place on the
ground. For pass/fail end-to-end loss, use a light source and power meter (OLTS);
the OTDR is for locating and characterising events.

## 1. Clean and inspect first
Inspect every connector with a fibre microscope/probe before connecting (IEC 61300-3-35
pass/fail is built into many probes). Clean if dirty, re-inspect. A dirty connector
on the OTDR port spoils every trace you take — and can damage the port.

## 2. Use launch (and receive) cables
- A **launch cable** (commonly 150 m–1 km, depending on pulse width) lets the OTDR
  recover from its own front-connector reflection, so you can see the first connector
  of the link under test.
- A **receive cable** at the far end lets you measure the last connector.
- Tell the OTDR the launch/receive lengths so it reports link-only results.

## 3. Settings
- **Wavelength:** 1310 and 1550 nm at least; 1625 nm shows macrobends best.
  A bend shows much more loss at 1550/1625 than at 1310; a splice shows similar loss at
  all wavelengths.
- **Pulse width:** short pulses (5–30 ns) resolve closely spaced events but don't reach
  far; long pulses (1–10 µs) reach tens of km but blur events together (bigger
  **dead zone**). Start short for buildings and access networks, longer for long-haul.
- **Range:** set to about 1.5–2× the fibre length so the end is on screen and ghosts are
  identifiable.
- **Averaging time:** longer = cleaner trace. 15–60 s typical; more for long spans.
- **IOR (group index):** from the cable datasheet (single-mode typically ~1.467–1.468).
  A wrong IOR scales every distance.

## 4. Reading the trace
- Sloping straight line = fibre backscatter; slope = attenuation (dB/km, roughly
  0.33–0.35 at 1310 and ~0.19–0.22 at 1550 for standard SM fibre).
- **Non-reflective drop** = fusion splice or bend.
- **Reflective spike + drop** = connector or mechanical splice. Report reflectance.
- **Big reflective spike then noise floor** = fibre end or clean break (a crushed
  fibre may be non-reflective).
- **Gainer** (apparent gain) at a splice = mode-field mismatch; measure from both ends
  and average.
- **Ghost** = an echo spike appearing at a multiple of a strong reflection's distance,
  often beyond the real fibre end with no loss after it. Change range or pulse; a
  ghost moves or disappears, a real event stays.

## 5. Distance to the ground
Trace distance is **optical fibre length**, not route length. Fibre is longer than the
route: slack loops at closures and manholes, helix (excess fibre length) in the cable,
and the route isn't straight. To locate:
1. Find the closest known reference — a splice closure visible on the trace.
2. Measure from that event to the fault, not from the OTDR.
3. Subtract recorded slack loops along that section; apply the cable's helix factor
   (often ~1–2 %, from the datasheet).
4. Use cable sheath **metre marks** where you can read them.
Expect to be within tens of metres on long spans; dig or open the nearest closure,
not a point guess.

## Gotchas
- Testing from the wrong end of a long link puts the fault in the far noise; test from
  the nearer end.
- Live fibres: use an out-of-band wavelength (1625/1650 nm with filter) or confirm
  dark with a power meter first — never shoot an OTDR into a live system without checking.
- Uncertain: dead zones, IOR and slack conventions vary by instrument and operator.

## Verify
- [ ] Connectors inspected and cleaned; launch and receive cables in use.
- [ ] Wavelengths, pulse width, range and IOR set and recorded.
- [ ] Each event classified (splice, connector, bend, break, ghost).
- [ ] Fault distance measured from the nearest known event with slack/helix corrections.
- [ ] Trace files saved with fibre ID and both-direction results where needed.
