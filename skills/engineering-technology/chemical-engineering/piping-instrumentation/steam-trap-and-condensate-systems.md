---
id: engineering-technology.chemical-engineering.piping-instrumentation.steam-trap-and-condensate-systems
name: steam-trap-and-condensate-systems
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-layout-and-steam-systems, steam-trap-and-condensate-systems, steam-trap, condensate-system, drip-leg]
level: practitioner
status: gated
description: "Select and install steam traps and condensate return: trap type, sizing, drip legs, and backpressure effects."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
  - "https://www.cooneybrothers.com/userfiles/ad/documents/Spirax_Sarco_72693_Manual.pdf (Spirax Sarco IM-3-2141-US)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Steam trap and condensate systems

**Goal:** Select and install steam traps and condensate return: trap type, sizing, drip legs, and backpressure effects.

## Steps
1. Choose the trap type: thermodynamic or float and thermostatic for different duties; thermostatic traps for tracing; float traps for heat exchangers where continuous drainage is needed.
2. Size by the condensate load times a safety factor (commonly 2 to 3 for process equipment (gated: unconfirmed, source is paywalled or blocked); follow the vendor) at the differential pressure available.
3. Install drip legs at steam main low points, at 30 to 50 m intervals (Spirax Sarco installation instruction IM-3-2141-US shows trap sets at 30-50 m on a 1:100 gradient) and before control valves, with strainers and isolation valves.
4. Design the condensate return for the flash steam and backpressure; do not lift condensate beyond the trap capability.
5. Set a survey programme for trap failures.

## Gotchas
- Failed-open traps waste steam; failed-closed traps cause waterlogging.
- Water hammer needs proper drainage.

## Verify
- [ ] Trap capacity exceeds the load at the working pressure difference.
- [ ] Return line is sized for flash steam.
