---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.post-crash-door-opening-and-egress
name: post-crash-door-opening-and-egress
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [egress, door-opening, post-crash-egress, door-latch, electronic-door-handle, emergency-release, un-r11, fmvss-206, submersion, post-crash]
level: practitioner
status: draft
description: "Design post-crash egress: door latch retention and opening after crash, emergency releases for electronic handles, power-loss behaviour, windows and exits."
sources:
  - "FMVSS 206 (door locks and door retention components) and UN Regulation 11 (door latches and hinges); post-crash door-opening provisions in UN R94 and R95; confirm current texts"
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "https://www.law.cornell.edu/cfr/text/49/571.206"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

Safety-critical, regulated work. This is professional practice guidance: confirm the current regulation, edition and market, and defer sign-off to qualified safety and homologation engineers.

# Post-crash door opening and egress

## 1. Requirement
After a crash, occupants must be able to leave and rescuers must reach them. Door latch and hinge strength (UN R11, FMVSS 206) keep doors closed during impact; crash test regulations also require that doors can be opened after the test (check the wording in the R94/R95 and local procedures for how many doors and what tools may be used). Consumer test protocols also look at it.

## 2. Mechanical design
- **Latch and striker retention:** high strength, designed so inertial loads in lateral impact do not open the latch (inertial lock design); hinges retain the door in crash.
- **Deformation:** structure around door apertures must keep door openable: avoid pinching striker or hinge geometry; check A and B pillar intrusion (see B-pillar design).
- **Handle design:** mechanical inside release always reachable; consider handle direction relative to crash acceleration.
- **Fuel and HV doors:** unrelated release of cap or HV cover must remain functional.

## 3. Electronic door systems
Flush or electrically operated handles and electronic latches add failure modes: loss of 12 V in a crash, damaged wiring, or fire. Design:
- Mechanical emergency release on every door (inside), discoverable and operable by an occupant without power and without instructions, and accessible from outside for responders.
- Power-loss behaviour: unlock on crash signal; keep emergency release independent of the 12 V supply (a backup power or a purely mechanical path).
- Regulatory attention: several markets have been introducing requirements for mechanical door release and for external handles to be operable after power loss; confirm the status in each market.
- Child locks: rear-door child lock must not prevent emergency exit by responders.

## 4. Other exits and glazing
Side glass type (tempered glass that can be broken by tools vs laminated glass that cannot be broken easily), emergency exit labelling on buses (separate regulation), tailgate opening mechanism, roof removal strategy, and seat belt release forces after load.

## 5. Submersion
Electric windows and latches may fail under water; provide an emergency escape method per the owner information, and consider window design with a backup mechanism where required.

## Verify
- [ ] Door opening after crash tests confirmed with documented method.
- [ ] Mechanical release path independent of the 12 V supply.
- [ ] Rescue information describes door and window release.
- [ ] Market regulations for electronic handles confirmed.
