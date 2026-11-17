---
id: architecture-construction.electrical-installation.residential-wiring.domestic-circuit-rough-in-and-termination
name: domestic-circuit-rough-in-and-termination
category: architecture-construction
field: electrical-installation
product: residential-wiring
tags: [electrical-installation, residential-wiring, domestic-wiring, rough-in, first-fix, final-circuit, branch-circuit, ring-final, socket-outlet, receptacle, gpo, safe-zones, nm-cable, romex, twin-and-earth, rcd, gfci, afci, rcbo, safe-isolation, lockout-tagout, prove-dead, nec, bs-7671, as-nzs-3000]
level: practitioner
status: draft
description: "Run, rough-in and terminate a domestic socket or lighting circuit: isolate and prove dead, route cable in safe zones, protect with RCD/GFCI, terminate and label."
sources: ["NFPA 70 National Electrical Code (NEC)", "BS 7671 Requirements for Electrical Installations (IET Wiring Regulations)", "AS/NZS 3000 Wiring Rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domestic circuit rough-in and termination

**Goal:** add or extend one domestic final circuit (sockets/receptacles/GPOs or lighting)
so it is correctly sized, mechanically protected, RCD/GFCI-protected where required,
neatly terminated and ready to pass testing first time.

> **Licensed, jurisdiction-specific work.** In most places fixed wiring must be done or
> certified by a licensed/registered electrician and may need a permit or notification
> (e.g. US permit + inspection, UK Part P notification, AU certificate of compliance).
> Figures below are typical and labelled by jurisdiction; always confirm against the
> edition of the wiring rules and local amendments that apply to you.

## 1. Plan the circuit before touching a cable
- **Load and protective device.** Typical pairings — US: 15 A on 14 AWG Cu, 20 A on
  12 AWG Cu. UK: 2.5 mm² ring final on 32 A, 2.5 mm² radial on 20 A, lighting 1.0/1.5 mm²
  on 6 A. AU: 2.5 mm² power on 20 A, 1.5 mm² lighting on 10–16 A. Long runs, insulation,
  grouping or high ambient change this — size properly per
  engineering-technology.electrical-engineering.electrical-installation-design.cable-sizing.
- **Protection type.** Current rules commonly require 30 mA RCD/GFCI (or RCBO) protection
  for domestic socket circuits and, increasingly, all final circuits; US also requires AFCI
  on most dwelling branch circuits. Check which apply (wet areas, outdoors, kitchens, garages).
- **Mark out** every box, switch and outlet height on the studs/walls and walk the route.

## 2. Safe isolation before any work near existing circuits
1. Identify the supply and the circuit at the panel/consumer unit/switchboard.
2. Switch off, **lock off** with a personal padlock and tag (lockout-tagout); keep the key.
3. **Prove the tester** on a known live source or proving unit.
4. **Test dead** at the point of work: every conductor pair (L–N, L–E, N–E; on US
   120/240 V split-phase also L1–L2).
5. **Re-prove the tester.** Only now touch conductors. See
   repair-maintenance.facilities-maintenance.minor-electrical-repair.safe-isolation-and-socket-switch-and-plug-replacement.

A non-contact voltage "pen" is a hint, not proof of dead.

## 3. Rough-in / first fix
- **Fix boxes** plumb, set to finished-wall depth (allow for plasterboard/drywall thickness).
- **Route cables** where a later fixer expects them. UK: prescribed "safe zones" run
  vertically/horizontally from accessories and within 150 mm of wall/ceiling junctions;
  cables concealed in walls at under 50 mm depth without mechanical protection need
  30 mA RCD protection. US (NEC): keep cable 1-1/4 in (32 mm) from the stud face or fit
  a steel nail plate. AU: similar zone/depth rules (unverified — confirm against your
  edition of the wiring rules).
- **Support:** US NM cable is typically stapled within 12 in (300 mm) of a box and at
  ≤4.5 ft (1.4 m) intervals; don't crush the sheath with staples.
- **Keep away from** hot pipes, flues and thermal insulation (or derate), and don't share
  holes with gas or water lines.
- **Leave slack:** US minimum 6 in (150 mm) of free conductor, reaching 3 in (75 mm)
  outside the box; elsewhere leave enough to re-terminate at least once.
- **Label both ends** of each cable (circuit number, "feed"/"switch-loop").

## 4. Termination / second fix
1. Strip the sheath only inside the box; don't nick conductor insulation.
2. Strip conductor ends to the terminal's strip gauge; no bare copper visible beyond it.
3. Sleeve bare earths green/yellow (UK/AU) or follow local practice for bare/green grounds.
4. Tighten terminals to the manufacturer's torque; use push-in connectors only within
   their rated conductor size and count.
5. **Polarity:** line to the brass/L terminal, neutral to silver/N; switches break line,
   never neutral. Re-identify a cable used as a switch loop with brown/black tape.
6. Earth/ground every metal box and accessory; respect box-fill limits (US NEC 314.16).
7. Fold conductors neatly so nothing is stressed when the accessory is screwed home.

## 5. Connect at the board
Terminate in the panel only with the board's incoming supply isolated and proved dead
(live-adjacent work is discouraged or restricted in most jurisdictions). Update the
circuit schedule/directory immediately.

## Gotchas
- **Borrowed neutrals** (neutral from a different circuit) cause RCD trips and are a
  shock hazard — keep each circuit's L and N together.
- **Mixed-circuit neutrals in 2-way/3-way lighting** trip RCDs on one side only.
- **Over-stripped or loose terminals** are the commonest cause of hot accessories.
- **Plasterers bury boxes** — photograph box and cable positions before boarding.

## Verify
- [ ] Circuit isolated, locked off and proved dead with a proven tester.
- [ ] Cable size suits device rating, length and installation method.
- [ ] Every cable in a safe zone or mechanically protected; nail plates where needed.
- [ ] RCD/GFCI (and AFCI where required) protection fitted.
- [ ] Polarity correct; switches in line; all earths connected and sleeved.
- [ ] Circuit labelled at the board and ready for continuity, insulation-resistance and
  RCD tests (architecture-construction.electrical-installation.electrical-testing-commissioning.initial-verification-test-sequence).
