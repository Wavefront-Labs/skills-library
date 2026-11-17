---
id: energy-mining-utilities.telecommunications-network-operations.cell-site-maintenance.clearing-site-down-power-and-vswr-alarms
name: clearing-site-down-power-and-vswr-alarms
category: energy-mining-utilities
field: telecommunications-network-operations
product: cell-site-maintenance
tags: [cell-site-maintenance, telecommunications-network-operations, cell-site, base-station, bts, nodeb, enodeb, gnodeb, rru, rrh, radio-unit, baseband-unit, bbu, cpri, vswr, return-loss, feeder, jumper, connector-weatherproofing, pim, rectifier, -48v-dc, battery-backup, vrla, generator, mains-failure, site-alarms, transmission-down, backhaul, site-access, rf-exposure, ericsson, nokia, huawei]
level: practitioner
status: draft
description: "Get a cell site back on air: separate power, transmission and radio faults from the alarm set, check rectifiers and batteries, chase VSWR to a connector, and swap a radio safely."
sources: ["Vendor site maintenance guides (Ericsson, Nokia, Huawei — general practice, paraphrased)", "ICNIRP / FCC RF exposure guidance (principles)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clearing site-down, power and VSWR alarms

**Goal:** when a mobile site drops off air or degrades, work out from the alarms
whether it's **power, transmission (backhaul) or radio**, go to site with the right
parts, and fix it without causing a second outage. Vendor names differ (Ericsson,
Nokia, Huawei, Samsung), but the logic is the same.

## 1. Triage from the NOC view before driving
- **All technologies and sectors down, no management access** → power or
  transmission. Check the power system alarms (mains fail, rectifier fail, battery
  low/disconnect) and the backhaul (microwave or fibre link alarms on the far end).
- **Site reachable, one sector or one band down** → radio side: radio unit (RRU/RRH),
  CPRI/eCPRI fibre between baseband and radio, antenna/feeder.
- **VSWR / return-loss alarm on one branch** → antenna line problem.
- **Mains failure with battery discharge** → you have hours, not days: battery
  autonomy is often 2–8 hours by design. Dispatch a generator early.

## 2. Site arrival
- Access per the site agreement (keys, landlord notice, rooftop permits). Log on with
  the NOC.
- **RF safety:** know the exclusion zones in front of antennas; on rooftops, stay
  behind the marked lines or ask the NOC to power down the sector before working near
  antennas.
- Look first: storm damage, tripped breakers, cabinet door alarms, water ingress.

## 3. Power faults
- DC plant is typically **−48 V DC** (positive grounded). Measure at the rectifier
  output and the battery string.
- **Rectifiers:** failed modules show alarm LEDs; hot-swap per the vendor.
- **Batteries (VRLA):** check string voltage under load, connector torque, swelling
  or heat. A string that collapses quickly on a mains failure needs replacing.
  Batteries are heavy and hold dangerous energy — insulated tools, no rings.
- **Low-voltage disconnect (LVD):** the site shuts down radio load before batteries
  are destroyed; after restoration, confirm the LVD reconnected.

## 4. VSWR alarms
VSWR (voltage standing wave ratio) rises when RF power is reflected — common alarm
thresholds are around 1.5:1 to 2:1 (vendor-set).
1. Note which branch/port. Check that the alarm isn't caused by a recent works
   (someone disconnected a jumper).
2. Inspect jumpers and connectors at the radio: loose, cracked, water in the
   connector, weatherproofing tape missing.
3. Sweep the line with a cable and antenna analyser (return loss and **distance-to-
   fault**) — DTF shows where along the feeder the reflection is.
4. Fix: re-terminate or replace the connector/jumper, re-weatherproof (self-amalgamating
   tape, then vinyl tape over), re-sweep.
Remote radios at the top of the tower mean climbing — see
energy-mining-utilities.telecommunications-network-operations.tower-work.climbing-a-telecom-tower-with-full-fall-protection.

## 5. Radio or baseband swap
- Confirm the replacement's part number and software compatibility with the NOC.
- Lock/block the cell in the OSS first; swap; let it load software and configuration;
  unlock; confirm traffic and KPIs (call setup, throughput) with the NOC before leaving.
- Return the faulty unit with the fault description.

## Gotchas
- Passive intermodulation (PIM) from loose metal or rusty bolts near antennas
  raises uplink noise without a VSWR alarm.
- Swapping a radio without locking the cell can cause alarms storms and dropped calls.
- Uncertain: thresholds, voltage systems (some sites +24 V or AC radios) and procedures
  are vendor- and operator-specific.

## Verify
- [ ] Fault class (power / transmission / radio) identified before dispatch.
- [ ] RF exclusion zones respected; NOC informed on arrival and departure.
- [ ] DC voltage and battery health measured and recorded.
- [ ] VSWR fixed with a post-repair sweep saved.
- [ ] Cell unlocked, traffic confirmed by the NOC before leaving.
