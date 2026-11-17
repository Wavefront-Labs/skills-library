---
id: repair-maintenance.automotive-repair.engine-repair.compression-leakdown-and-timing-belt-replacement
name: compression-leakdown-and-timing-belt-replacement
category: repair-maintenance
field: automotive-repair
product: engine-repair
tags: [automotive-repair, engine-repair, compression-test, cranking-compression, leak-down-test, cylinder-leakage, head-gasket, block-test, combustion-leak-tester, timing-belt, cambelt, timing-chain, interference-engine, locking-tools, water-pump, tensioner, torque-to-yield, misfire, valve-timing, diesel, petrol]
level: practitioner
status: draft
description: "Mechanical engine diagnosis (cranking compression, leak-down, combustion-gas block test) and a correct timing belt replacement with locking tools, tensioner setup and hand-rotation check."
sources: ["Manufacturer workshop manuals (timing procedures; structure only)", "Gates/ContiTech timing belt installation guidance (general practice)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compression, leak-down and timing belt replacement

**Goal:** prove the engine's mechanical health before throwing parts at a misfire or
rough running, and replace a timing belt so the valve timing is exact. On an
**interference engine** a timing mistake bends valves. Specs (compression values,
tensioner settings, torque/angle) come from the workshop manual for the exact engine code.

## 1. Cranking compression test (petrol)
1. Engine warm. Disable fuel (pull the fuel pump fuse/relay or injector fuse) and
   ignition (unplug coil packs) — prevents fuel washing the bores and coil damage.
2. Remove **all** spark plugs (so the engine cranks evenly), throttle held fully open
   (or pedal floored on drive-by-wire if the manual says it opens the throttle while cranking).
3. Screw in the gauge adapter; crank 4–6 compression strokes until the needle stops rising.
   Record each cylinder.
4. Judge: **evenness matters more than absolute value** — cylinders within ~10–15 % of
   each other is normal (typical healthy petrol ~ 150–200 psi / 10–14 bar; check spec).
5. **Wet test** on any low cylinder: squirt ~ 1 teaspoon (5 ml) of engine oil into it and
   retest. Rises substantially → rings/bores. No change → valves or head gasket.
   Two adjacent low cylinders → head gasket between them.
Diesel compression is much higher (~ 300–500 psi) and needs a diesel gauge via the glow
plug or injector holes — not a petrol gauge.

## 2. Leak-down test (more precise)
1. Bring the cylinder to TDC compression (both valves closed). On manual cars put in
   top gear and apply the handbrake, or hold the crank bolt with a breaker bar — air
   pressure will spin the engine if not exactly at TDC.
2. Calibrate the tester per its instructions (zero), regulator at e.g. 100 psi.
3. Read percentage leakage: ~ < 10 % good, 10–20 % worn but serviceable, > 20–30 %
   investigate (thresholds vary — compare cylinders).
4. Listen: intake/throttle body → intake valve; exhaust pipe → exhaust valve; oil filler /
   dipstick → rings; bubbles in the coolant expansion tank or adjacent plug hole → head gasket
   or cracked head.

## 3. Combustion gas in coolant (head gasket confirm)
Block tester (chemical, blue → yellow/green with CO2) over the coolant tank neck, engine
running warm; or an exhaust gas analyser sniffing the tank for HC. Also: white sweet-smelling
exhaust, coolant loss with no external leak, pressurised hoses right after start.

## 4. Timing belt replacement (typical overhead-cam engine)
1. Disconnect battery; remove accessory belts, engine mount (support engine with a jack
   and wood block), covers. Note all cover bolt lengths.
2. Rotate the engine **clockwise** (normal direction) to TDC No. 1 by the crank mark;
   confirm cam marks align. Fit the **engine-specific locking tools** (crank pin/lock, cam
   locking plate or pins). Marks alone are not enough on many engines.
3. Release the tensioner, remove the belt. Replace as a kit: **belt, tensioner, idlers,
   and usually the water pump** if belt-driven (a leaking pump destroys the new belt).
   Inspect cam/crank seals for leaks; replace if weeping.
4. Fit the new belt observing direction arrows, starting at the crank and working in the
   order the manual gives, keeping the tight side tight (no slack between crank and cam on
   the non-tensioner side).
5. Set the **automatic tensioner** to its pointer/window per the manual (often with the
   engine cold), or set a manual tensioner by deflection/sonic tension meter frequency.
6. Torque bolts to spec; many crank pulley bolts are **torque-to-yield** (torque + angle)
   and must be replaced.
7. Remove locking tools and **rotate the crank by hand two full turns** clockwise; re-check
   all marks line up and the tool pins fit freely. Any resistance → stop: valve contact.
8. Reassemble, refill/bleed coolant if the pump was changed, start and check for noise.
   Record the mileage/date on a sticker in the engine bay.

## Gotchas
- Never rotate the engine backwards with the new belt (can jump teeth with some tensioners).
- Camshaft pulleys on keyless/taper fits lose timing if the bolt is loosened without lock tools.
- Uncertain: pressures and percentages are typical rules of thumb; manufacturer data governs.

## Verify
- [ ] Compression recorded per cylinder, low cylinders wet-tested and leak-down located.
- [ ] Head gasket suspicion confirmed with a block test, not guessed.
- [ ] Engine locked at TDC with correct tools; belt kit and water pump replaced.
- [ ] Tensioner set to spec; TTY bolts replaced and torqued + angled.
- [ ] Two hand-rotations show marks aligned with no resistance; engine runs quietly.
