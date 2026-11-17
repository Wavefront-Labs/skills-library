---
id: transportation-logistics.warehousing.automated-handling-systems.monitoring-and-jam-recovery-for-asrs-sorters-and-robots
name: monitoring-and-jam-recovery-for-asrs-sorters-and-robots
category: transportation-logistics
field: warehousing
product: automated-handling-systems
tags: [as-rs, asrs, automated-storage-retrieval, shuttle-system, miniload, autostore, conveyor, sortation, tilt-tray, cross-belt, shoe-sorter, amr, agv, goods-to-person, wcs, wes, scada, jam-clearing, lockout-tagout, loto, e-stop, recirculation, no-read, throughput, oee, mhe-controls]
level: practitioner
status: draft
description: "Running warehouse automation: reading WCS/SCADA dashboards, spotting throughput killers (no-reads, recirculation), safe jam clearing with LOTO, and restarting AS/RS, sorters and robots."
sources: ["OSHA 29 CFR 1910.147 (control of hazardous energy)", "ISO 13850 (emergency stop) and ISO 3691-4 (driverless industrial trucks)", "Vendor operator manuals concepts (AutoStore, Dematic, Honeywell Intelligrated, Vanderlande)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring and jam recovery for AS/RS, sorters and robots

**Goal:** keep automated flow near its design rate, recover from faults quickly, and
never put a hand into moving equipment. Vendor screens differ; the controls hierarchy
(WMS → WES/WCS → PLC/SCADA → equipment) and the principles don't.

## 1. Watch the right numbers
- **Throughput vs. plan** per subsystem (cartons/hour inducted, sorted, stored/retrieved).
- **Sorter:** induction rate, **no-read/no-scan rate** (target typically < 1–2 %),
  **recirculation rate**, full/blocked chute alarms, reject lane volume.
- **Conveyor:** accumulation zones full, photo-eye blocked timers, motor faults.
- **AS/RS / shuttles / cube storage (AutoStore-type):** retrieval cycle time, robots
  in error, port queue length, bins in error.
- **AMR/AGV fleets:** robots available vs. charging vs. faulted, traffic hotspots,
  mission age.
Trend these by hour; a rising no-read rate usually means a dirty scanner window,
a label quality problem from one supplier, or a misaligned tunnel.

## 2. Common causes and first actions
| Symptom | Likely cause | First action |
|---|---|---|
| Recirculation climbing | Destination chutes full/unmanned; WCS allocation mismatch | Staff the chutes, release full lanes, check assignment |
| No-reads | Labels (glossy, wrinkled, wrong position), scanner dirty | Clean scanner window, check sample labels, feed supplier back |
| Jams at merges | Oversized/non-conveyable items, poor gapping | Remove item, divert non-conveyables to manual flow |
| Robot stuck | Debris on floor, lost localisation (fiducial/QR damaged), battery | Clear via fleet manager procedure; never walk into the grid without lockout |
| AS/RS retrieval errors | Bin overweight/overheight, sensor misread | Remove and inspect bin at the service port |

## 3. Safe jam clearing
1. **Stop the zone** via the control (not just an E-stop on a running system, unless
   urgent). Know which zones a stop affects upstream/downstream.
2. **Lockout/tagout** for any entry into the machine envelope or reach past guards:
   isolate energy (electrical, pneumatic, gravity — e.g. raised lifts, stored
   tension in belts), apply personal lock, **verify zero energy** by trying to start.
3. Clear the jam with tools where possible; remove the cause (broken pallet, strap).
4. Remove locks only after everyone is out; account for every person.
5. Restart: reset the zone, watch the first items through the jam point.
For AMR/robot grids: use the system's service mode to stop/park robots in the area
and follow the access procedure (permit, lock, buddy) — robots can move without
warning.

## 4. Restart after a stoppage
- Bring systems up **downstream first** (sorter and outbound before induction) so
  product has somewhere to go.
- Reconcile items in transit during the stop: WCS may lose track of cartons
  manually removed — rescan or re-induct them; otherwise they become "ghosts".
- Check WMS-WCS interface: messages queued during the outage processed in order.

## 5. Preventive habits
- Daily: walk the system, listen for bearings, clean scanners/photo-eyes, empty
  debris trays.
- Track faults by location and code; top 5 recurring faults go to maintenance with data.

## Gotchas
- Resetting an E-stop doesn't make the area safe; LOTO does.
- Downtime from a single chute being full can stop an entire sorter.
- *Thresholds above are typical; vendors set their own design values.*

## Verify
- [ ] Hourly dashboard review: throughput, no-reads, recirculation, faults.
- [ ] Every machine entry used LOTO with verified zero energy.
- [ ] Restart sequence downstream-first; in-transit items reconciled.
- [ ] Recurring faults logged and sent to maintenance with counts.
