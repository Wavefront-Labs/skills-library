---
id: defence-public-safety.search-and-rescue.maritime-search-and-rescue.maritime-sar-coordination-search-patterns-and-person-overboard
name: maritime-sar-coordination-search-patterns-and-person-overboard
category: defence-public-safety
field: search-and-rescue
product: maritime-search-and-rescue
tags: [search-and-rescue, maritime-search-and-rescue, maritime-sar, iamsar, iamsar-manual, solas, gmdss, epirb, plb, ais-sart, dsc, mayday, rcc, mrcc, jrcc, on-scene-coordinator, osc, datum, leeway, total-water-current, drift, expanding-square, sector-search, track-line-search, parallel-sweep, person-overboard, williamson-turn, lifeboat, rnli, coastguard, surf-rescue]
level: practitioner
status: gated
description: "Maritime SAR reference: IAMSAR roles (RCC, OSC), distress alerting (GMDSS, EPIRB), datum and drift, expanding square, sector and track-line patterns, and person-overboard recovery."
sources: ["https://www.imo.org/en/ourwork/safety/pages/iamsarmanual.aspx", "https://cospas-sarsat.int/en/beacons-pro/experts-beacon-information/beacon-carriage-requirements-pro", "https://www.dco.uscg.mil/Portals/9/CG-5R/nsarc/BalticAcoManual.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maritime SAR coordination, search patterns and person-overboard

**Goal:** understand how a sea search is coordinated and executed so that a vessel,
lifeboat crew or aircrew can play its part correctly. The reference is the
**IAMSAR Manual** (International Aeronautical and Maritime Search and Rescue, ICAO/IMO),
Vol. I (organisation), II (mission coordination) and III (mobile facilities — carried
on ships). Use the current edition (IMO lists the 2025 editions); rescue coordination centre instructions always win.

## 1. Alerting and roles
- **Distress alerts** reach a **Rescue Coordination Centre (RCC/MRCC/JRCC)** via VHF
  DSC/Channel 16 (Mayday), MF/HF DSC, satellite (Inmarsat), **EPIRBs** (406 MHz,
  Cospas-Sarsat) and **PLBs**, and SART transponders on survival craft (gated: unconfirmed, source is paywalled or blocked).
- The RCC is the **SAR Mission Coordinator (SMC)**. It may appoint an **On-Scene
  Coordinator (OSC)** — often a lifeboat, coastguard cutter or the first capable ship —
  to coordinate assets on scene. Ships have a SOLAS obligation to respond to distress where able (gated: unconfirmed, source is paywalled or blocked).

## 2. Datum and drift
The search centres on a **datum** — the most probable position of the search object,
corrected for movement since the last known position:
- **Total water current** (sea current + tidal stream + wind-driven current).
- **Leeway:** the object's own drift from wind, which depends heavily on the object
  (a person in the water has little leeway; a liferaft with no drogue drifts more and
  diverges left/right of the downwind direction). IAMSAR tables give leeway rates by object type (gated: unconfirmed, source is paywalled or blocked).
Error grows with time, so the search area grows; modern RCCs use drift-modelling software (e.g. SAROPS in the US (gated: unconfirmed, source is paywalled or blocked)), but IAMSAR Vol. III gives manual methods for ships.

## 3. Search patterns (IAMSAR Vol. III)
- **Expanding square (SS):** starting at datum, legs increasing in length by one track spacing every second leg (gated: unconfirmed, source is paywalled or blocked); used when the position is fairly well known and for
  a single vessel. Precise navigation matters.
- **Sector search (VS):** radial legs through datum, for a small area and a
  well-defined datum (e.g. person overboard witnessed); a marker can be dropped at datum.
- **Track-line search (TS):** along the intended route of a missing vessel or aircraft.
- **Parallel sweep (PS):** large areas, multiple units abreast at set spacing.
**Track spacing** is chosen from the sweep width for the object, visibility and sea
state, and the probability of detection required.

## 4. Person overboard (own vessel)
1. Shout "man overboard" and the side; throw a lifebuoy with light/smoke; press the
   MOB button on GPS/chart plotter; assign a pointer who never takes their eyes off the person.
2. Manoeuvre: **Williamson turn** (returns to the original track — good at night or in restricted visibility), **Anderson turn** (quick, for a seen person), or a **Scharnow turn** (when the event is noticed after some delay) (gated: unconfirmed, source is paywalled or blocked) — choose by vessel and situation.
3. Alert the RCC (Mayday or Pan-Pan as appropriate) — others can help.
4. Recovery is often harder than finding: plan a recovery method (sling, scramble net,
   rescue boat) that keeps a cold, exhausted person horizontal where possible.

## Gotchas
- Cold water: incapacitation from cold shock and swim failure comes well before hypothermia (gated: unconfirmed, source is paywalled or blocked) — time matters.
- Lookout effectiveness drops quickly with fatigue; rotate lookouts.
- Datum from an old position is a guess; the RCC's updated datum takes precedence.

## Verify
- [ ] Alert reached the RCC; OSC identified if appointed.
- [ ] Datum, drift factors and search pattern recorded.
- [ ] Track spacing and pattern chosen for the object and conditions.
- [ ] Your crew can execute a person-overboard drill and a recovery method.

## Checked

Checked 2026-10-25. Jurisdiction: International (IMO/ICAO IAMSAR); US examples named. Source versions: IMO IAMSAR page (2025 editions of Volumes I to III listed as current in the June 2026 IMO publications listing); Cospas-Sarsat carriage page. Confirmed: Volume I covers organisation and management, Volume II mission coordination, Volume III mobile facilities; 406 MHz Cospas-Sarsat EPIRBs and PLBs; the pattern names and abbreviations SS, VS, PS and TS, with expanding square used when the datum is well known. The claims marked gated rest on the IAMSAR text, which is paywalled, or on sources that could not be read; no free primary source was found for them.

Method: documentation only; no commands were run.
