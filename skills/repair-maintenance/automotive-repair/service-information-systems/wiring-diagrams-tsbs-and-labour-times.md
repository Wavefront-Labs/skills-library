---
id: repair-maintenance.automotive-repair.service-information-systems.wiring-diagrams-tsbs-and-labour-times
name: wiring-diagrams-tsbs-and-labour-times
category: repair-maintenance
field: automotive-repair
product: service-information-systems
tags: [automotive-repair, service-information-systems, alldata, mitchell-1, prodemand, identifix, oem-portal, techinfo, service-manual, wiring-diagram, connector-views, component-locator, tsb, technical-service-bulletin, recall, labour-times, labor-guide, flat-rate, torque-specs, vin-lookup, nastf, right-to-repair, repair-procedure, estimate]
level: practitioner
status: draft
description: "Get the right answer from ALLDATA, Mitchell 1 ProDemand or OEM portals: VIN-exact lookup, TSBs and recalls first, reading wiring diagrams and connector views, torque specs and labour-time estimates."
sources: ["ALLDATA and Mitchell 1 ProDemand product documentation (features overview)", "NASTF (National Automotive Service Task Force) OEM service information directory", "Massachusetts/right-to-repair MOU context"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wiring diagrams, TSBs and labour times

**Goal:** turn a vehicle and a symptom into the exact procedure, specification and price
you need — quickly — from a service information system (SIS). Guessing a torque spec or
a wire colour from a forum is how jobs come back.

## 1. Pick the source
- **Aftermarket aggregators:** ALLDATA Repair, Mitchell 1 ProDemand (adds real-world fixes
  "SureTrack"), Identifix Direct-Hit (crowd-sourced confirmed fixes), Haynes Pro/Autodata in
  Europe. Subscription per shop; broad coverage, consistent layout.
- **OEM portals** (e.g. Ford's Motorcraft Service, GM's ACDelco TDS, Toyota TIS,
  BMW AOS/ISTA-related portals, Mercedes XENTRY/WIS): most complete and current, include
  module programming. Short-term subscriptions (day/week) exist; the NASTF website lists
  each OEM's portal. In the US, OEMs make this available under right-to-repair commitments.
- Use the OEM source for programming, recent models, and anything the aggregator
  doesn't have or shows as "refer to manufacturer".

## 2. Always start with the VIN
- Enter or scan the **17-character VIN**: it decodes the exact engine, transmission,
  build date and options. Mid-year changes are common — a 2015 model may have two different
  sensor designs.
- Check **recalls and campaigns** (free on the manufacturer's site / NHTSA in the US) —
  recall work is done by dealers at no cost to the owner.

## 3. TSBs before diagnosis
- **Technical Service Bulletins** document known problems and the manufacturer's fix
  (updated software, revised part, new procedure). Search by symptom, DTC and system.
- A TSB applies only if VIN/build-date range and symptoms match. Read the whole bulletin:
  the fix may be a reflash, not the part everyone replaces.

## 4. Reading wiring diagrams
1. Find the system diagram (e.g. "Engine Performance → Fuel Injectors"). Most systems use
   power at the top, ground at the bottom.
2. Identify: fuse and its rating/location, relay, connectors (C-numbers, e.g. C101 pin 12),
   splices (S-numbers), grounds (G-numbers with location), wire colour codes
   (e.g. "BK/WH" = black with white stripe; abbreviations vary by OEM — check the legend).
3. Use the **connector end views** to find the right pin — note whether the view is
   from the terminal side or the wire (harness) side; this trips everyone up once.
4. **Component locator** and **ground locations** pages show where things physically are.
5. Use the **power distribution** and **ground distribution** diagrams when several
   circuits fail together: they often share one fuse or ground.
6. Print or screenshot the circuit and mark measurements on it as you go.

## 5. Specs and procedures
- Torque specs (with **torque-to-yield** angles — those bolts are usually one-time-use),
  fluid capacities and specifications, service intervals, relearn procedures (throttle,
  steering angle, TPMS, battery registration).
- Read the procedure's warnings/notes block first (special tools, "replace bolt", "do not
  reuse gasket").

## 6. Labour times and estimating
- Labour guides give **warranty** (OEM) and **retail/flat-rate** times per operation, plus
  "additional" times (e.g. "+0.3 h with AC") and **overlap** (when two jobs share
  disassembly, e.g. water pump with timing belt, you shouldn't charge both fully).
- Estimate = labour hours × shop rate + parts (with your markup) + fluids/shop supplies +
  diagnosis time.
- Note flagged "rust/seized fastener" risk and add contingency in the estimate wording.

## Gotchas
- Wrong engine code in the lookup → wrong torque spec, wrong timing procedure.
- Aftermarket diagrams sometimes redraw OEM schematics with errors; confirm with the OEM
  diagram for critical circuits.
- Uncertain: portal names and pricing change frequently; check the NASTF listing for current links.

## Verify
- [ ] Vehicle identified by VIN; recalls and TSBs checked before diagnosis.
- [ ] Wiring diagram, connector view orientation and component location confirmed.
- [ ] Torque specs and one-time-use fasteners noted from the procedure.
- [ ] Estimate uses the guide time with overlap applied and contingencies stated.
