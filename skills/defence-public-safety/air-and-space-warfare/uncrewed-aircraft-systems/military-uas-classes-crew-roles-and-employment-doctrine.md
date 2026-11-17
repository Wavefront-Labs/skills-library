---
id: defence-public-safety.air-and-space-warfare.uncrewed-aircraft-systems.military-uas-classes-crew-roles-and-employment-doctrine
name: military-uas-classes-crew-roles-and-employment-doctrine
category: defence-public-safety
field: air-and-space-warfare
product: uncrewed-aircraft-systems
tags: [uncrewed-aircraft-systems, unmanned-aircraft-systems, uas, uav, rpa, remotely-piloted-aircraft, rpas, drones, military-drones, small-uas, suas, nato-uas-classes, class-i, class-ii, class-iii, dod-uas-groups, group-1, group-5, male-uas, hale-uas, rpa-pilot, sensor-operator, mission-intelligence-coordinator, launch-and-recovery-element, mission-control-element, remote-split-operations, isr, persistent-surveillance, full-motion-video, ped, processing-exploitation-dissemination, lost-link, airspace-integration, loitering-munitions, fpv-drones, counter-uas, c-uas, human-judgement, autonomy-in-weapon-systems, dodd-3000-09, loac, nagorno-karabakh-2020, ukraine-drone-war, operator-fatigue, moral-injury, staff-college, air-power-doctrine]
level: practitioner
status: draft
description: "Doctrine-level military drones: NATO classes and US groups, crew roles and split operations, ISR and PED, armed RPA and autonomy policy, small-UAS lessons and counter-UAS."
sources: ["NATO AJP-3.3 and ATP-3.3.7 Guidance for the Training of UAS Operators (public)", "US DoD Unmanned Systems Integrated Roadmap (public editions)", "US DoD Directive 3000.09 Autonomy in Weapon Systems (2012, updated 2023)", "Whittle, Predator: The Secret Origins of the Drone Revolution (2014)", "Kunertova, 'The war in Ukraine shows the game-changing effect of drones', Bulletin of the Atomic Scientists (2023)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Military uncrewed aircraft systems — classes, crews and employment

**Goal:** understand military drones as an equipment class the way doctrine and
staff colleges describe them: how they are categorised, who flies them and how, what
they are used for, and the policy and legal frame. It does not cover building,
modifying or weaponising drones, or specific system performance — that is out of scope.

## 1. It is a *system*, not an aircraft
A UAS is the aircraft **plus** the ground control station, datalinks, launch and recovery
equipment, the crew, and the people who turn its sensor output into intelligence.
Most limits (bandwidth, crews, analysts, airspace) sit outside the airframe.

## 2. How they are categorised
| NATO class (by max take-off mass) | Rough US DoD group | Typical role |
|---|---|---|
| Class I (< 150 kg) — micro, mini, small | Groups 1–3 | Company/battalion-level ISR, hand-launched to catapult |
| Class II (150–600 kg) — tactical | Group 3–4 | Brigade/division ISR |
| Class III (> 600 kg) — MALE/HALE, strike | Groups 4–5 | Theatre ISR, armed overwatch, long endurance |
MALE = medium altitude, long endurance; HALE = high altitude, long endurance. Boundaries
between US groups also use speed and altitude; check the current tables before quoting.

## 3. Crew roles and how they fly
- Larger RPA are flown by a **pilot** with a **sensor operator**, often with a
  **mission intelligence coordinator** — a crewed-aircraft culture of checklists and
  qualification, despite being remote.
- **Remote split operations:** a forward **launch and recovery element** handles take-off
  and landing via line-of-sight link; a distant **mission control element** flies the
  mission via satellite link. This reduces deployed footprint but adds link latency and
  dependence.
- Small UAS are typically flown by soldiers as a secondary duty after short courses.
- **Lost-link procedures** (pre-programmed behaviour if the link fails) and airspace
  deconfliction with crewed aircraft are core planning items.

## 4. Employment
- **ISR is the main mission:** persistence (many hours on station) changes how commanders
  watch an area; the bottleneck is **PED** (processing, exploitation, dissemination) — the
  analysts who watch the video.
- **Armed RPA:** used since 2001 for strikes, governed by the same law of armed conflict
  and targeting process as crewed aircraft (see
  `defence-public-safety.air-and-space-warfare.strike-operations.strategic-bombing-theory-targeting-doctrine-and-interdiction`).
  Public controversy centres on transparency, civilian harm and use outside declared
  conflict zones.
- **Small UAS and loitering munitions:** Nagorno-Karabakh (2020) and Ukraine (from 2022)
  showed cheap drones in very large numbers transforming observation and fire adjustment,
  and driving fast cycles of electronic warfare and counter-drone adaptation.
- **Counter-UAS** has become its own discipline within air defence (see
  `defence-public-safety.air-and-space-warfare.air-and-missile-defence.integrated-air-and-missile-defence-doctrine`).

## 5. Policy, law and people
- **Autonomy:** US DoD Directive 3000.09 requires that autonomous and semi-autonomous weapon
  systems allow "appropriate levels of human judgment over the use of force"; international
  discussion (UN CCW) of lethal autonomous weapons is ongoing and unresolved.
- **Crew welfare:** studies of RPA crews report fatigue from shift work and stress and moral
  injury from prolonged close observation before and after strikes — a real force-management
  issue, not a footnote.

## Gotchas
- Counting airframes instead of crews, links and analysts.
- Assuming drones operate freely: most MALE types are highly vulnerable in defended
  airspace.
- Ignoring the electromagnetic dependence — jamming and spoofing shape small-UAS warfare.
- Treating recent-conflict claims as settled: much public reporting on drone effectiveness is
  unverified or partisan.
- Uncertainty note: the class/group mapping above is approximate; NATO and US schemes use
  different criteria.

## Verify
- [ ] You can explain why a UAS is a system and name its parts.
- [ ] You can place an example drone in a NATO class and rough US group.
- [ ] You can describe pilot, sensor operator and split-operations roles.
- [ ] You can explain why PED, not airframes, often limits ISR.
- [ ] You can summarise the US policy on human judgement in autonomous weapons.
