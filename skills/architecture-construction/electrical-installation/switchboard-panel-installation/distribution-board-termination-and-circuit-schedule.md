---
id: architecture-construction.electrical-installation.switchboard-panel-installation.distribution-board-termination-and-circuit-schedule
name: distribution-board-termination-and-circuit-schedule
category: architecture-construction
field: electrical-installation
product: switchboard-panel-installation
tags: [electrical-installation, switchboard-panel-installation, distribution-board, db, consumer-unit, panelboard, load-center, switchboard, subpanel, mcb, mccb, circuit-breaker, rcd, rcbo, gfci, breaking-capacity, kaic, neutral-bar, earth-bar, men-link, main-bonding-jumper, circuit-schedule, panel-directory, torque, lockout-tagout]
level: practitioner
status: draft
description: "Fit out a distribution board/panelboard/consumer unit: isolate the incomer, select breakers and RCDs, terminate and torque, separate N and E, label circuits."
sources: ["NFPA 70 National Electrical Code (NEC)", "BS 7671 Requirements for Electrical Installations", "AS/NZS 3000 Wiring Rules", "IEC 61439 Low-voltage switchgear and controlgear assemblies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distribution board termination and circuit schedule

**Goal:** mount and dress a distribution board (UK "consumer unit"/"DB", US
"panelboard"/"load center", AU "switchboard"/"distribution board") so every circuit
lands on the right device, the right neutral and the right earth, every terminal is at
torque, and the next person can identify every circuit from the label alone.

> **Licensed, jurisdiction-specific work.** Board changes usually need a licensed
> electrician and often a permit, notification or network-operator involvement for the
> incomer. Figures below are typical; confirm against your edition of the wiring rules
> and the board manufacturer's instructions.

## 1. Plan the board
- **Count ways** for all circuits plus ~20% spare.
- **Device selection:** rating to protect the cable; curve to suit the load (IEC: B for
  general, C for motors/lighting with inrush, D for high-inrush); **breaking capacity**
  at least the prospective fault current at the board (common: UK domestic MCB 6 kA
  within a board conditionally rated 16 kA; US residential breakers 10 kAIC). Measure or
  obtain the prospective fault current from the supplier.
- **RCD arrangement:** RCBO per circuit (best discrimination) vs split-load banks behind
  shared RCDs (one fault trips several circuits). Keep critical loads (fridge/freezer,
  alarms) off shared RCDs where rules allow.
- **Board type rules:** UK domestic consumer units must have a non-combustible enclosure
  (ferrous metal). US: listed panel and breakers of the matching type only.

## 2. Safe isolation — the incomer stays live
1. Isolate at the point of supply: the supplier's cut-out/service fuse, upstream breaker,
   or meter pull, as your jurisdiction allows. Turning off the board's main switch leaves
   its **line-side terminals live**.
2. Lock off and tag (lockout-tagout); for supplier fuses use the network's procedure.
3. Prove the tester, test dead at the main switch line and load terminals (L–N, L–E,
   N–E, phase–phase on three-phase), re-prove the tester.
4. Treat the meter tails/service conductors as live unless proved otherwise.

## 3. Mount and enter
- Mount level, at the height rules require (accessibility and working clearance: US NEC
  110.26 working space is typically 30 in (762 mm) wide and 3 ft (914 mm) deep for
  ≤150 V to ground).
- Enter cables through the knockouts/glands nearest their device; fit grommets; keep the
  enclosure IP/fire rating — no open holes. Seal unused knockouts.

## 4. Terminate in a fixed order
1. **Earth/ground conductors first**, to the earth bar.
2. **Neutrals** to the neutral bar **in the same order as their breakers** (UK/AU split
   boards: to the neutral bar of the RCD that protects that circuit).
3. **Lines** to their breakers.
4. Strip to the terminal depth; no insulation under the clamp, no bare copper showing;
   ferrules on fine-stranded conductors where the maker requires.
5. **Torque** every terminal with a calibrated driver to the printed value and mark it.

**Neutral–earth bonding:** only at the origin/service (US main bonding jumper; AU MEN
link; UK TN-C-S at the cut-out). In any **sub-board/subpanel**, neutrals and earths are
kept on separate, isolated bars — a bond there puts neutral current on the earthing system.

## 5. Dress and label
- Route conductors along the gutters with a service loop; nothing across busbars.
- Fit blanks in every unused way.
- **Circuit schedule / panel directory:** number, description specific enough to find it
  ("Kitchen sockets, island and east wall", not "Sockets"), device rating/type, cable size,
  RCD that covers it.
- Warning labels as required: RCD test notice, dual-supply (solar/battery/generator)
  warnings, non-standard colours notice. UK RCD notice now says six-monthly testing
  (unverified — confirm against your edition of the wiring rules).

## 6. Metering (where fitted)
Install CTs with the P1 face toward the source; never open-circuit a CT secondary under
load — short it first.

## Gotchas
- **Neutral on the wrong RCD bank** trips that RCD whenever the load runs.
- **Breakers of the wrong brand/type** in a listed panel void listing and can arc at the bus.
- **Loose neutral** on three-phase boards causes over-voltage on lightly loaded phases.
- Alloy conductors need rated terminals and anti-oxidant.

## Verify
- [ ] Supply isolated upstream of the board, locked off and proved dead.
- [ ] Device ratings protect the cables; breaking capacity ≥ prospective fault current.
- [ ] Each neutral on the bar of its own RCD/circuit; no N–E bond in a sub-board.
- [ ] All terminals torqued and marked; blanks fitted; no open knockouts.
- [ ] Circuit schedule complete and specific; warning labels fitted.
- [ ] Board ready for testing per architecture-construction.electrical-installation.electrical-testing-commissioning.initial-verification-test-sequence.
