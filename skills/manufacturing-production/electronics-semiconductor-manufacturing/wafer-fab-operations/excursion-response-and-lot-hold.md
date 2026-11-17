---
id: manufacturing-production.electronics-semiconductor-manufacturing.wafer-fab-operations.excursion-response-and-lot-hold
name: excursion-response-and-lot-hold
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: wafer-fab-operations
tags: [wafer-fab-operations, wafer-fab, semiconductor, fab, excursion, ooc, out-of-control, oos, spc, control-chart, western-electric-rules, ocap, lot-hold, inhibit, tool-down, mes, workstream, fabguard, secs-gem, fdc, fault-detection, tool-qualification, qual-wafer, monitor-wafer, foup, lot-tracking, containment, disposition, mrb, cleanroom]
level: practitioner
status: draft
description: "Respond to a fab excursion as an operator or technician: follow the OCAP, inhibit the tool, hold affected lots, scope the exposure window, and release only after qual and engineering disposition."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Excursion response and lot hold

**Goal:** when a measurement, FDC alarm or tool event says something is wrong, stop the
damage spreading — fewer wafers processed on a bad tool, every exposed lot found — and
leave a clean record for engineering. In a fab, a few minutes of "let's see if the next
lot is OK" can expose hundreds of wafers worth a lot of money.

## 1. What counts as an excursion
- **SPC out-of-control (OOC)** on a monitored parameter (thickness, CD, overlay, particle
  adders, sheet resistance) — a rule violation on the control chart, even within spec.
- **Out-of-spec (OOS)** product measurement.
- **FDC** (fault detection and classification) alarm on tool sensor traces — RF power,
  pressure, gas flow, endpoint time.
- A tool event: alarm, abort mid-recipe, wafer broken or dropped, PM just completed
  without qual.

## 2. Follow the OCAP — don't improvise
Each monitored parameter has an **OCAP** (out-of-control action plan): a decision tree
the operator follows. Typical skeleton:
1. **Verify the measurement**: re-measure (same metrology tool, then a second tool if
   allowed). Metrology errors are a large share of OOC events.
2. If confirmed: **inhibit the process tool/chamber** in the MES so no more lots can
   be dispatched to it. Do it in the system, not just by a sign on the tool.
3. **Hold** the measured lot.
4. **Scope:** find every lot processed on that tool/chamber since the last good
   measurement (MES lot history by tool, chamber, recipe and time). Hold them all,
   including lots already moved downstream.
5. Notify the owning engineer per the OCAP escalation (pager/chat), with the facts.

## 3. Writing the hold
Hold comments are read later by someone without your context. Include: parameter,
measured value vs limits, tool/chamber, recipe, time window, OCAP step reached, who was
notified. "Hold per eng" tells nobody anything.

## 4. Getting back up
- Engineering or the equipment tech fixes the cause (PM, part swap, recipe/
  chamber seasoning).
- **Qualification run**: monitor/qual wafers through the tool, measured against the
  qual limits. Pass → engineer releases the inhibit. Some tools need several
  conditioning (seasoning) wafers before the qual is meaningful.
- Held product is **dispositioned** by engineering (release, rework, scrap, more
  measurement) — operators don't release held lots on their own judgment.

## 5. Lot-handling hygiene that prevents excursions
- Scan FOUPs/lot carriers at every move-in and move-out; a wrong lot in a tool is
  caught by the MES only if you use it.
- Never bypass a recipe/lot mismatch interlock or SECS/GEM automation error without
  the documented override path.
- Watch queue-time (Q-time) limits between steps (e.g. clean → furnace); expired
  Q-time is itself an excursion in many fabs.
- Report wafer handling events (chipped, slid, broken) immediately; broken-wafer
  debris contaminates following lots.

## Gotchas
- Re-measuring until you get a passing number is not verification; follow the OCAP's
  allowed re-measures.
- A chamber-specific problem on a multi-chamber tool: inhibit the chamber, check if
  other chambers also ran the window.
- Run-to-run (R2R) control can mask drift by adjusting recipes; an R2R correction
  hitting its limit is an early warning.

## Verify
- [ ] Tool/chamber inhibited in the MES before more lots ran.
- [ ] Exposure window scoped from the last good measurement; all lots held.
- [ ] Hold comments contain value, limits, tool, window and notifications.
- [ ] Release only after qual pass and engineering disposition.

*Draft: names (OCAP, FDC, inhibit) and escalation flow vary by fab and MES (e.g.
Applied SmartFactory, Camstar/Opcenter); confirm locally.*
