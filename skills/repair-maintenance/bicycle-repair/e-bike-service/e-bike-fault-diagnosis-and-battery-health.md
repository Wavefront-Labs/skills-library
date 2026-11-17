---
id: repair-maintenance.bicycle-repair.e-bike-service.e-bike-fault-diagnosis-and-battery-health
name: e-bike-fault-diagnosis-and-battery-health
category: repair-maintenance
field: bicycle-repair
product: e-bike-service
tags: [bicycle-repair, e-bike-service, ebike, pedelec, bosch, bosch-diagnostic-tool, shimano-steps, e-tube, yamaha, brose, bafang, specialized-turbo, mid-drive, hub-motor, battery-health, lithium-ion, charge-cycles, error-codes, speed-sensor, magnet, firmware-update, controller, wiring-harness, connectors, multimeter, dielectric-grease, battery-storage, thermal-runaway]
level: practitioner
status: draft
description: "Triage e-bike faults: read error codes with the maker's tool, fix speed-sensor and connector faults, assess battery health and voltage, update firmware and store batteries safely."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# E-bike fault diagnosis and battery health

**Goal:** find the faulty part of the drive system quickly using the maker's
diagnostics and a short physical checklist, and advise on battery health without
opening a pack. Motors and battery cells are almost always replace-or-send-to-maker
items; your job is to prove which one, and to fix the wiring, sensor and software faults
that cause most callbacks.

## 1. Identify the system
Read the motor casing and display: Bosch (Performance Line, CX, SX), Shimano STEPS / EP8 /
EP801, Yamaha PW, Brose (Specialized Turbo), Fazua, TQ, Bafang (common on aftermarket
kits and budget bikes), or a rear hub motor. Each has its own dealer tool:
- **Bosch:** DiagnosticTool 3 (dealer login) — fault log, component versions, updates.
- **Shimano:** E-TUBE PROJECT (Professional for dealers) via a PC link cable or Bluetooth.
- **Specialized:** Mission Control app / Turbo Studio; **Yamaha/Brose/Fazua** have
  their own dealer software. Bafang: programming cable and community tools — note this
  can void warranty and road-legal limits.
Without the tool you can still read the display's error code and look it up in the
maker's code list.

## 2. Triage order
1. **Record the error code**, when it occurs (at power-on, under load, intermittently).
2. **Power cycle:** off, remove battery, wait 30 s, refit, power on. Many codes are
   transient.
3. **Speed sensor (most common fault):** spoke or rotor magnet must pass the sensor
   within the specified gap (Bosch: typically under ~17 mm; check model). Symptoms:
   assist cuts out, speed reads zero, error code for speed signal. Check magnet hasn't
   slid, sensor cable isn't pinched at the chainstay.
4. **Connectors:** unplug, inspect for green corrosion, bent pins, water. Clean with
   contact cleaner, dry, a thin film of dielectric grease where the maker allows, refit
   until it clicks. Check the battery terminals and the dock.
5. **Firmware:** update all components together via the dealer tool — mismatched
   versions cause odd codes, especially after a component swap.
6. **Then** motor or battery: use the tool's self-tests and logs (motor hours, error
   history, battery cycles and health %).

## 3. Battery health
- **Dealer tool reading** of state of health / full-charge-equivalent cycles is the
  reliable measure. Bosch packs are commonly rated around 500 full cycles before
  noticeable capacity loss (check current spec) — capacity fades gradually, not a cliff.
- **Voltage check** with a multimeter on the discharge terminals (if accessible and
  pack is on): a nominal 36 V pack reads ~42 V full and should not sit below ~30 V; a
  "dead" pack at near 0 V may have gone into protection — do not attempt to force-charge.
- **Range complaints:** check tyre pressure, brake drag, assist mode use, cold weather
  (capacity drops noticeably near 0 °C), and the battery's health % before condemning it.

## 4. Safety and storage
- Never open, re-cell or repair a lithium-ion pack unless trained and authorised; never
  use a charger other than the maker's.
- Quarantine any pack that is swollen, dropped hard, water-soaked or smells sweet: store
  outdoors or in a fire-safe container away from exits, and arrange specialist disposal.
- Storage: **30–60% charge**, 10–20 °C, dry; check monthly. Don't leave on charge
  unattended for days, don't charge below ~0 °C.
- Transport: damaged lithium batteries are dangerous goods — use a specialist courier.

## 5. Mechanical points specific to e-bikes
- Chains and cassettes wear 2–3x faster; use e-bike-rated chains and check at every visit.
- Motor mounting bolts: check torque at service (often 8–10 N·m range; confirm per brand).
- Wash with low pressure only; never jet the motor, display or connectors.

## Gotchas
- A replaced speed sensor or display with old firmware can throw new codes; update.
- Tuning devices ("chips") to exceed 25 km/h (EU) / class limits void warranties and can
  make the bike a moped in law — record and advise, don't fit.
- Don't confuse a worn chain slipping under motor torque with a motor fault.

## Verify
- [ ] Error code and system/version recorded before and after.
- [ ] Speed sensor gap and magnet position correct; speed reads on test ride.
- [ ] All connectors clean, dry, fully clicked.
- [ ] Firmware updated consistently across components.
- [ ] Battery health % and cycles recorded; storage/charging advice given.
- [ ] Assist works in every mode, cuts at the legal limit, no codes on a 10-minute ride.
