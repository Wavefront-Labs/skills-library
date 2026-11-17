---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.hydraulic-systems-repair.hydraulic-pressure-flow-testing-and-cylinder-resealing
name: hydraulic-pressure-flow-testing-and-cylinder-resealing
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: hydraulic-systems-repair
tags: [hydraulic-systems-repair, hydraulics, stored-energy, accumulator, injection-injury, pressure-test, flow-meter, flow-test, relief-valve, main-relief, port-relief, pump-efficiency, case-drain, load-sense, margin-pressure, cylinder-drift, cylinder-reseal, piston-seal, rod-seal, wiper-seal, hose-fabrication, iso-4406, contamination-control, kidney-loop, test-points, minimess]
level: practitioner
status: draft
description: "Safely relieve stored hydraulic energy, pressure- and flow-test pumps, reliefs and cylinders, reseal a cylinder, and keep contamination out with ISO 4406 cleanliness targets."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hydraulic pressure and flow testing, cylinder resealing

**Goal:** prove whether the pump, a valve or a cylinder is at fault with gauges and a
flow meter instead of swapping parts, then repair it without bringing dirt in.

## 1. Make it safe first — hydraulics stores energy
- Lower every implement to the ground or onto rated blocking/cribbing. A raised boom
  is held only by oil and seals; never work under it on hydraulics alone.
- Shut down, apply lockout, then **relieve pressure**: cycle the controls several times
  with the key on/engine off (pilot accumulator), bleed the tank cap slowly if
  pressurised, and discharge accumulators per the OEM procedure.
- Accumulators stay charged with nitrogen after the oil is relieved; treat them as live.
- Oil at 200–350 bar from a pinhole can inject through skin and gloves. Search for
  leaks with cardboard, never a hand. Any injection injury goes straight to hospital,
  even if it looks like a small puncture.
- Hot oil (60–80 °C running temperature) burns; let it cool before opening.

## 2. Pressure testing
1. Bring oil to operating temperature (typically ~50 °C; OEMs specify a test range).
   Cold oil gives misleading numbers.
2. Fit calibrated gauges or transducers on the test points (Minimess-type quick
   couplers) with a gauge rated above the expected maximum — a 0–400 bar gauge for a
   350 bar system.
3. **Main relief**: stall a function against its end stop at rated engine speed and read
   pressure. Low = relief set low or leaking, or pump unable to make pressure.
4. **Port reliefs**: test each work port separately.
5. **Load-sense systems**: read pump pressure minus LS pressure with a function
   lightly loaded — this margin (often 20–30 bar) tells you if the pump compensator is
   right. Standby pressure with nothing moving is the other check.
6. **Pilot pressure**: typically 30–40 bar; low pilot gives slow everything.

## 3. Flow testing
- Put an in-line **flow meter with load valve** between the pump outlet and the system
  (or on a function). Record flow at no load, then at increasing pressure up to just
  below relief.
- A healthy pump loses little flow as pressure rises. A drop of more than about 10–15%
  of no-load flow at working pressure means internal wear.
  (Draft note: acceptance limits are OEM-specific — compare to the pump curve.)
- Measure **case drain flow** on piston pumps and motors into a graduated container
  over a timed period; high case drain points to internal wear before output drops.

## 4. Cylinder drift and resealing
- Drift test: load the cylinder, mark the rod, time the movement. Then isolate: with
  the rod fully extended and a hose disconnected and capped at the valve on the rod side
  (pressure safely relieved), oil leaking past the piston shows on the open side. If the
  cylinder holds, the leak is in the valve spool or a port relief.
- Resealing: clean outside first. Mount in a bench vise or cylinder bench, remove gland
  (spanner wrench), pull rod, then remove the piston nut (often torqued very high and
  locked — use the OEM procedure and heat only if specified).
- Inspect the rod for chrome pits and straightness, the barrel for scoring. A scored
  barrel or pitted rod will chew new seals in hours.
- Fit seals with plastic picks and installation cones; never use a screwdriver.
  Size and soak/heat PTFE piston seals per the kit instructions. Lightly oil with the
  system fluid on assembly.

## 5. Contamination control and hoses
- Target cleanliness is around ISO 4406 18/16/13 for mobile gear and tighter
  (16/14/11) for servo/proportional valves. Take an oil sample after major work.
- Cap every open port and hose end immediately. Flush new hoses with a projectile
  cleaner and cap both ends.
- Hoses: match SAE/ISO pressure rating, crimp with the manufacturer's die set and
  measured crimp diameter; do not mix fitting and hose brands.
- After a pump failure, flush and change filters, or debris kills the new pump.

## Gotchas
- A slow machine with correct pressures can be a low engine speed or pilot problem.
- Raising relief setting to "fix" weakness overloads the pump and hoses.
- (Draft note: all pressures here are typical ranges; set and test to the OEM manual.)

## Verify
- [ ] Implements grounded or blocked, pressure and accumulators relieved before opening.
- [ ] Relief, margin and pilot pressures recorded and within OEM spec.
- [ ] Flow at working pressure within pump curve limits.
- [ ] Cylinder drift test passes after reseal; no external leaks.
- [ ] Oil sample after the job meets the cleanliness target.
