---
id: defence-public-safety.firefighting.fire-apparatus-and-pumps.pump-operation-and-fireground-hydraulics
name: pump-operation-and-fireground-hydraulics
category: defence-public-safety
field: firefighting
product: fire-apparatus-and-pumps
tags: [firefighting, fire-apparatus-and-pumps, pump-operator, driver-operator, engineer, fire-engine, pumper, fireground-hydraulics, friction-loss, pump-discharge-pressure, pdp, nozzle-pressure, elevation-loss, hydrant, drafting, relay-pumping, cavitation, pressure-relief-valve, pressure-governor, tanker-shuttle, aerial-ladder, outriggers, nfpa-1002, nfpa-1901, nfpa-1911]
level: practitioner
status: gated
description: "Driver/operator pump practice: water supply, friction loss and pump discharge pressure calculations, relay pumping, cavitation and pressure-relief control, and aerial setup basics."
sources: ["NFPA 1002 Standard for Fire Apparatus Driver/Operator Professional Qualifications (nfpa.org; free read-only access)", "IFSTA Pumping and Aerial Apparatus Driver/Operator Handbook"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pump operation and fireground hydraulics

**Goal:** get the right flow at the right pressure to every line, keep water supply
continuous, and never injure a crew with a pressure surge. Reference for
driver/operators (NFPA 1002 competencies in the US); your apparatus manual and
service SOPs govern the specifics. US units are used below; metric services use bar and L/min
with different rule-of-thumb constants.

## 1. Water supply first
- **Hydrant:** lay supply line from hydrant to fire (forward lay) or fire to hydrant
  (reverse lay). Flush the hydrant, open fully (partly open hydrants can erode their
  drains), and note static vs residual pressure on the intake gauge.
- **Drafting** from static sources: hard suction, strainer submerged clear of the
  bottom, prime the pump; lift (vertical distance) limits capacity.
- **Tank water** is a short bridge (often 500–1,000 gal): know how many minutes it
  lasts at your flow.
- Rural: tanker/tender shuttles and portable dump tanks; continuous flow depends
  on cycle times.

## 2. The core equation
**PDP = NP + FL + EL (± appliance loss)**
- **NP (nozzle pressure):** smooth-bore handlines typically 50 psi (master streams
  ~80 psi); fog nozzles 100 psi, or lower for low-pressure designs (often 50–75 psi) (IFSTA/NFPA-style figures, not fetched (gated: unconfirmed, source is paywalled or blocked)).
  Use the manufacturer's figure.
- **FL (friction loss):** FL = C × (Q/100)² × (L/100), with Q in gpm, L in feet
  and C a coefficient per hose diameter (e.g. ~15.5 for 1¾-inch, 2 for 2½-inch, 0.2 for 4-inch
  LDH (gated: unconfirmed, source is paywalled or blocked) — values vary by hose make; calibrate with flow testing).
- **EL (elevation):** about 0.5 psi per foot (the head of water is 0.433 psi per foot; 0.5 is the usual rounded-up fireground figure), or 5 psi per storey above the first (gated: unconfirmed, source is paywalled or blocked).
- **Appliance loss:** wyes, standpipes, master stream devices (often 10–25 psi (gated: unconfirmed, source is paywalled or blocked)).
Example: 150 gpm through 200 ft of 1¾-inch to a 50 psi fog nozzle on the second
floor: FL = 15.5 × 1.5² × 2 = 69.75 ≈ 70 psi; EL ≈ 5; PDP = 50 + 69.75 + 5 = 124.75 ≈ 125 psi (arithmetic recomputed).
Many services pre-calculate standard lines and post them on the panel.

## 3. Running the panel
- Engage the pump per the manufacturer's sequence; confirm "pump engaged" and road
  gear interlock before leaving the cab; chock wheels.
- Set the **pressure governor** or **relief valve** before charging lines, so
  closing one nozzle doesn't surge the others.
- Open and close discharges **slowly** to avoid water hammer.
- Watch intake pressure: keep a positive residual (commonly ≥ 20 psi on a hydrant (gated: unconfirmed, source is paywalled or blocked))
  to avoid collapsing the supply line or drawing a vacuum on the main.
- **Cavitation** (rattling noise, pressure that doesn't rise with throttle) means you are
  asking for more water than you are getting — throttle back.

## 4. Relay pumping
For long distances, engines in series with large-diameter hose. Relay calculations
start at the attack engine's requirement and work back; each relay engine maintains a
set intake residual. Communications between operators are essential.

## 5. Aerials (outline)
Level and stabilise on firm ground with outriggers fully deployed as the manufacturer
requires; check overhead power lines; respect load charts (waterway in use, angle,
extension, people on the tip). Aerial work is a separate qualification.

## Gotchas
- Kinks and sharp bends add unaccounted friction loss.
- Tank-to-pump valve left open when switching to hydrant supply recirculates; check
  valve positions.
- Pump overheating when lines are shut — use the circulator/tank fill.

## Verify
- [ ] Water supply established and intake residual known.
- [ ] PDP calculated for each line and governor/relief set before charging.
- [ ] Nozzle teams confirm adequate stream (flow test or flowmeter).
- [ ] Apparatus chocked, pump engaged indicators confirmed.
