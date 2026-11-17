---
id: computing-software.digital-forensics-incident-response.evidence-handling.evidence-labeling-bagging-and-seizure-photography
name: evidence-labeling-bagging-and-seizure-photography
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-labeling, evidence-seizure, chain-of-custody, photography, iso-27037, dfir]
level: practitioner
status: draft
description: "Label, bag and photograph physical digital evidence at seizure: scene photography, labels, anti-static and Faraday bags, seals, and cable/port documentation."
sources: ["https://www.iso.org/standard/44381.html", "https://www.swgde.org/documents/published-complete-listing/", "https://www.ojp.gov/pdffiles1/nij/219941.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Evidence labeling, bagging and seizure photography

**Goal:** physical items are unambiguously identified, protected from damage and tampering,
and the scene is documented as found (ISO/IEC 27037; NIJ Electronic Crime Scene
Investigation guide; SWGDE).

## Photograph before touching
- Wide shots of the room, then the device in place, then close-ups: screen content (if on),
  cables and ports (label each cable end), serial number labels, damage.
- Include a scale and an evidence ID placard in close-ups. Record photo numbers in notes.
- Photograph the screen of a running system before any action.

## Label
Each item and each removable part (drive removed from laptop gets its own sub-ID, e.g.
EVID-004-A). Label content: case number, evidence ID, description, serial, date/time,
collector initials. Labels on the bag and, where possible, on the item itself (not over
ports or serial plates).

## Bag
- Anti-static bags for drives and boards; padded containers for laptops.
- **Faraday bags** for phones and wireless devices (and keep them powered if needed, see
  the mobile isolation skill).
- Seal with tamper-evident tape, signature and date across the seal.
- Never use plastic bags for electronics that are wet; use paper and dry them.

## Transport and storage
Avoid heat, magnets, and radio transmitters; keep upright; log in the evidence store on
arrival with seal intact check.

## Verify
Another examiner can match every bag to its photo, label, evidence log entry and chain of
custody form without asking you.
