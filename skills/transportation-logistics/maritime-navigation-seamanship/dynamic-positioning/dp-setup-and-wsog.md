---
id: transportation-logistics.maritime-navigation-seamanship.dynamic-positioning.dp-setup-and-wsog
name: dp-setup-and-wsog
category: transportation-logistics
field: maritime-navigation-seamanship
product: dynamic-positioning
tags: [dynamic-positioning, dp, dpo, dp-operator, maritime-navigation-seamanship, dp-class, dp2, dp3, position-reference-systems, dgnss, taut-wire, hpr, usbl, fanbeam, cyscan, radius, wsog, asog, cam, tam, capability-plot, consequence-analysis, footprint, drive-off, drift-off, blackout, imca, imca-m103, imca-m220, offshore-supply-vessel, station-keeping]
level: advanced
status: draft
description: "Set up a DP vessel for a task: pre-field checklist, select and pool position references, check capability plots, apply the WSOG/ASOG green-blue-yellow-red limits, and respond to drive-off."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DP setup and WSOG — hold station, know when to stop

**Goal:** bring a dynamic-positioning vessel onto location, configure sensors and
thrusters for the required redundancy, and operate within agreed limits so that a
single failure never becomes a position loss near an installation. This summarises
common industry practice (IMCA guidance, IMO MSC/Circ.1580 DP guidelines); the
vessel's DP operations manual and the activity-specific WSOG/ASOG are the authority.

## 1. Before entering the 500 m zone
- **Field arrival / location checklist** completed (company form): all thrusters
  tested in DP, both DP controllers healthy, UPS on, power plant in required mode
  (e.g. split bus for DP2/DP3 critical activity — CAM — or the configuration the
  FMEA allows for TAM).
- Wind, current and sea within limits; weather forecast checked for the work period.
- Communication with the installation and set up of the **WSOG/ASOG** (well-specific /
  activity-specific operating guidelines) agreed and signed by master and client.
- Settle on DP outside the zone (e.g. 10–15 min) to let the model learn current
  before approaching.

## 2. Position reference systems (PRS)
- Use **at least three** independent PRS for DP2/DP3 critical operations, ideally of
  different principles: e.g. two DGNSS (with different correction sources), plus a
  laser/radar (Fanbeam, CyScan, RadaScan) or acoustic (HPR/USBL) or taut wire.
- Check each reference before pooling: plausible, stable, low noise. The DP weights
  references by variance — a jumping reference can drag the model.
- Watch for common-mode failure: all DGNSS degraded by ionospheric activity or
  shadowing near a platform; reflections for laser targets; acoustic noise from thrusters.
- Check **heading** sources (gyros) and **wind** sensors (at least two, compare —
  a sheltered sensor near a platform gives wrong feed-forward).

## 3. Capability and consequence
- **Capability plot:** for the current environment, can the vessel hold position
  with all thrusters, and after the **worst-case single failure** (WCF)?
  Keep operating below the WCF capability, with margin.
- **Consequence analysis** (online, DP2/3): alarms when the WCF would leave insufficient
  thrust. Treat it as an advisory status change per the WSOG.
- Thruster load: sustained high utilisation (e.g. >~45–50% average for some setups)
  is a warning sign of limited reserve — check the vessel's specific limit.

## 4. WSOG / ASOG status
| Status | Meaning | Action |
|---|---|---|
| Green | Normal | Continue |
| Blue (advisory) | Approaching limits or degraded | Risk assess, inform client, consider stopping |
| Yellow | Reduced status | Stop operations, prepare to disconnect/move away |
| Red | Emergency | Execute emergency disconnect/move to safety |
Typical criteria: position excursion (e.g. yellow at 3 m, red at 5 m — task-dependent),
loss of a PRS, thruster or generator trip, power utilisation above limit, weather
over limit, DP alarm. Agree and post them on the bridge.

## 5. Failures: drift-off vs drive-off
- **Drift-off** (blackout/loss of thrust): vessel moves with the environment — set up so
  that drift direction is away from the installation where possible (work on the lee/"blow-off" side).
- **Drive-off** (DP pushes vessel the wrong way due to bad reference or heading):
  recognise early from thruster commands diverging from expected and position trend;
  deselect the bad reference, or take **manual/joystick** control. Practise drills.

## 6. During operations
- Two DPOs on the bridge for critical activity; hourly checklist (PRS status, power,
  thruster loads, environment).
- Log all events; never change major configuration without informing the client.
- Watch handover: references, alarms, WSOG status, ongoing activity, weather trend.

## Gotchas
- Model not settled after setup → poor current estimate → erratic thruster use.
- Using two DGNSS on the same correction service as "two independent" references.
- Moving heading too fast while close to a structure.

## Verify
- [ ] Location checklist and WSOG signed before entering the 500 m zone.
- [ ] ≥3 healthy, diverse PRS pooled; two heading and wind sources compared.
- [ ] WCF capability exceeds current environment with margin.
- [ ] Drive-off/drift-off response rehearsed; manual takeover known by both DPOs.

*Uncertainty:* numeric limits are illustrative only; real values come from the vessel's FMEA, DP manual and WSOG.
