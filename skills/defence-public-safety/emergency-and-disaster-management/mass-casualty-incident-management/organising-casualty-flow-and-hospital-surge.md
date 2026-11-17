---
id: defence-public-safety.emergency-and-disaster-management.mass-casualty-incident-management.organising-casualty-flow-and-hospital-surge
name: organising-casualty-flow-and-hospital-surge
category: defence-public-safety
field: emergency-and-disaster-management
product: mass-casualty-incident-management
tags: [mass-casualty-incident-management, mci, major-incident, mass-casualty, mascal, triage-organisation, start-triage, salt-triage, triage-sieve, triage-sort, casualty-clearing-station, casualty-collection-point, treatment-area, transport-officer, ambulance-loading-point, casualty-distribution, hospital-surge, hics, major-incident-declaration, methane, ethane, mist-handover, patient-tracking, triage-tags, hospital-capacity, reverse-triage, casualty-bureau, family-reunification, medical-branch, jesip]
level: practitioner
status: docs-checked
description: "Organise a mass-casualty incident: declare early with METHANE, set up triage, treatment and transport areas, distribute casualties across hospitals, track patients and trigger hospital surge."
sources: ["https://www.jesip.org.uk/joint-doctrine/m-ethane/", "https://asprtracie.hhs.gov/technical-resources/resource/4049/salt-mass-casualty-triage-on-line-training", "https://chemm.hhs.gov/incident-primer/triage/start-triage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organising casualty flow and hospital surge

**Goal:** when casualties outnumber the immediately available care, do the most good for
the most people: spread casualties across the system instead of flooding the nearest
hospital, keep track of every patient, and switch hospitals into surge mode early. The
individual triage algorithm is covered in
`health-medicine.emergency-medical-services-and-first-aid.scene-management-and-mass-casualty-triage.start-triage-at-mass-casualty-incidents`;
this skill is the system around it.

## 1. Declare early, report in a fixed format
- The first senior clinician/crew on scene **declares a major incident** (or "major
  incident standby") as soon as it is plausible — standing down an over-call is cheap;
  a late declaration is not.
- Send a **METHANE** report (UK/JESIP; also widely used elsewhere):
  **M**ajor incident declared · **E**xact location · **T**ype of incident ·
  **H**azards present/potential · **A**ccess and egress routes · **N**umber and severity of
  casualties (estimate) · **E**mergency services present and required.
- Repeat METHANE as the picture changes; dispatch alerts hospitals from it.

## 2. Lay out the scene
Command assigns medical roles (titles vary: medical branch/group supervisor, ambulance
commander, triage, treatment, transport officers).
- **Triage at the point of contact** with a simple sieve (START or SALT) — tag colour/category, minimal life-saving interventions only
  (catastrophic bleeding control, airway positioning). Walking wounded are directed
  to a collection point, not left behind.
- **Casualty clearing station / treatment area** upwind, uphill, out of the hazard,
  with separate zones by priority (immediate/P1, urgent/P2, delayed/P3, expectant if
  your system uses it). A second, more detailed **triage sort** happens here.
- **Ambulance loading point** with a one-way circuit: ambulance parking → loading →
  exit. A **transport officer** controls which patient goes where.
- Separate areas for the **deceased** (left in place where possible for investigation)
  and for uninjured survivors (they're witnesses and need welfare and registration).

## 3. Distribute casualties
- The transport officer (with ambulance control) allocates by **hospital capability and
  current capacity**, not proximity: the nearest hospital gets swamped first by self-presenters.
- Send the most critical to the **major trauma centre/trauma level I**; spread P2 and
  P3 to units further away. Use a pre-agreed **casualty distribution plan** with
  initial numbers per hospital, updated by real-time capacity calls.
- Hand over with a structured format (e.g. ATMIST/MIST) and keep patient numbers on tags.

## 4. Hospital surge
- Hospitals activate their major-incident plan (in the US often HICS): command centre,
  ED reorganised, **reverse triage** (early discharge of stable inpatients, cancel elective
  surgery), open surge beds, call in staff by a cascade, secure the site and control
  entrances.
- Prepare for decontamination if CBRN is possible — contaminated self-presenters
  arrive before ambulances.
- Blood bank, theatres, ICU and imaging are bottlenecks; count them first.

## 5. Patient tracking and families
- Every casualty has a unique number from the triage tag, carried through to the
  hospital record. Ambulance control logs destination for each.
- Feed data to the **casualty bureau** (police) or family assistance centre; designate a
  family reception area at hospitals and a single public helpline. Families arriving at
  the scene need somewhere to go that is not the scene.

## Gotchas
- Over-triage (too many P1s) clogs the trauma centre; under-triage kills. Re-triage at each step.
- Ambulances self-deploying to the scene without staging create gridlock — route via a
  rendezvous point.
- Clinicians drawn into treating one patient lose the overview — commanders don't treat.
- Radio and phone networks overload; agree a backup communication method beforehand.

## Verify
- [ ] Major incident declared and METHANE sent and updated.
- [ ] Triage, treatment and loading areas set up with one-way vehicle flow.
- [ ] Casualties distributed by capability/capacity, not proximity alone.
- [ ] Every patient has a tag number traceable to a destination.
- [ ] Hospitals notified early and surge measures (reverse triage, staff call-in) triggered.

## Checked

Checked 2026-10-25. Jurisdiction: UK (JESIP METHANE) with US terms (START, SALT, HICS) noted. Source versions: JESIP M/ETHANE pages and aide-memoires (2022 v5.1, 2024 v6); ASPR TRACIE and CHEMM triage pages. Confirmed: the METHANE elements (major incident declared, exact location, type, hazards, access, number of casualties, emergency services) and that the first responders send it; START and SALT exist as US sieve methods. Removed the UK Ten Second Triage mention and an unconfirmed claim that self-presenters can be half or more of arrivals at the nearest hospital. Triage algorithms are not restated here.

Method: documentation only; no commands were run.
