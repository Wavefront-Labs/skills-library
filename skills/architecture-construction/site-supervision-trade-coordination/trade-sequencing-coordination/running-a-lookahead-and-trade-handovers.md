---
id: architecture-construction.site-supervision-trade-coordination.trade-sequencing-coordination.running-a-lookahead-and-trade-handovers
name: running-a-lookahead-and-trade-handovers
category: architecture-construction
field: site-supervision-trade-coordination
product: trade-sequencing-coordination
tags: [site-supervision-trade-coordination, trade-sequencing-coordination, lookahead, three-week-lookahead, short-interval-planning, last-planner, pull-planning, make-ready, constraints, trade-handover, area-handover, clash-resolution, coordination-meeting, sequencing, crew-flow, takt, master-programme, critical-path, foreman, site-manager, trade-stacking]
level: practitioner
status: draft
description: "Keep trades flowing: build a 3-6 week lookahead from the master programme, check constraints, run handovers between trades and resolve clashes before crews arrive."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a lookahead and trade handovers

**Goal:** every crew that turns up has a ready area, the materials, the information and
the access it needs — and leaves the area ready for the next trade.

## 1. From master programme to lookahead
- The master programme (CPM) is too coarse for daily work. Each week, break the next
  **3–6 weeks** into tasks by area and trade: "L2 east — wall framing", "L2 east —
  plumbing rough-in", "L2 east — electrical rough-in", "L2 east — inspection", "L2 east —
  board".
- Note dependencies explicitly (what must be finished, inspected or delivered first).
- Keep it visible: a whiteboard or printed area-by-week grid in the site office beats a
  file nobody opens.

## 2. Make-ready: check constraints
For each task in weeks 2–6, ask (Last Planner System "make-ready" thinking):
- **Information:** drawings current, RFIs answered, submittals approved?
- **Materials:** ordered, lead time inside the window, delivery booked, laydown space?
- **Prior work:** predecessor complete and accepted?
- **Labour and equipment:** crew committed, crane/hoist time booked?
- **Access and permits:** scaffold up, permit-to-work, inspection booked?
- **Space:** no other trade in the same space at the same time (trade stacking kills
  productivity and creates safety risks).
Assign each open constraint an owner and a date. Tasks with unresolved constraints don't
go into next week's plan.

## 3. Weekly coordination meeting
- Foremen of each trade, 30–60 minutes, same time each week.
- Review last week: what was promised vs. done (percent plan complete) and the
  reasons for misses (look for patterns: missing information, late materials,
  prior trade unfinished).
- Commit next week's work: trades commit only to tasks that are ready.
- Record decisions and actions in minutes.

## 4. Handovers between trades
- Define what "complete" means for an area before the next trade enters: e.g., framing
  complete, nogs in for fixtures, straightened studs, area swept, inspection passed.
- **Walk the area with both foremen.** Outgoing trade shows; incoming trade accepts or
  lists what's missing. Record with photos.
- Unfinished work at handover → agree who returns and when, or the incoming trade will
  either wait or work around it (and damage it).

## 5. Clash resolution on site
- Services clashes (duct vs beam vs sprinkler main) found on site: stop, photo, mark the
  drawing, get the affected trades together at the location. Priority usually goes to
  gravity systems (drainage falls), then large ducts, then pressure pipes, then cables —
  a common heuristic, confirm against design intent.
- Anything changing design (penetrations in structure, fire ratings) → RFI to designers.

## 6. Keeping crews productive
- Plan areas so trades can flow in a consistent direction (e.g., floor by floor, zone by
  zone) without leapfrogging.
- Keep a "backlog" of ready work so a crew blocked in one area has somewhere to go.

## Gotchas
- Lookahead copied from the master with no constraint check.
- Trades sharing the same room on the same day.
- Handover by phone call, no walk → disputes over damage.
- Inspection not booked → the next trade idle.

## Verify
- [ ] Lookahead updated this week, 3–6 weeks, by area and trade.
- [ ] Every week-2 task has its constraints cleared or flagged with an owner.
- [ ] Percent-plan-complete tracked and miss reasons recorded.
- [ ] Last handover walked and recorded with photos by both foremen.

*Status: draft — synthesis of Last Planner System and common site practice.*
