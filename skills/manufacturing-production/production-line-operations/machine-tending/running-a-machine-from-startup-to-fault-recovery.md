---
id: manufacturing-production.production-line-operations.machine-tending.running-a-machine-from-startup-to-fault-recovery
name: running-a-machine-from-startup-to-fault-recovery
category: manufacturing-production
field: production-line-operations
product: machine-tending
tags: [machine-tending, production-line-operations, machine-operator, machine-minding, startup-sequence, shutdown-sequence, pre-start-checks, jam-clearing, fault-clearing, loto, lockout-tagout, isolation, e-stop, guarding, interlocks, hmi, alarm-response, cycle-monitoring, first-off, escalation, shift-handover, operator-safety]
level: intro
status: draft
description: "Run a production machine safely through a shift: pre-start checks, startup and shutdown order, cycle watching, safe jam clearing under isolation, reading HMI alarms and when to escalate."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a machine from startup to fault recovery

**Goal:** bring a production machine (press, filler, moulder, CNC cell, wrapper) up
cleanly, keep it making good parts, and recover from stops without injuring yourself
or the machine. The specifics live in that machine's own SOP; this is the method that
sits under every SOP. Where the site procedure says something different, the site
procedure wins.

## 1. Pre-start checks (before you press anything)
- **Read the handover.** What stopped last shift, what is still open, any temporary
  fixes ("sensor taped over" is a red flag — escalate, do not run).
- **Walk round it.** Guards closed and fixed, no tools or rags inside, no leaks or
  puddles, air and power available (gauge in the green band on the regulator).
- **Check materials and order.** Right part/material/label for the order on the
  HMI or traveller; batch number recorded if traceability needs it.
- **Test the stops.** Many sites require an e-stop or guard-interlock function check at
  shift start; if a guard opens and the machine still runs, it is out of service.

## 2. Startup order
Typical sequence (confirm against the SOP): reset e-stops → reset safety relay
(blue/reset button) → acknowledge alarms on the HMI → home/reference the axes → run
in **manual or jog** one cycle → check the first part → switch to **auto**.
Bring heat-dependent machines (moulders, sealers, glue units) to temperature first and
let them **soak** — the display hitting setpoint is not the same as the tooling being
at temperature. Running early gives short shots, weak seals, cold glue.

## 3. Watching it run
- Know the **normal cycle time** and sound. A cycle that has crept up 10% or a new
  knock is an early warning; note it before it becomes a stop.
- Check parts on the frequency the control plan sets, plus every restart and every
  material change.
- Keep infeed full and outfeed clear: starving or blocking the machine is the
  operator's commonest self-inflicted downtime.
- Log every stop over the site threshold (often 1–5 min) with a reason, not "jam".

## 4. Clearing a jam or fault — the safe way
1. **Stop it properly** (cycle stop, then stop). Never reach past a guard into a
   machine that is merely paused or waiting for a sensor: sensors trigger motion.
2. **Decide if isolation is needed.** Anything inside the guarding, or with stored
   energy (air, hydraulics, springs, gravity, heat), needs **lockout/tagout**: isolate
   at the point marked, lock with *your* lock, bleed down air/hydraulics, **try to
   start** to prove dead. Some quick-clear tasks are covered by a validated
   "minor servicing" procedure with guard-interlock only — use that only where the
   site has written it down.
3. **Clear, then find out why.** Bent product, wrong material, mis-set guide, worn
   part? Clearing without a cause guarantees a repeat.
4. **Count back.** Product near the jam may be damaged or out of sequence — quarantine
   it per the site rule.
5. Remove your lock, guards closed, reset, one jog cycle, check the part, back to auto.

## 5. Reading alarms and escalating
- Read the **full alarm text and number** and note it. Acknowledging without reading
  destroys the evidence.
- Operator-level: material out, door open, jam, low air — fix and reset.
- **Escalate** (team leader, maintenance) when: the same alarm repeats (rule of thumb:
  3 times in an hour), a safety device or interlock faults, you need to go beyond the
  operator access level, you smell burning, or anything is leaking. Give machine,
  alarm number, what you saw, what you did.
- Never bypass, bridge or tape a sensor or interlock to "keep it going".

## 6. Shutdown
Finish or purge the cycle, run out the product, stop in the documented order
(heaters may need to stay on or be purged — e.g. moulding barrels with heat-sensitive
material), clean to the standard, record counts and handover notes.

## Verify
- [ ] You can name every energy source on your machine and where it is isolated.
- [ ] First part after every start, restart and material change was checked.
- [ ] Every stop has a logged reason and every repeat alarm was escalated.
- [ ] Handover note lists open issues, temporary fixes and counts.

*Uncertain: shift-start safety-function tests and "minor servicing" exemptions vary by
jurisdiction and site — confirm the rule locally.*
