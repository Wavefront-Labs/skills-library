---
id: transportation-logistics.traffic-transport-signalling.port-vessel-traffic-services.vts-watchkeeping-and-traffic-organisation
name: vts-watchkeeping-and-traffic-organisation
category: transportation-logistics
field: traffic-transport-signalling
product: port-vessel-traffic-services
tags: [vts, vessel-traffic-services, vtso, port-control, harbour-control, ais, radar, vhf, smcp, imo-smcp, message-markers, information-service, navigational-assistance, traffic-organisation-service, reporting-points, channel-sequencing, one-way-traffic, under-keel-clearance, pilotage, berth-coordination, iala, colregs]
level: practitioner
status: draft
description: "VTS watchkeeping: building the traffic image from radar and AIS, VHF calls with IMO SMCP message markers, sequencing vessels in restricted channels, and coordinating berths and pilots."
sources: ["IMO Resolution A.1158(32) Guidelines for Vessel Traffic Services (2021)", "IALA Guideline G1089 and VTS Manual", "IMO Standard Marine Communication Phrases (Res. A.918(22))"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VTS watchkeeping and traffic organisation

**Goal:** keep a complete, current picture of vessel traffic in your area, give clear
information and instructions on VHF, and sequence movements so ships never meet where
they can't pass.

## 1. Build the traffic image
- **Sensors:** radar (with tracking), AIS, CCTV, met/hydro sensors (wind, tide gauges,
  current), and the port's movement schedule.
- Correlate radar tracks with AIS targets; flag **radar targets without AIS** (small
  craft, AIS off) and **AIS positions that disagree with radar** (GNSS error or
  spoofing).
- Track each participating vessel from its first **reporting point** to berth or exit:
  name, call sign, draught, ETA, destination, pilot on board, special conditions
  (dangerous goods, restricted manoeuvrability, tow).
- Watch tide windows: deep-draught vessels need minimum under-keel clearance — check
  the predicted (and observed) height of tide for the transit time.

## 2. VHF communication
- Use **IMO Standard Marine Communication Phrases**; open with the vessel's name and
  your station: "<Ship>, this is <Port> VTS."
- Use message markers to make intent unambiguous:
  **INFORMATION**, **WARNING**, **ADVICE**, **INSTRUCTION**, **QUESTION**, **ANSWER**,
  **REQUEST**, **INTENTION**. e.g. "WARNING. Dredger working in the fairway, east side,
  between buoys 7 and 9."
- **INSTRUCTION** is used only where the VTS is authorised to give instructions
  (traffic organisation service) — know your legal authority.
- Read back critical items: positions, times, clearance.
- Never navigate the ship from shore: give information and traffic organisation, not
  helm or engine orders (that's the master/pilot's responsibility) unless your service
  includes formal navigational assistance procedures.

## 3. Organise traffic
- **Restricted channels** (one-way stretches, bends, bridges, locks): grant clearance
  to enter only when the opposing direction is clear; maintain a sequence list.
- Priorities follow port rules: e.g. deep-draught vessels on the tide window, vessels
  restricted in manoeuvrability, passenger ferries on schedule, then others.
- Set **meeting points** in wide sections when two-way passing is allowed.
- Space vessels for tug and pilot availability, berth readiness and lock cycles.
- Weather limits: suspend movements of certain classes above wind/visibility limits
  per port by-laws.

## 4. Berth and pilot coordination
- Confirm berth free and ready (lines handlers, shore crane clear) before letting a
  vessel leave the anchorage.
- Pilot boarding times and tug orders aligned with ETA updates; pass changes promptly.

## 5. Incidents
- Collision, grounding, man overboard, pollution: suspend traffic in the area,
  inform the coast guard/MRCC, broadcast warnings, keep a timed log of all
  communications (recording is usually automatic — note times anyway).

## Gotchas
- AIS draught and destination are manually entered and often wrong — confirm by VHF.
- Fixation on big ships while small craft wander into the channel.
- Over-talking: say only what helps; busy channels drown important calls.
- *Service levels and authority differ by port and national law.*

## Verify
- [ ] Every participating vessel tracked and identified, radar/AIS correlated.
- [ ] Calls use SMCP and correct message markers; critical info read back.
- [ ] No conflicting clearances into one-way sections (sequence list current).
- [ ] UKC checked for deep-draught transits against tide predictions.
- [ ] Watch log complete and handover covers active movements and restrictions.
