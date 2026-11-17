---
id: energy-mining-utilities.power-transmission-distribution.network-switching.writing-and-executing-a-switching-schedule
name: writing-and-executing-a-switching-schedule
category: energy-mining-utilities
field: power-transmission-distribution
product: network-switching
tags: [network-switching, switching-schedule, switching-program, switching-instructions, isolation, earthing, grounding, point-of-isolation, point-of-earthing, permit-to-work, access-permit, sanction-for-test, safety-document, lockout-tagout, loto, danger-tag, caution-tag, test-for-dead, voltage-detector, repeat-back, three-way-communication, control-room, operator, authorised-person, backfeed, parallel-feeds, ring-main-unit, rmu, load-break-switch]
level: advanced
status: draft
description: "Plan, check and carry out a switching schedule that isolates and earths network plant for work: identifying all sources, step order, repeat-back communication, permits and restoration."
sources:
  - "General principles common to utility safety rules (isolation, earthing, safety documents); paraphrased and jurisdiction-neutral"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing and executing a switching schedule

**Goal:** make a piece of network plant safe to work on (isolated from every source,
locked, proven dead and earthed), hand it over under a safety document, then put it
back without surprises. Switching kills people when a source is missed, a step is
done on the wrong device, or a verbal instruction is misheard. Your company's safety
rules and authorisation levels define who may do what; this is the method beneath them.

## 1. Plan: find every source
Draw (or mark up) the single-line diagram for the work area and ask, for each
conductor that will be touched: **how could it become live?**
- Normal feeds and alternative feeds (ring circuits, normally-open points).
- Backfeeds through transformers from the LV side, including customer generation,
  solar inverters and standby generators.
- Voltage transformers that can be back-energised from secondary wiring.
- Capacitors and long cables holding charge; induced voltage from parallel live lines.
Every one of those needs a **point of isolation** and the work area needs **points
of earthing** between it and each source.

## 2. Write the schedule
Each step is one action on one uniquely identified device:
`Step | Location | Device ID | Operation | Time | Initials`
- Order: open load-breaking devices before disconnectors (never break load on an
  off-load disconnector); isolate all sources; lock and tag each point of isolation;
  **test for dead** at the point of earthing; apply earths; then issue the permit.
- Include checks as steps ("confirm open by indication and visual break").
- Restoration is a separate, equally detailed section in reverse logic.
- Have it **independently checked** by a second authorised person against the
  current diagram, not memory. Network changes since the diagram was printed are a
  classic trap.

## 3. Execute with disciplined communication
- **Three-way communication:** controller issues one step; operator repeats it back
  verbatim including device ID; controller confirms "correct"; operator does it and
  reports completion and time. Never accept "next three steps" in one breath.
- At the device: **read the label, compare with the schedule, touch the label**
  before operating. Check you are at the right site, panel and circuit.
- After each operation, confirm state by more than one indication where possible
  (mechanical indicator, visible break, meter reading, SCADA).
- **Test for dead** with an approved detector proved on a known live source before
  and after the test. Then earth — earths on before anyone touches.
- If anything doesn't match the schedule (device in an unexpected state, label wrong,
  unexpected indication), **stop**. Don't improvise; report and replan.

## 4. Safety documents
- Issue the permit (or equivalent) stating exactly what is isolated, where earths are,
  what work may be done and what remains live nearby. The recipient signs it, the crew
  is briefed, and the key/lock regime is recorded.
- **Sanction-for-test** (where earths must come off to test) is a separate document;
  the permit is suspended while it applies.

## 5. Restoration
- Permit cleared and cancelled by the recipient (all crew and tools clear, work-area
  earths removed), then remove switching earths, unlock, and restore by schedule.
- Check load and voltage once back in service; confirm customers restored.

## Common mistakes
- Missing an LV or generator backfeed. Operating the twin device in the next panel.
- Earthing before testing for dead. "Quick" restoration done from memory.
- Two controllers giving instructions on the same network area.

## Verify
- [ ] Every source identified on a current diagram, with isolation and earth points.
- [ ] Schedule independently checked; one device and one action per step.
- [ ] Every step repeated back and logged with time.
- [ ] Locks and tags on all isolation points; dead proven before earthing.
- [ ] Permit issued and later cancelled before any earths removed.
