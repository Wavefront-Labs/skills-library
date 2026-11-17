---
id: repair-maintenance.facilities-maintenance.cmms-software.cmms-work-order-pm-and-backlog-management
name: cmms-work-order-pm-and-backlog-management
category: repair-maintenance
field: facilities-maintenance
product: cmms-software
tags: [cmms-software, cmms, eam, maximo, ibm-maximo, fiix, upkeep, limble, mpulse, planon, work-order, work-request, asset-register, asset-hierarchy, pm-schedule, preventive-maintenance, meter-based-pm, failure-codes, backlog, kpi, pm-compliance, mttr, wrench-time, maintenance-reporting, helpdesk, facilities-management]
level: practitioner
status: draft
description: "Run facility maintenance in a CMMS (Maximo, Fiix, UpKeep, Limble): clean asset register, work order lifecycle, PM schedule setup, failure codes, backlog and KPI reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running maintenance through a CMMS

**Goal:** a CMMS whose data you can trust — every asset findable, every job a work order
with a status that means something, PMs that generate on time, and reports that show
backlog and compliance honestly. The software matters less than the discipline; the
steps below apply to Maximo, Fiix, UpKeep, Limble and similar tools.

## 1. Asset register before anything else
1. Build a **location hierarchy** first: site > building > floor > room/plant room.
   Assets hang off locations, so a moved asset changes location, not identity.
2. Give each maintainable asset a unique, permanent ID and a physical label (QR or
   barcode sticker). Use a naming convention such as `BLD1-L2-AHU-01`; do not encode
   things that change (owner, contractor) in the ID.
3. Minimum fields: asset class/type, make, model, serial, install date, location,
   criticality (e.g. 1–3 or A/B/C), warranty end, and a parent asset where relevant
   (a pump under its booster set).
4. Decide the cut-off: assets worth tracking individually (plant, fire doors, lifts,
   emergency lights) versus "run to failure" items logged against a location
   (light switches, coat hooks).
5. Audit 10% of records against the building each quarter; duplicates and ghost
   assets breed fast after refurbishments.

## 2. A work order lifecycle with meaning
Typical statuses: **Request > Approved > Planned/Scheduled > In progress > Waiting
(parts/contractor/access) > Complete > Closed**. Rules that keep it honest:
- One fault = one WO. Don't append new faults to an open job.
- Mandatory at close: labour hours, parts used, a **problem/cause/remedy failure
  code**, and a free-text note a stranger could understand ("replaced cartridge,
  35 mm ceramic, tap now drip-free"), not "done".
- Priority by a fixed matrix (safety/legal > business critical > comfort > cosmetic)
  with target response and completion times, e.g. P1 respond in 1 h, P4 within 20
  working days. (Draft note: targets are illustrative; set them in the service-level
  agreement for your site.)
- "Waiting" must carry a reason code; otherwise it hides backlog.
- Supervisors review completed WOs before closing — closure is a quality gate.

## 3. Setting up PM schedules
1. Create a **PM template** (job plan) per asset type: task steps, estimated hours,
   craft, tools, parts kit, safety notes (isolation points, permits).
2. Choose the trigger: **calendar** (every 3 months), **meter** (every 2,000 run
   hours), or both, whichever comes first.
3. Choose **fixed** scheduling (next due from the original due date — use for
   statutory tests) or **floating** (next due from completion — fine for lubrication
   and cleaning).
4. Set the lead time so the WO generates early enough to plan, typically 7–14 days
   ahead for monthly PMs. Stagger due dates so 40 filter changes don't land the same
   Monday.
5. Attach the PM to assets, not locations, so history follows the asset.
See repair-maintenance.facilities-maintenance.preventive-maintenance-planning for
deciding which tasks and frequencies to load.

## 4. Backlog and KPIs that management will read
- **Backlog (weeks)** = open planned labour hours / weekly available labour hours.
  Healthy is roughly 2–4 weeks; under 2 suggests idle capacity, over 6 means you are
  falling behind. (Draft note: a common rule of thumb, not a standard.)
- **PM compliance** = PMs completed within their window / PMs due. Define the window
  (e.g. ±10% of interval) and stick to it; target ≥ 90%.
- **Planned vs reactive ratio** — aim to drift towards 70–80% planned hours.
- **MTTR / MTBF** per critical asset class, from WO timestamps and failure codes.
- Age profile of open WOs (0–30, 31–90, >90 days) is the quickest health check.
Schedule these as saved reports or dashboards and review them weekly, not quarterly.

## Gotchas
- Garbage in: if techs close jobs from a phone with no codes, KPIs are fiction. Make
  fields mandatory and keep the code list short (20–40 codes, not 300).
- Never delete assets that have history; set them inactive/decommissioned.
- Importing a spreadsheet register: dedupe and normalise make/model spelling first.
- Mobile apps cache offline; sync before reporting, or yesterday's work looks missing.
- Field names and status sets differ by product and licence tier; map your workflow
  to the tool, not the reverse. (Draft note: menu paths vary by version — check the
  vendor docs for your edition.)

## Verify
- [ ] Any asset can be found by scanning its label or searching its ID.
- [ ] Every closed WO this week has hours, parts, a failure code and a readable note.
- [ ] PMs generate on schedule with lead time; statutory PMs use fixed scheduling.
- [ ] Waiting WOs all have reason codes.
- [ ] Backlog weeks, PM compliance and WO age profile are reported weekly.
