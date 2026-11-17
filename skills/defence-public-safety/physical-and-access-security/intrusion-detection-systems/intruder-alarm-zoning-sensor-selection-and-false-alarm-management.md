---
id: defence-public-safety.physical-and-access-security.intrusion-detection-systems.intruder-alarm-zoning-sensor-selection-and-false-alarm-management
name: intruder-alarm-zoning-sensor-selection-and-false-alarm-management
category: defence-public-safety
field: physical-and-access-security
product: intrusion-detection-systems
tags: [physical-and-access-security, intrusion-detection-systems, ids, intruder-alarm, burglar-alarm, alarm-panel, pir, dual-technology-detector, door-contacts, magnetic-contacts, glass-break-detector, shock-sensor, beam-detector, perimeter-intrusion-detection, pids, zoning, partitions, en-50131, pd-6662, ul-681, ul-2050, alarm-receiving-centre, arc, central-station, dual-path-signalling, sequential-confirmation, video-verification, false-alarms, police-response-policy, keyholder]
level: practitioner
status: draft
description: "Designing and running intruder alarm systems: sensor selection (PIR, dual-tech, contacts, glass-break), zoning, grading (EN 50131), signalling and confirmation, and cutting false alarms."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intruder alarm zoning, sensor selection and false-alarm management

**Goal:** detect real intrusions early enough to respond, without the false alarms
that teach everyone to ignore the system or get police response withdrawn. Reference
for security managers and installers; local standards and police policy decide what
qualifies for response.

## 1. Grading and standards
- **Europe/UK:** **EN 50131** series grades systems 1–4 by risk (Grade 2 typical
  domestic/low commercial, Grade 3 for most commercial, Grade 4 high-risk). In the UK,
  **PD 6662** applies it, and police response requires a compliant system installed by
  a certified company (NSI or SSAIB) under the NPCC policy.
- **US:** UL 681 (installation), UL 2050 (national industrial security), with
  central-station certificates; local ordinances on alarm permits and false-alarm fines.
(Check current versions and local requirements.)

## 2. Sensor selection
- **Door/window contacts** (magnetic): perimeter detection at the point of entry;
  surface or recessed, grade-appropriate (high-security contacts resist magnetic defeat).
- **PIR** (passive infrared) volumetric detectors: detect body heat moving across zones.
  Poor near heaters, air vents, direct sunlight, and where pets roam (use pet-tolerant
  models carefully).
- **Dual-technology** (PIR + microwave) reduce false alarms in difficult environments.
- **Glass-break** (acoustic or shock) for large glazed areas.
- **Perimeter (PIDS):** fence-mounted, buried, beam or radar for outdoor sites —
  environment (wind, animals, vegetation) dominates false-alarm rates.
- **Anti-masking** on detectors in higher grades (detects someone covering the sensor).
Layer them: perimeter, then space, then specific targets.

## 3. Zoning and partitions
- One zone per detector (or small logical group) so an alarm tells responders exactly
  where. Name zones in plain language.
- **Entry/exit route** zones with entry delay; others instant.
- **Partitions/areas** let parts of a building be set independently; make sure
  shared routes are handled.
- **Tamper** circuits, battery standby and supervised signalling at the grade's level.

## 4. Signalling and confirmation
- Signal to an **alarm receiving centre (ARC)/central station** over **dual-path**
  (e.g. IP + cellular) with line-fault monitoring.
- **Confirmation:** UK practice uses *sequential confirmation* (two separate detectors
  within a time window), audio or **video verification** before police response is
  requested. US central stations commonly use enhanced call verification (calling at
  least two keyholders before dispatch) where local rules require it.
- Keyholder lists and response instructions kept current.

## 5. False-alarm management
- Most false alarms are **user error** (wrong code, wrong exit route) — training and
  simple setting procedures help most.
- Log every alarm with cause; look for repeat zones (a draughty PIR, a loose door).
- Maintenance visits at the frequency the standard requires (often twice a year for
  monitored systems — check), with walk-tests of every detector.
- Police may withdraw response after a set number of false alarms in a period; know
  the threshold and restoration process locally.

## Gotchas
- Detectors installed facing windows or heaters.
- Seasonal effects: spiders, insects, heating switched on.
- Wireless detectors' batteries — monitor supervision faults.

## Verify
- [ ] Grade chosen from a risk assessment; installer certified as required.
- [ ] Each zone named and mapped; walk-test passes on every detector.
- [ ] Dual-path signalling and confirmation configured.
- [ ] False-alarm log reviewed monthly with causes fixed.
