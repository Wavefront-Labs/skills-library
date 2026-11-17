---
id: manufacturing-production.chemical-process-manufacturing.process-safety-operations.operating-limits-permits-isolation-and-moc
name: operating-limits-permits-isolation-and-moc
category: manufacturing-production
field: chemical-process-manufacturing
product: process-safety-operations
tags: [process-safety-operations, process-safety, psm, safe-operating-limits, sol, integrity-operating-window, iow, permit-to-work, ptw, isolation, positive-isolation, double-block-and-bleed, blinding, spading, lockout-tagout, loto, energy-isolation, management-of-change, moc, temporary-change, hazop, hazop-actions, safety-instrumented-system, sis, bypass, override, line-break, normalisation-of-deviance, chemical-plant]
level: practitioner
status: draft
description: "Operate inside the process safety envelope: respect safe operating limits, prepare and verify isolations for permit-to-work, recognise a change that needs MOC, and close out HAZOP actions."
sources: ["UK HSE HSG253 safe isolation of plant and equipment (general reference)", "CCPS Guidelines for Risk Based Process Safety (general reference)", "US OSHA 29 CFR 1910.119 PSM (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process safety in operations: limits, permits, isolation and MOC

**Goal:** make the everyday operational decisions that keep the plant inside its
designed safety envelope — the ones where most major accidents actually begin.

*This is an orientation to good practice, not a substitute for your site's
procedures, training and authorisations, which always take precedence.*

## 1. Safe operating limits
- **Safe operating limits (SOLs)** — the boundaries beyond which the design cannot
  guarantee safety (max pressure, temperature, level, composition). Exceeding one
  requires a defined action, usually going to a safe state, and is reported.
- **Integrity operating windows (IOWs)** — limits that protect equipment over time
  (corrosion, creep, embrittlement). Short excursions may be allowed with reporting.
- **Normal operating limits** — where you aim to run; well inside the above.
Know, for each critical variable: the limit, the consequence of exceeding it, the
action to take, and how much time you have. That is what the "consequence of
deviation" tables in good operating procedures are for.

## 2. Bypasses and overrides on safety systems
A safety instrumented function (trip) or alarm that is bypassed removes a layer of
protection. Treat every bypass as a temporary change:
- Authorised by the right level, with a risk assessment and compensating measures
  (e.g. a dedicated operator watching the variable).
- Logged, time-limited, visible on the board, reviewed at every handover.
- Removed and the function proved after the work.

## 3. Isolation for permit-to-work
Before anyone opens equipment, the hazard must be isolated and proved.
1. **Identify every energy and material source:** process lines in and out, utilities,
   steam tracing, nitrogen, drains/vents, electrical supply, stored pressure,
   stored heat, gravity, springs.
2. **Choose the isolation standard** for the hazard: a single valve is weakest; double
   block and bleed is stronger; **positive isolation** (spade/blind or spool removal)
   is required for many vessel entries and high-hazard fluids. Your site's isolation
   standard decides.
3. **Apply:** close and lock valves, open and verify bleeds, isolate and lock
   electrical supplies (LOTO), each with personal locks or a lock box system.
4. **Prove:** depressurise and drain, check pressure gauges read zero, test the bleed
   for flow, test electrical "try-start" or voltage absence. **Isolation is not done
   until it is proven.**
5. **Record** isolation points on the isolation certificate attached to the permit.
6. **Line break:** first break on bolts furthest from you, expecting residual contents;
   correct PPE.
De-isolation is just as hazardous: confirm the work is complete, people clear,
equipment boxed up, then remove isolations in a planned order and leak-test.

## 4. Recognising a change that needs MOC
Management of Change applies to anything that is not "replacement in kind". Examples
operators meet:
- A new raw material supplier or grade, a new solvent, a different catalyst.
- Operating outside the documented range "because it works better".
- Changing an alarm or trip setpoint, a control configuration, a procedure step.
- Temporary hoses, temporary pumps, a jumper on a junction box.
- Staffing changes on a shift that affect who does critical tasks.
If you are not sure, ask the question formally — the cost is a form; the cost of an
uncontrolled change can be the plant.

## 5. HAZOP action follow-through
HAZOP recommendations become real only when closed out: a procedure updated, an alarm
added, a check valve installed. Operations' role: review recommendations that affect
operation, make sure procedure and training changes reach the shift, and flag actions
"closed" on paper but not in the field.

## Gotchas
- **Normalised deviance:** an alarm that "always" comes in, a limit routinely exceeded
  with no consequence. Each time, the margin shrinks unseen.
- Isolations that rely on a valve passing nothing — valves pass. Prove it.
- Permit handover at shift change: the permit is with the shift, not the person.

## Verify
- [ ] You can state SOLs, consequences and actions for your unit's critical variables.
- [ ] Every bypass/override is authorised, logged, visible and time-limited.
- [ ] Isolations identified all sources, met the site standard and were proven.
- [ ] Non-like-for-like changes went through MOC before, not after.
- [ ] HAZOP actions affecting operation verified in the field, not only on paper.
