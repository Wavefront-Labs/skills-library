---
id: engineering-technology.chemical-engineering.process-safety.relief-header-and-flare-sizing
name: relief-header-and-flare-sizing
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-relief-sizing, relief-header-and-flare-sizing, flare-header, relief-header, flare-knockout-drum, flare-stack, api-521, back-pressure, mach-number, thermal-radiation, flare-sizing]
level: advanced
status: verified
description: "Size relief headers, knockout drums and flares from simultaneous relief loads, back-pressure limits, Mach number and thermal radiation criteria per API 521 practice."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relief header and flare sizing

**Goal:** a disposal system that handles the governing contingency without excessive back pressure or radiation. Flare and relief system design is safety-critical and must be carried out and reviewed by qualified engineers using API 521 (or equivalent) and the specific site regulations.

## Design basis
1. **Governing contingency**: the worst credible simultaneous relief from a single cause (power failure, cooling water failure, fire in an area). Do not add unrelated events (double jeopardy) unless the standard or company requires it.
2. **Loads** per device (mass flow, molecular weight, temperature, composition) from the relief sizing; sum by header for the contingency.
3. **Back pressure limits** at each relief device: conventional valves typically limited to about 10% of set pressure (built-up), balanced bellows or pilot valves to higher values per the vendor.

## Header hydraulics
1. Size each header segment for the contingency flow with a compressible-flow method; check Mach number: API 521 gives limits (for example about 0.5 at flare header inlets, higher at tail-pipe outlets and flare tips for emergencies) (gated: unconfirmed, source is paywalled or blocked).
2. Calculate back pressure at each device by tracing from the flare tip back through the network (network software is typical).
3. Check low-temperature effects (autorefrigeration; brittle fracture material limits) and liquid carryover (slope headers to the knockout drum).

## Knockout drum
Size to separate liquid droplets (for example removing droplets above a design size such as 300 to 600 microns, per the standard) (gated: unconfirmed, source is paywalled or blocked), hold the maximum liquid from the contingency for a set time, and keep vapour velocity below the entrainment limit; check the pumps and level instruments.

## Flare stack
- Height from thermal radiation limits at grade and at personnel locations: API 521 gives allowable radiation levels vs exposure time (the order of 1.6 kW/m2 for continuous exposure and about 4.7 kW/m2 for limited-time exposure with shelter) (gated: unconfirmed, source is paywalled or blocked) and solar radiation addition.
- Tip velocity and Mach limits, smokeless operation steam or air assist, flame stability (purge gas), and dispersion of unburned gas or toxic combustion products (ground-level concentration).
- Seal drum or purge reduction to prevent air ingress and flashback.

## Gotchas
- A flare system modified without re-evaluating loads can silently exceed capacity (see MOC).
- Cold-flare releases and liquid flashing change the stack design.

## Verify
- [ ] Network model results (back pressure at each device, Mach number, radiation map) reviewed by an independent relief engineer.
- [ ] Contingency list and basis retained under change control.
