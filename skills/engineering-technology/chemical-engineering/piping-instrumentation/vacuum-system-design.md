---
id: engineering-technology.chemical-engineering.piping-instrumentation.vacuum-system-design
name: vacuum-system-design
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-compressors-and-vacuum, vacuum-system-design, vacuum-system, steam-jet-ejector, liquid-ring-pump]
level: practitioner
status: gated
description: "Size a vacuum system: load from air in-leakage and condensables, choosing ejectors, liquid ring pumps or dry pumps and condensers."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
  - "https://www.heatexchange.org/standards/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vacuum system design

**Goal:** Size a vacuum system: load from air in-leakage and condensables, choosing ejectors, liquid ring pumps or dry pumps and condensers.

## Steps
1. Calculate the load: air in-leakage (estimate from the system volume and the standard in-leakage tables; the HEI publishes "Standards for Steam Jet Vacuum Systems" (7th edition plus addendum) and a liquid ring vacuum pump performance standard, so confirm the table in the current edition) plus non-condensable and condensable vapours.
2. Choose the device by the suction pressure: liquid ring pumps to the tens of mbar, steam ejectors for the lower pressures in multiple stages, dry screw pumps for clean duty (gated: unconfirmed, source is paywalled or blocked).
3. Add condensers between ejector stages to cut the load, and size for the motive steam and cooling water.
4. Check the performance curves at the operating suction pressure and at the cooling water temperature.
5. Consider the environmental effect of the ejector discharge and the seal liquid.

## Gotchas
- In-leakage estimates are uncertain; allow a margin.
- Condensables in the pump can change its performance.

## Verify
- [ ] Pump capacity exceeds the load at the working pressure.
- [ ] Condenser and utility needs are listed.
