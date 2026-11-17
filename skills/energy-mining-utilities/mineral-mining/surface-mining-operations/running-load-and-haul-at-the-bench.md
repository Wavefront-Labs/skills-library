---
id: energy-mining-utilities.mineral-mining.surface-mining-operations.running-load-and-haul-at-the-bench
name: running-load-and-haul-at-the-bench
category: energy-mining-utilities
field: mineral-mining
product: surface-mining-operations
tags: [surface-mining-operations, open-pit, open-cut, strip-mining, load-and-haul, bench, dig-face, shovel, excavator, haul-truck, truck-spotting, double-side-loading, match-factor, payload, haul-road, windrow, berm, dump, tip-head, stockpile, grade-control, queueing, cycle-time, pit-supervisor]
level: practitioner
status: docs-checked
description: "Run open-pit load-and-haul: bench and dig-face setup, truck spotting and loading, matching fleets, haul road and dump edge care, and the production numbers to watch."
sources:
  - "https://www.ecfr.gov/current/title-30/part-56/section-56.9300"
  - "https://www.ecfr.gov/current/title-30/part-56/section-56.9304"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running load-and-haul at the bench

**Goal:** move the planned tonnes from blasted bench to the right destination (crusher,
stockpile, waste dump) with full payloads, short queues, good roads and no edge
incidents.

> Numbers below are rules of thumb unless a regulation is cited; your mine's
> traffic management plan and OEM limits govern.

## 1. Setting up the dig
- **Know the material boundaries.** Grade control marks ore/waste polygons on the
  ground (pegs, flagging, or in the machine guidance system). Digging across a boundary
  sends ore to the dump or waste to the mill — the most expensive mistake on the bench.
- **Floor at grade.** The loader keeps the floor at design level; a rising floor
  compounds bench after bench and makes the next drill pattern wrong.
- **Face height** suited to the machine: too high and the face overhangs the operator
  (sloughing risk); too low and bucket fill suffers.
- Keep a **safe working area**: berms on open edges, no light vehicles in the loading
  zone without radio contact and permission.

## 2. Spotting and loading trucks
- **Double-side loading** (a truck spotted on each side of the shovel) cuts the
  loader's idle time between trucks; single-side loading is simpler where room is tight.
- Trucks reverse to the spot on the operator's signal (horn or light codes are site
  specific — learn them). The loader bucket never passes over the truck cab.
- Aim for the **target payload** shown on the truck's payload monitor; habitual
  overloading wears tyres, frames and roads, underloading wastes cycles. Follow your OEM's payload policy.
- Place the first bucket gently and centre the load; side-heavy loads spill on the road
  and twist frames.

## 3. Matching the fleet
- **Match factor** ≈ (number of trucks × loader cycle time to fill one truck) ÷
  (number of loaders × truck cycle time). Near 1 is balanced; well under 1 means the
  loader waits for trucks, well over 1 means trucks queue. Dispatch systems do this
  live (see the mine-dispatch-systems skills in this field).
- Watch queue length at the shovel and at the crusher: queues are wasted engine hours.

## 4. Haul roads and dumps
- Roads: keep the grade, crossfall and drainage per design; grade out potholes and
  spillage daily; water to control dust without making the surface slick (wet roads
  on ramps cause slides).
- **Windrows/berms** on open edges where a fall is possible: US 30 CFR 56.9300(b) requires berms or guardrails at least mid-axle height of the largest self-propelled mobile equipment that usually travels the roadway.
- **Dump edges:** tip short of the edge and push over with a dozer, or tip against a
  windrow; never back to an unsupported crest (30 CFR 56.9304(b): where the ground may not support the equipment, dump a safe distance back from the edge of the unstable area). Watch for cracks parallel to the crest,
  which indicate settlement or failure.
- Stockpiles: build in layers by grade where blending matters, and keep a record of
  what went where.

## 5. What to watch each shift
Tonnes per hour per loader, average payload, truck cycle times, queue time,
equipment availability and delay codes. Sudden cycle-time increase usually points at
road condition, a long detour or a crusher bottleneck.

## Gotchas
- Haul trucks have large blind spots; light vehicles must have positive radio contact
  and visible flags/lights before entering.
- Mud on ramps plus braking equals sliding trucks. Stop hauling on a ramp that is
  slick.
- Night shift loses depth perception at dump edges — lighting and windrows matter more.

## Verify
- [ ] Ore/waste boundaries visible and confirmed with grade control before digging.
- [ ] Payloads near target; loading pattern centred.
- [ ] Queue times monitored and fleet reassigned when unbalanced.
- [ ] Edge windrows intact and dumps showing no crest cracks.
- [ ] Roads graded, drained and watered appropriately for the shift.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States, surface metal and nonmetal mines (MSHA, 30 CFR Part 56).

Sources: https://www.ecfr.gov/current/title-30/part-56/section-56.9300; https://www.ecfr.gov/current/title-30/part-56/section-56.9304 (versions: current eCFR and web pages as read on the date above).

Confirmed: 56.9300(b): berms or guardrails at least mid-axle height of the largest self-propelled mobile equipment that usually travels the roadway. 56.9304(b): dump a safe distance back from the edge of unstable ground. Match factor is the standard fleet definition, checked algebraically.

Method: documentation only; no commands were run.
