---
id: repair-maintenance.marine-vessel-repair.marine-electrical-systems.dc-fault-finding-and-battery-bank-service
name: dc-fault-finding-and-battery-bank-service
category: repair-maintenance
field: marine-vessel-repair
product: marine-electrical-systems
tags: [marine-electrical-systems, boat-electrics, 12v, dc-system, battery-bank, house-bank, start-battery, voltage-drop, multimeter, clamp-meter, tinned-wire, abyc-e-11, iso-13297, iso-10133, fuse-sizing, anl-fuse, class-t-fuse, battery-switch, vsr, dc-dc-charger, lithium-lifepo4, agm, flooded-lead-acid, shore-power, galvanic-isolator, bonding, anodes, stray-current, heat-shrink-crimp]
level: practitioner
status: draft
description: "Find 12/24 V boat electrical faults by voltage drop under load, test and maintain battery banks, size fuses and wire, make marine-grade crimps, and check bonding and anodes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DC fault finding and battery bank service on boats

**Goal:** locate the real cause of a dead or flickering circuit quickly, keep battery
banks healthy, and make repairs that survive salt, vibration and damp.

## 1. Measure, don't guess — voltage drop under load
Static voltage checks lie: a corroded connection shows 12.6 V with no load and
collapses when the pump runs.
1. Switch the load **on**.
2. Meter across the **positive path**: battery + post → load + terminal. Then the
   **negative path**: load − terminal → battery − post. Each reading is the drop.
3. Targets (ABYC E-11 guidance): **≤3%** drop for critical circuits (nav lights, bilge
   pumps, electronics), **≤10%** for others. At 12 V, 3% ≈ 0.36 V.
4. Walk the meter probe along the path (switch, fuse, terminal block, each crimp) — the
   drop jumps across the bad joint.
Also: a **clamp meter** on the battery negative shows parasitic draw with everything
off (should be milliamps; amps = something left on or a leak to ground).

## 2. Battery bank health
- **Resting voltage** (≥4 h no charge/load), flooded/AGM 12 V: ~12.7 V full, ~12.4 V
  ~75%, ~12.2 V ~50%, ≤12.0 V ~25% — recharge before going lower. Lithium (LiFePO4)
  sits flat ~13.2–13.4 V across most of its range; use the **battery monitor (shunt) SoC**,
  not voltage.
- Flooded: check electrolyte monthly, top up with distilled water over the plates, never
  overfill. Hydrometer: spread >0.05 SG between cells = bad cell.
- **Load test** or a conductance tester for start batteries; capacity test for house banks.
- Keep banks of the **same type, age and capacity**. Don't add a new battery to an old bank.
- Terminals: clean bright, tight to torque, coated with terminal protector; **max four
  lugs per stud** is a common good-practice rule.
- Charging: set the charger and alternator regulator profiles to the battery chemistry.
  Lithium banks need a BMS and usually a **DC-DC charger** or regulator limiting
  alternator current (alternators can overheat feeding lithium).

## 3. Wire, fuses and terminations
- Use **tinned, stranded marine cable** (fine-strand, e.g. Type 3 / ISO 10133 class) —
  never solid core or household wire.
- Size by **both** current (ampacity) and voltage drop over the *round-trip* length.
  Long runs (bow thruster, windlass) are usually drop-limited: use a voltage-drop table/
  calculator for 3%.
- **Fuse within ~18 cm (7 in) of the battery** on every positive conductor (ABYC; up to
  ~1.8 m if the conductor is sheathed), sized to protect the *wire*, not the load.
  High-current banks (lithium) need fuses with adequate interrupt rating (Class T).
- **Crimp** with a ratcheting crimper and tinned heat-shrink terminals; tug-test every
  crimp. Avoid solder-only joints in vibration (the wire breaks where the solder stops).
- Support wire every ~45 cm, chafe-protect through bulkheads, keep above bilge water.

## 4. Shore power, bonding and corrosion (overview)
- Fit a **galvanic isolator** (or isolation transformer) in the shore-power ground —
  otherwise your boat is in a galvanic circuit with every boat on the dock.
- Check **anodes** each haul-out; replace at ~50% wasted. Anodes that don't erode at
  all may be disconnected or painted over; ones eroding very fast suggest stray current.
- **Reference electrode** (silver/silver chloride) and a meter measure hull potential:
  aluminium boats and underwater metals have target ranges; a survey is worth it if
  corrosion is rapid.
- Leaking AC into the water is a lethal shock risk to swimmers (electric shock drowning).
  An **ELCI/RCD** on the shore-power inlet is strongly recommended.

## 5. Fault-finding sequence for a dead circuit
1. Breaker/fuse: tripped? Reset once; if it trips again, there's a short — stop and find it.
2. Voltage at the load with it switched on.
3. Voltage drop on + and − paths (section 1).
4. Inspect the worst-environment joints first: bilge, deck penetrations, mast step,
   behind the panel.
5. Repair with marine-grade terminals and seal deck plugs/connectors.

## Gotchas
- Green crusty corrosion wicks under insulation — cut back to bright copper.
- A 12.4 V reading with a charger connected means nothing; disconnect and rest first.
- Disconnect lithium and electronics before welding or jump-starting.
- AC work on board (240/120 V) is shock-hazard work: isolate shore power and inverter first.

## Verify
- [ ] Voltage drop ≤3% on critical circuits measured under load.
- [ ] Parasitic draw measured with everything off; explained or fixed.
- [ ] Every positive has a correctly sized fuse near the battery.
- [ ] Crimps tug-tested and heat-shrink sealed; wire supported and chafe-free.
- [ ] Anodes checked; galvanic isolator/RCD present on shore power.

*Draft: standards references (ABYC E-11, ISO 13297) summarised from memory — confirm current editions.*
