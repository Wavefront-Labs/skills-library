---
id: architecture-construction.electrical-installation.commercial-industrial-wiring.three-phase-motor-circuit-installation
name: three-phase-motor-circuit-installation
category: architecture-construction
field: electrical-installation
product: commercial-industrial-wiring
tags: [electrical-installation, commercial-industrial-wiring, three-phase, 3-phase, motor-circuit, motor-wiring, dol-starter, direct-on-line, star-delta, wye-delta, overload-relay, motor-starter, local-isolator, disconnect-within-sight, cable-gland, swa, mc-cable, phase-rotation, insulation-resistance, megger, vfd, lockout-tagout, nec-430, bs-7671, as-nzs-3000]
level: practitioner
status: draft
description: "Install and connect a three-phase motor circuit: isolator, starter/overload, cable and glanding, star/delta terminal links, IR test, rotation check and lock-off."
sources: ["NFPA 70 National Electrical Code (NEC) Article 430", "BS 7671 Requirements for Electrical Installations", "AS/NZS 3000 Wiring Rules", "NFPA 70E Standard for Electrical Safety in the Workplace"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-phase motor circuit installation

**Goal:** take a fixed three-phase motor (pump, fan, conveyor) from a distribution board
to a running, correctly rotating, correctly protected machine with a lockable local
isolator — without damaging the windings or a drive on the way.

> **Licensed, jurisdiction-specific work.** Industrial motor circuits must be installed by
> a licensed electrician under site permit-to-work rules. The figures below are typical
> and labelled by jurisdiction; confirm against your edition of the wiring rules, the motor
> nameplate and the starter/drive manufacturer's data.

## 1. Read the nameplate and pick the scheme
Record: kW/hp, voltage(s) and connection (e.g. `230Δ/400Y` or `400Δ/690Y`), full-load
current (FLA/FLC), service factor, IP rating, frame and duty. Then decide the starter:
- **DOL (direct-on-line):** simplest; inrush typically 6–8× FLC.
- **Star-delta (wye-delta):** six leads to the starter; motor must be rated delta at supply voltage.
- **Soft starter or VFD:** see engineering-technology.electrical-engineering.motor-drive-design.vfd-application.

## 2. Size conductors and protection
- **US (NEC Art. 430):** size branch conductors at 125% of the *table* FLC (Table
  430.250), not the nameplate; overload set from the *nameplate* FLA at 125% (service
  factor ≥1.15 or temp rise ≤40 °C) or 115% otherwise; short-circuit/ground-fault device
  per Table 430.52 (e.g. inverse-time breaker up to 250% of FLC).
- **UK/AU (IEC practice):** thermal overload set at motor FLC; upstream MCB/MCCB of a
  curve that rides through starting (often type D or a motor-protection breaker);
  coordination type 1/2 per the starter maker's tables.
- Check voltage drop on start for long runs; full method in
  engineering-technology.electrical-engineering.electrical-installation-design.cable-sizing.

## 3. Isolate, lock off, prove dead
1. Get the permit; identify the supply way at the board.
2. Open the breaker, apply a personal lock and tag (lockout-tagout); try-start to confirm.
3. Prove the tester, **test dead** across all phase pairs (L1–L2, L2–L3, L1–L3) and each
   phase to earth and neutral, re-prove the tester.
4. Note stored energy: VFD DC-bus capacitors need several minutes to discharge
   (drive label states the time) — measure the bus before touching.

## 4. Install the cable and isolator
- Run cable on tray/ladder or in conduit with fixings at the manufacturer's spacing;
  keep power and control/instrument cables segregated.
- **Local isolator / disconnect:** lockable in the off position and within sight of the
  motor — US "within sight" means visible and not more than 50 ft (15 m). Use an
  AC-23 rated switch for motor duty (IEC).
- **Glanding:** SWA via a correctly sized gland with the armour clamped as the earth
  path (plus a separate CPC if the design calls for it); MC/Teck with listed fittings;
  VFD output cable shielded with a 360° EMC gland at both ends.
- Fit drip loops or flexible conduit for vibration at the motor.

## 5. Terminate at the motor
- Set the terminal-box links for the supply: **star (Y)** links join U2-V2-W2;
  **delta (Δ)** links are U1-W2, V1-U2, W1-V2. Wrong link = burnt motor or no torque.
- Torque terminals to the motor maker's values; earth to the box earth stud.
- Re-fit the terminal-box gasket — this is how IP55 motors take water.

## 6. Test before energising
- **Continuity** of the protective conductor to the motor frame.
- **Insulation resistance** at 500 V DC (for ≤500 V motors) phase-to-phase and
  phase-to-earth; ≥1 MΩ is a common minimum for a motor, new ones read far higher
  (unverified — confirm against your edition of the wiring rules and the motor maker).
  **Disconnect any VFD or soft starter first** — IR testing through a drive destroys it.
- Prove overload setting and starter wiring with the motor disconnected.

## 7. Energise and check rotation
1. Remove locks under the permit procedure; tell everyone at the machine.
2. Check phase sequence at the isolator with a rotation meter, or **bump** the motor
   (start and stop at once), ideally uncoupled from the load.
3. Wrong direction: isolate, prove dead, swap **any two** phases at the motor or isolator.
4. Run, then measure current on each phase under load: compare with FLC and check
   balance.

## Gotchas
- Setting overloads from the table FLC instead of the nameplate (US) — trips or no protection.
- Single-phasing on a lost fuse burns windings unless the overload has phase-loss sensing.
- Some pumps and compressors are damaged quickly if run backwards — bump, do not run.
- Fans in a draught can windmill and back-feed voltage into "dead" terminals.

## Verify
- [ ] Locked off and proved dead (all phase pairs + earth) before termination.
- [ ] Conductors, short-circuit device and overload sized per the applicable rules.
- [ ] Lockable isolator within sight of the motor.
- [ ] Star/delta links match the nameplate and supply voltage.
- [ ] IR and earth continuity recorded with drives disconnected.
- [ ] Rotation correct, phase currents balanced and within FLC.
