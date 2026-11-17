---
id: defence-public-safety.policing-and-patrol.dispatch-and-cad-systems.call-taking-cad-incident-entry-and-radio-procedure
name: call-taking-cad-incident-entry-and-radio-procedure
category: defence-public-safety
field: policing-and-patrol
product: dispatch-and-cad-systems
tags: [policing-and-patrol, dispatch-and-cad-systems, cad, computer-aided-dispatch, 911, 999, 112, psap, call-taking, dispatcher, telecommunicator, ani-ali, wireless-location, rapidsos, priority-codes, incident-types, unit-status, avl, radio-procedure, plain-language, ten-codes, nato-phonetic-alphabet, officer-safety, apco, nena]
level: practitioner
status: draft
description: "Emergency call-taking and dispatch on a CAD: verify location first, the core interrogation, coding priority, entering and updating incidents, unit status and clear radio procedure."
sources: ["APCO / NENA call-taking standards (public summaries)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Call-taking, CAD incident entry and radio procedure

**Goal:** turn a frightened caller into a correctly located, correctly prioritised incident in
the CAD within seconds, get the right units moving, and keep everyone informed over the
radio. Vendors differ (Hexagon/Intergraph, Motorola PremierOne/Spillman, Tyler, CentralSquare,
Mark43 and others) but the workflow is the same.

## 1. Location first, always
Ask "What is the address of your emergency?" before anything else. If the line drops you can
still send help to a location; you can't send it to a description.
- Compare the caller's address with **ANI/ALI** (landline) or the wireless location
  (Phase II coordinates, device-based hybrid location such as RapidSOS in the US/AML in
  Europe). Wireless Phase I only gives the tower sector — never dispatch to it as if it were
  the incident.
- Verify: repeat it back, get a cross-street or landmark, apartment/floor, and which side of
  a divided road. Watch for same street names in neighbouring towns — CAD geo-validation may
  pick the wrong one.
- Get a **callback number** next.

## 2. The core interrogation
- What happened? (In the caller's words — then classify.)
- Is anyone hurt? Are weapons involved or mentioned?
- Is it happening now? When did it happen?
- Who is involved — descriptions (top to bottom: sex, race/ethnicity as described, age,
  height, build, clothing head-to-toe), vehicle (colour, make, model, plate, direction of travel).
- Caller's safety: are they in danger? Can they stay on the line?
Medical calls follow a structured protocol (e.g. MPDS, APCO) and pre-arrival instructions —
see health-medicine.emergency-medical-services-and-first-aid.emergency-medical-dispatch.telephone-cpr-coaching.

## 3. Entering the incident
- Choose the incident type and priority from the agency's response plan; the type drives the
  CAD's unit recommendations. Wrong type = wrong units.
- Put officer-safety information where the dispatcher and responding units will see it
  (premise hazards, weapons, prior violence flags) — not buried in narrative.
- Update the narrative live; time-stamped comments are the legal record of what was known when.
- Check for duplicate incidents (several callers about the same crash) and link them instead
  of dispatching twice.

## 4. Dispatching and tracking units
- Use the CAD recommendation, then check it against reality (AVL positions, units tied up).
- Keep **unit status** accurate: dispatched, en route, on scene, transporting, available.
  Status timers (e.g. officer welfare check after a set time on scene) only work if statuses are right.
- Escalate per plan: supervisor notification, mutual aid, specialised units.

## 5. Radio procedure
- Structure: who you're calling, who you are, message. Wait for acknowledgement.
- **Plain language** is the US NIMS recommendation for multi-agency incidents; ten-codes vary
  between agencies and cause confusion at shared scenes.
- Spell with the NATO phonetic alphabet (Alpha, Bravo, Charlie...); give numbers digit by digit.
- Emergency traffic: clear the channel, give the emergency unit priority, and use alert tones
  per policy. When an officer calls for help, location is the first thing to confirm.
- Keep transmissions short; release the key between thoughts so others can break in.

## Gotchas
- Callers often give where they *are*, not where the incident *is*. Ask both.
- "Shots fired" with no other detail still gets the highest priority until downgraded by facts.
- Copy-forwarding prior narratives into a new incident carries stale information.
- CAD map layers can be out of date in new developments; keep a local note list.

## Verify
- [ ] Location verified two ways and callback number captured before anything else.
- [ ] Incident type and priority match the response plan.
- [ ] Safety flags visible in the incident, not only in narrative.
- [ ] Every unit's status accurate at the end of the incident.

*Uncertainty:* protocol names and location-service features differ by country and vendor;
check your PSAP's SOPs.
