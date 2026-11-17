---
id: defence-public-safety.air-and-space-warfare.military-space-operations.space-domain-awareness-satellite-operations-and-space-doctrine
name: space-domain-awareness-satellite-operations-and-space-doctrine
category: defence-public-safety
field: air-and-space-warfare
product: military-space-operations
tags: [military-space-operations, space-operations, space-power, space-doctrine, space-force, space-command, space-domain-awareness, sda, space-situational-awareness, ssa, satellite-catalogue, conjunction-assessment, collision-avoidance, space-track, tle, two-line-elements, satellite-operations, tt-and-c, telemetry-tracking-and-command, station-keeping, anomaly-resolution, leo, meo, geo, heo, molniya-orbit, pnt, gps, satcom, missile-warning, space-based-isr, space-weather, launch-support, responsive-launch, space-control, counterspace, asat, anti-satellite, kessler-syndrome, space-debris, outer-space-treaty, gulf-war-first-space-war, starlink-ukraine, spacepower-doctrine, space-capstone-publication, jp-3-14, staff-college, air-power-doctrine]
level: practitioner
status: draft
description: "Doctrine-level military space: orbits and what each does, space mission areas, space domain awareness and conjunction assessment, satellite ops basics, counterspace categories, debris and law."
sources: ["US Space Force, Spacepower: Space Capstone Publication (2020)", "US Joint Publication 3-14 Space Operations (public edition)", "NATO Overarching Space Policy (2022, public)", "Secure World Foundation, Global Counterspace Capabilities: An Open Source Assessment (annual)", "CSIS Aerospace Security Project, Space Threat Assessment (annual)", "Treaty on Principles Governing the Activities of States in the Exploration and Use of Outer Space (1967)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Space domain awareness, satellite operations and military space doctrine

**Goal:** understand military space operations as public doctrine and open-source analysis
describe them: what militaries use space for, how they keep track of what is in orbit,
what operating a satellite involves, and the strategic, legal and debris issues of
conflict in space. Classified capabilities and anything resembling counterspace
targeting are out of scope.

## 1. Orbits and what each is good for
| Orbit | Altitude (approx.) | Typical military use |
|---|---|---|
| **LEO** low Earth orbit | ~160–2,000 km | Imaging/ISR, weather, large comms constellations; short passes, many satellites needed |
| **MEO** medium Earth orbit | ~2,000–35,786 km (GNSS ~20,000 km) | Navigation (GPS, Galileo, GLONASS, BeiDou) |
| **GEO** geostationary | 35,786 km | Wide-area comms, missile-warning infrared, persistent view of one hemisphere |
| **HEO** e.g. Molniya | Highly elliptical | Long dwell over high latitudes (comms, warning) |
Physics shapes strategy: orbits are predictable, so satellites can't hide easily, and
manoeuvring costs fuel (see
`engineering-technology.aerospace-engineering.orbital-mechanics.delta-v-budget-and-transfers`).

## 2. Space mission areas
- **PNT** — positioning, navigation and timing; underpins precision weapons, finance, power
  grids. **SATCOM.** **ISR** and **missile warning.** **Environmental monitoring** (weather,
  space weather). **Launch** and on-orbit support.
- The 1991 Gulf War is often called the "first space war" because GPS, satellite comms and
  missile warning were first used at scale by ground and air forces.
- Ukraine since 2022 highlighted commercial space: commercial imagery and the Starlink
  constellation became military-relevant, raising questions about private firms in conflict.

## 3. Space domain awareness (SDA)
- Formerly "space situational awareness": knowing what is in orbit, where it is going,
  what it is and what it intends.
- Ground radars and telescopes (plus some space-based sensors) track objects; a **catalogue**
  of tens of thousands of tracked objects is maintained. Public element sets (two-line
  elements, via space-track.org) let anyone propagate orbits approximately.
- **Conjunction assessment:** predict close approaches and decide whether to manoeuvre.
  Operators balance probability of collision against fuel cost; false alarms are frequent.
- Characterising **intent** (inspection vs threat) is harder than tracking position.

## 4. Operating a satellite (basics)
- **TT&C** — telemetry, tracking and command — via ground stations with limited contact
  windows for LEO satellites.
- Routine work: health monitoring, **station-keeping** manoeuvres, payload tasking,
  software updates, **anomaly resolution** (often caused by space weather or component
  failure), end-of-life disposal.
- Operations floors run like other mission crews: checklists, shift handovers, contingency
  procedures.

## 5. Counterspace, debris and law (concept)
- Open-source assessments group counterspace capabilities as **direct-ascent kinetic**,
  **co-orbital**, **electronic** (jamming/spoofing), **directed energy** and **cyber**.
- **Debris:** destructive ASAT tests — China 2007 (thousands of tracked fragments) and
  Russia 2021 (Kosmos 1408) — created long-lived debris threatening all users, including the
  ISS. The **Kessler syndrome** describes cascading collisions. Several states have since
  pledged not to conduct such tests.
- **Outer Space Treaty (1967):** no nuclear weapons or WMD in orbit, no national appropriation,
  states responsible for their national activities; it does not ban conventional weapons in
  orbit — a gap at the centre of current diplomacy.

## Gotchas
- Treating space as a sanctuary — doctrine now treats it as a contested warfighting domain.
- Equating tracking with understanding; intent and characterisation are the hard parts.
- Ignoring dependence on commercial and allied systems.
- Forgetting that debris from conflict harms everyone, including the attacker.
- Uncertainty note: altitude bands are conventional, not legal definitions; counterspace
  details here come from open-source assessments that may lag reality.

## Verify
- [ ] You can match LEO, MEO, GEO and HEO to a military use and explain why.
- [ ] You can list the main space mission areas and one historical example of reliance.
- [ ] You can explain SDA and conjunction assessment in plain terms.
- [ ] You can describe what TT&C and station-keeping involve.
- [ ] You can name counterspace categories, the 2007/2021 ASAT tests and the Outer Space
      Treaty's key limits.
