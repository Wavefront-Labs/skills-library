---
id: energy-mining-utilities.oil-gas-extraction.drilling-rig-systems.drawworks-top-drive-and-mud-pump-checks
name: drawworks-top-drive-and-mud-pump-checks
category: energy-mining-utilities
field: oil-gas-extraction
product: drilling-rig-systems
tags: [drilling-rig-systems, drawworks, crown-saver, floor-saver, block-position, hookload, weight-on-bit, drill-line, slip-and-cut, ton-miles, top-drive, ibop, makeup-torque, mud-pump, triplex-pump, pop-off-valve, relief-valve, liner, swab, pulsation-dampener, iron-roughneck, pipe-handler, zone-management, anti-collision, driller-cabin, cyber-chair, edr, electronic-drilling-recorder, amphion, nov]
level: practitioner
status: draft
description: "Operate and check core rig machinery: drawworks and crown/floor saver limits, top drive torque and IBOP, mud pump pop-offs and liners, pipe handler zones, and reading the driller's display."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drawworks, top drive and mud pump checks

**Goal:** run the rig's big machines inside their limits and catch wear before it becomes
a dropped block, a parted drill line or a burst pump.

> Status: draft. Written generically across rig makers (NOV, Canrig, Cameron and
> others); control screens and limits differ by rig and must come from the OEM manual
> and the contractor's procedures.

## 1. Drawworks and hoisting
- **Block position limits:** the **crown saver** stops the travelling block before it
  hits the crown; the **floor saver** stops it before the floor. Function-test both at
  the start of each tour/hitch as procedure requires, and after any calibration change.
  Calibrate block height after slipping and cutting the line.
- **Hookload and weight-on-bit** come from the deadline anchor sensor; zero (tare) the
  weight indicator with the string off bottom and pumps on as procedure specifies.
- **Drill line:** track **ton-miles** (work done by the line) and slip and cut on the
  programme to move wear points. Inspect for broken wires, birdcaging and crushing,
  especially at the crossover points on the drum.
- Brakes: band brakes (older rigs) need adjustment and lining checks; disc and
  regenerative braking systems have their own checks. Test the emergency brake.

## 2. Top drive
- Check **makeup and breakout torque settings** for the pipe in use; incorrect
  settings overtorque or under-torque connections.
- **IBOP (internal blowout preventer) valves:** function and pressure test on schedule;
  they are part of well control equipment.
- Watch for torque spikes and stalls (stick-slip, packing off) and set the torque
  limit appropriately so the string isn't twisted off.
- Inspect the guide dolly/rails, link tilt, elevators and pipe handler for wear and
  loose bolts — dropped objects from the top drive are a major hazard.

## 3. Mud pumps
- **Pop-off (relief) valve** on each pump set at or below the weakest rated item in the
  high-pressure system (pump, standpipe, hoses). Test and reset per procedure; never
  cap or bypass it. Route discharge safely.
- **Pulsation dampener** precharge (often nitrogen at a fraction of operating pressure;
  check OEM) keeps pressure smooth — a flat dampener shows up as violent pressure
  swings.
- Listen and look for **liner and piston (swab) wear**: fluid at the liner wash, falling
  pump efficiency, knocking. Washouts in valves and seats show as pressure loss at the
  same strokes per minute.
- Lockout: isolate and **bleed pressure to zero** before opening a module; trapped
  pressure behind a valve cover kills.

## 4. Pipe handling and zone management
- Iron roughnecks, pipe handlers and racking systems move heavy steel automatically.
  **Zone management / anti-collision** software prevents machines clashing; red-zone
  rules keep people out of moving machine envelopes. Don't defeat interlocks to save
  time.
- When a machine faults, follow the recovery procedure; manual intervention in an
  energised machine's path is a classic serious-injury scenario.

## 5. Driller's display (EDR)
Watch hookload, standpipe pressure, pump strokes, torque, RPM, block height, ROP,
active pit and trip tank. Set **alarms with sensible limits** for pit gain/loss and
pressure changes — and keep them on.

## Gotchas
- Re-calibration after a line slip is commonly missed; the crown saver then trips late.
- Drill line damage shows first at the drum crossover and fastline.
- Pump pressure drop with no other change = washout (string or pump) until proven not.

## Verify
- [ ] Crown and floor savers function-tested and block height calibrated.
- [ ] Ton-miles tracked; line inspected; slip-and-cut on schedule.
- [ ] Top drive torque limits set; IBOP tested.
- [ ] Pop-offs set and tested; dampener charged.
- [ ] Zone management active; red-zone rules followed.
