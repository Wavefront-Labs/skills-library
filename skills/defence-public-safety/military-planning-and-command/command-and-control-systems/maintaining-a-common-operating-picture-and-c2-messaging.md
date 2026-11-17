---
id: defence-public-safety.military-planning-and-command.command-and-control-systems.maintaining-a-common-operating-picture-and-c2-messaging
name: maintaining-a-common-operating-picture-and-c2-messaging
category: defence-public-safety
field: military-planning-and-command
product: command-and-control-systems
tags: [command-and-control-systems, c2-systems, c2is, battle-management-system, bms, common-operating-picture, cop, recognised-picture, rap, rmp, blue-force-tracking, friendly-force-tracking, app-6, mil-std-2525, military-symbology, track-management, data-latency, information-management, information-manager, knowledge-management, military-messaging, usmtf, adatp-3, link-16, nato-fmn, federated-mission-networking, interoperability, pace-plan, degraded-operations, analogue-backup, map-board, sop, classification, data-hygiene]
level: practitioner
status: draft
description: "Operate C2 systems as a staff: manage the common operating picture (symbology, track hygiene, latency), formatted messaging, interoperability with allies, and PACE plans for degraded operations."
sources: ["NATO APP-6 Joint Military Symbology (public edition) and US MIL-STD-2525", "NATO Federated Mission Networking (FMN) public overview", "US Army FM 6-0 (information and knowledge management chapters)", "US Army ATP 6-01.1 Techniques for Effective Knowledge Management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining a common operating picture and C2 messaging

**Goal:** a headquarters' C2 systems present a picture the commander can trust, messages
reach the right people in a format machines and humans both understand, and the HQ keeps
working when networks degrade. Specific systems differ by nation and service (and their
operating details are often restricted); these practices are system-agnostic, at the
level of published doctrine.

## 1. What the common operating picture (COP) is
- A single displayed picture of relevant information — friendly and adversary positions,
  boundaries and control measures, key terrain, civil considerations — **shared across
  echelons** and tailored by each.
- Built from feeds: friendly force tracking, intelligence tracks, sensor and data links,
  manual inputs from reports. Each has **latency and reliability** characteristics; the
  operator must know them.
- Domain pictures (e.g. recognised air or maritime pictures) feed the joint COP.

## 2. Keeping the picture trustworthy
- **Ownership:** one cell (usually current operations, with an information manager)
  owns the COP; others submit inputs, not edits.
- **Symbology:** use the current standard (NATO APP-6 / US MIL-STD-2525) consistently —
  affiliation, echelon, status (present vs planned/anticipated). Wrong affiliation colours
  are a serious error, not cosmetic.
- **Track hygiene:** timestamp every manual entry, show "as of" time, age out stale tracks
  by rule, merge duplicates, mark unconfirmed reports clearly. A cluttered picture is
  ignored; a stale one is dangerous.
- **Control measures** (boundaries, phase lines, coordination lines) are loaded from the
  current order and FRAGOs — version-control them with the order.
- **Overlays/layers:** keep the base view simple; let users toggle detail.
- **Verify** with voice/radio reports at set times; "the system says" is not confirmation.

## 3. Messaging
- **Formatted messages** (e.g. NATO ADatP-3, US USMTF and their national variants;
  tactical data links like Link 16 for machine-to-machine) allow automatic parsing and
  reduce ambiguity. Know the reports in your SOP — situation report, intelligence summary,
  logistics status report, casualty report — and their schedules.
- Precedence levels and distribution lists set in the SOP: overuse of high precedence
  degrades the whole network.
- Write free text with the same discipline as briefs: BLUF, date-time-group, location
  references in the agreed grid/datum.
- **Classification** and releasability marked on every product — essential in coalitions.

## 4. Interoperability
- Coalition operations require agreed standards for data exchange, symbology and
  services; NATO's **Federated Mission Networking (FMN)** sets these out in "spirals".
- Test interoperability **before** deployment or the exercise — most failures are
  configuration, certificates, map datum or version mismatches.
- Assign liaison officers with their own systems where technical links aren't possible.

## 5. Degraded operations (PACE)
- A **PACE** plan (primary, alternate, contingency, emergency) for each critical C2
  information flow — e.g. data network → satellite voice → HF radio → messenger.
- Maintain an **analogue backup**: a paper map board updated on a schedule, so the HQ
  can continue if systems fail or must go silent. Rehearse switching to it.
- Electronic signature and emissions management affect HQ survivability; follow the
  signals officer's guidance on what to transmit and when (the details are
  context-specific).

## 6. Roles
Information manager (rules for what goes where), knowledge manager (getting the right
understanding to decision-makers), system operators/administrators, and the current
operations watch officers who curate the COP.

## Gotchas
- Assuming every node sees the same picture — different filters and latency produce
  different "truths".
- Uncontrolled overlays copied between files spread errors.
- Time zones and map datums mismatched across allies.
- Training only on the system and never on analogue fallback.

## Verify
- [ ] COP has a named owner and an SOP for inputs, ageing and duplicates.
- [ ] Symbology follows APP-6/2525; status and "as of" times shown.
- [ ] Control measures match the latest order/FRAGO version.
- [ ] Message formats, schedules and precedence rules are in the SOP.
- [ ] PACE plan and analogue backup exist and have been rehearsed.
