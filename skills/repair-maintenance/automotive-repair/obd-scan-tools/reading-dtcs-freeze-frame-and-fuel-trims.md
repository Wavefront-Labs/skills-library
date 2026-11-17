---
id: repair-maintenance.automotive-repair.obd-scan-tools.reading-dtcs-freeze-frame-and-fuel-trims
name: reading-dtcs-freeze-frame-and-fuel-trims
category: repair-maintenance
field: automotive-repair
product: obd-scan-tools
tags: [automotive-repair, obd-scan-tools, obd-ii, eobd, scan-tool, code-reader, elm327, dtc, p-codes, freeze-frame, live-data, pids, fuel-trim, stft, ltft, o2-sensor, readiness-monitors, mode-06, misfire, p0300, p0171, bidirectional-controls, autel, launch, snap-on, torque-app]
level: practitioner
status: draft
description: "Use an OBD-II/EOBD scan tool properly: read DTCs and freeze frame before clearing, interpret fuel trims and O2 data, check readiness monitors and Mode $06, and use bidirectional tests."
sources: ["SAE J1979 / ISO 15031 (OBD-II services) and SAE J2012 (DTC definitions)", "US EPA OBD information for technicians"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading DTCs, freeze frame and fuel trims

**Goal:** get from a check-engine light to a confirmed fault, using the scan tool as a
data source, not a parts list. A DTC tells you which *test failed*, not which part is
broken. Applies to petrol cars and light trucks from 1996 (US) / 2001 petrol, 2004 diesel (EU).

## 1. Connect and capture before touching anything
1. Connector (DLC) is under the dash, driver's side, within reach of the steering column.
   Ignition on (engine off) or running.
2. Tools range from ELM327 Bluetooth dongles with apps (generic OBD only) to pro scanners
   (Autel, Launch, Snap-on) with manufacturer-specific codes, all modules, and
   bidirectional controls. Generic OBD sees only emissions-related engine/transmission data.
3. **Read all codes**: stored (confirmed), pending and permanent. Pending = failed once;
   confirmed = failed on consecutive drive cycles (MIL on).
4. **Save the freeze frame** for each code: rpm, load, coolant temperature, vehicle speed,
   fuel trims and fuel system status at the moment the code set. This tells you *when* the
   fault happens (cold start? idle? highway?).
5. Only then clear codes, if needed — clearing erases freeze frame and resets readiness
   monitors (the car will fail an emissions inspection until they re-run).

## 2. Decode the code
- Format: letter (P powertrain, B body, C chassis, U network) + 0 (generic SAE) or 1
  (manufacturer-specific) + subsystem digit + two digits. E.g. **P0301** = cylinder 1 misfire
  detected; **P0171** = system too lean, bank 1.
- Look up **TSBs** for that code and vehicle (see
  `repair-maintenance.automotive-repair.service-information-systems.wiring-diagrams-tsbs-and-labour-times`)
  — known pattern failures save hours.
- Follow the manufacturer's diagnostic trouble-tree for the code when you have it.

## 3. Live data you'll use most
- **Fuel trims** (petrol): STFT (short-term, fast) and LTFT (long-term, learned), in %.
  Positive = ECU adding fuel (it sees lean); negative = removing (rich).
  - Total trim (STFT + LTFT) within about ±10 % is normal; beyond ±20–25 % usually sets
    P0171/P0172 or P0174/P0175.
  - **Lean at idle, normal at 2,500 rpm** → vacuum/intake leak (unmetered air is a bigger
    share at idle). **Lean everywhere, worse at load** → fuel delivery (pump, filter,
    pressure regulator, injectors) or a dirty/under-reading MAF.
  - Bank 1 vs bank 2 differ → fault specific to one bank (leak, injector, O2 sensor).
- **Upstream O2/AFR sensor:** narrowband switches ~0.1–0.9 V several times a second when
  warm in closed loop; wideband reads lambda (~1.00) or current. Downstream sensor should be
  steadier (catalyst storing oxygen); a downstream that mirrors upstream → catalyst efficiency
  (P0420).
- **Coolant temperature:** reaches ~85–105 °C; stuck-low thermostat keeps it cold
  (rich running, P0128).
- **MAF g/s at idle:** rough check ~ engine litres × 2–3 g/s on many petrol engines (heuristic).
- **Misfire counters** per cylinder (Mode $06 or manufacturer data) show which cylinder
  even before a code sets.

## 4. Readiness monitors and Mode $06
- Readiness: catalyst, evap, O2 sensor, O2 heater, EGR, misfire, fuel, components. "Not
  complete" after clearing until the car completes its drive cycle.
- **Mode $06** shows on-board test results vs min/max limits — a component that passes
  but sits near the limit is a likely next failure.

## 5. Bidirectional tests (pro tools)
Command components to prove them: fuel pump on, EVAP purge/vent solenoids, cooling fans,
injector cut-out (cylinder contribution), EGR position, throttle relearn, ABS bleed.

## Gotchas
- Replacing an O2 sensor for a lean code is the classic mistake: the sensor is usually
  reporting a real lean condition correctly.
- Low battery voltage (< ~12 V cranking dips) produces spurious U-codes and module faults.
- Uncertain: numeric thresholds are rules of thumb; manufacturer specs govern.

## Verify
- [ ] All codes and freeze frames recorded before clearing.
- [ ] Code meaning and TSBs checked for the specific vehicle.
- [ ] Fuel trims compared at idle and 2,500 rpm; bank-to-bank compared.
- [ ] Repair confirmed by live data and monitors completing, not just the light going off.
