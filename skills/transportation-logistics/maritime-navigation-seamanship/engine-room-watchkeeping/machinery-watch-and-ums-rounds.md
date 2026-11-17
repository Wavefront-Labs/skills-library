---
id: transportation-logistics.maritime-navigation-seamanship.engine-room-watchkeeping.machinery-watch-and-ums-rounds
name: machinery-watch-and-ums-rounds
category: transportation-logistics
field: maritime-navigation-seamanship
product: engine-room-watchkeeping
tags: [engine-room-watchkeeping, engineering-watch, eow, engineer-officer-of-the-watch, maritime-navigation-seamanship, ums, unmanned-machinery-space, duty-engineer, engine-rounds, main-engine, auxiliary-engines, generators, purifiers, fuel-oil, lube-oil, bilge, oily-water-separator, oil-record-book, blackout, blackout-recovery, fuel-changeover, eca, alarm-monitoring, stcw-a-viii-2, jacket-water, scavenge-fire]
level: practitioner
status: draft
description: "Keep an engine-room watch or UMS duty: handover, round checklist (ME, gensets, purifiers, bilges), fuel and lube management, ECA fuel changeover, alarms, and blackout recovery sequence."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Machinery watch and UMS rounds — catch it at the trend, not the trip

**Goal:** keep propulsion and power running safely through your watch or night duty
(UMS — unmanned machinery space), detect abnormal trends early, and recover quickly
from failures, following STCW A-VIII/2 and the chief engineer's standing orders.

## 1. Taking over
- Read standing and night orders; check log and alarm history since last watch.
- Plant status: main engine load/rpm, generators running and load, purifiers,
  boilers, fresh water generator, any equipment isolated for maintenance (permits
  to work open!).
- Tank levels: fuel service/settling tanks, sludge, bilge holding, lube sumps.
- Fuel in use (sulphur grade) and upcoming changeovers (ECA entry).
- Bridge communications: manoeuvring expected? Weather?

## 2. Rounds (manned watch: hourly-ish; UMS: before going unmanned and at handover)
Use all senses — sight, sound, smell, touch (carefully):
- **Main engine:** exhaust temperatures per cylinder (spread), scavenge air pressure
  and temperature, jacket cooling water temperatures, lube oil pressure, cylinder
  lube feed rate, turbocharger noise/vibration, leaks (fuel, oil, water), crankcase
  oil mist detector status.
- **Generators:** load share, voltage/frequency, exhaust temps, oil and water pressures.
- **Purifiers:** sludge discharges occurring, throughput, temperature, no overflow.
- **Pumps and coolers:** sea water pressure, sea chest strainers, cooler ΔT.
- **Bilges:** levels and any unusual water/oil; source traced.
- Hot surfaces insulated, no oil-soaked lagging (fire risk).
- Record readings in the log; compare with previous days — trends matter more
  than single readings.

## 3. UMS readiness (before leaving the engine room unattended)
- All alarms tested per schedule (company UMS checklist: fire detection, bilge high
  level, key engine alarms, extension alarm to duty engineer's cabin/mess).
- Service tanks full, transfer arranged so they won't run dry overnight; purifiers stable.
- Standby generator in auto, standby pumps in auto; no open work.
- Inform the bridge that the engine room is unmanned and who is duty engineer.
- Dead-man/engineer alarm system operational when entering alone at night.

## 4. Fuel management and ECA changeover
- Changeover from HFO to compliant low-sulphur fuel early enough that the fuel
  system is fully flushed before the ECA boundary: compute time from tank and pipe
  volumes and consumption; log start/finish times, positions and tank levels
  (MARPOL Annex VI record).
- Temperature change gradually (often ≤ ~2 °C/min) to avoid fuel pump sticking;
  watch viscosity — distillates may need coolers to keep minimum viscosity.
- Fuel samples (MARPOL sample) kept; bunker quality issues reported.

## 5. Alarms and failures
- Acknowledge, investigate the cause, inform bridge if propulsion/steering affected.
- Never reset safety trips repeatedly without finding the cause.
- **Blackout recovery** (typical sequence, check your plant): standby generator
  auto-starts and connects; if not, start manually and close breaker; restore
  essential loads in order — steering gear, lubricating oil pumps, cooling water
  pumps, fuel supply, then main engine restart with bridge consent; then non-essential
  loads. Report to bridge immediately and log.
- Scavenge fire signs: high exhaust temp on a cylinder, smoke/sparks at scavenge drains —
  reduce load, increase cylinder lube, follow engine-maker procedure.

## 6. Environmental
Bilge water discharged only via oily water separator with 15 ppm monitor working,
outside special areas, recorded in the **Oil Record Book**; never bypass.

## Gotchas
- Readings logged but not compared — trends missed.
- Changeover started late → off-spec fuel inside the ECA.
- Standby equipment not actually in auto mode.
- Working alone without the dead-man alarm.

## Verify
- [ ] Rounds completed and readings logged and compared with previous.
- [ ] UMS checklist done; bridge informed of unmanned status.
- [ ] Fuel changeover planned, executed and logged before the ECA line.
- [ ] Blackout recovery steps posted and practised.
- [ ] Oil Record Book entries match operations.

*Uncertainty:* sequences and limits are generic; plant-specific manuals and the chief engineer's orders govern.
