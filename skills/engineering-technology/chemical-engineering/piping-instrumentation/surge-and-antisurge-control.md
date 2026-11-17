---
id: engineering-technology.chemical-engineering.piping-instrumentation.surge-and-antisurge-control
name: surge-and-antisurge-control
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-compressors-and-vacuum, surge-and-antisurge-control, compressor-surge, antisurge-control, recycle-valve]
level: practitioner
status: gated
description: "Protect centrifugal compressors from surge: surge line, control margin, recycle valve sizing and fast control response."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surge and antisurge control

**Goal:** Protect centrifugal compressors from surge: surge line, control margin, recycle valve sizing and fast control response.

## Steps
1. Obtain the surge limit line from the vendor curves; set the surge control line with a margin (commonly around 10 percent in flow (gated: unconfirmed, source is paywalled or blocked); confirm with the vendor).
2. Use a dedicated antisurge controller with fast scan, measuring flow and the head proxy, and opening a recycle or blow-off valve when the operating point approaches the control line.
3. Size the recycle valve for the flow needed to stay on the right of the surge line at the worst case; include the trip case and the cooler in the recycle path.
4. Choose a fast-acting valve and a short recycle line to reduce the volume (the surge response depends on the volume).
5. Test the system at commissioning.

## Gotchas
- Surge can damage the machine within seconds.
- Hot recycle needs cooling or limits.

## Verify
- [ ] Recycle valve capacity covers the trip case.
- [ ] Controller margins are tested.
