---
id: repair-maintenance.reliability-engineering-failure-analysis.fmea.equipment-fmea-scoring-and-action-tracking
name: equipment-fmea-scoring-and-action-tracking
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: fmea
tags: [fmea, fmeca, pfmea, dfmea, failure-mode-and-effects-analysis, rpn, risk-priority-number, action-priority, aiag-vda, severity, occurrence, detection, criticality, failure-modes, corrective-actions, risk-ranking, iec-60812, reliability, maintenance, worksheet, spreadsheet]
level: practitioner
status: draft
description: "Run an equipment or process FMEA: build the worksheet, brainstorm failure modes, score severity/occurrence/detection on a 1-10 scale, rank by S first then RPN or AP, and track actions to rescoring."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Equipment FMEA: scoring and action tracking

**Goal:** systematically find how a piece of equipment or a process can fail, rank
the risks consistently, and drive actions that measurably lower them — not produce a
spreadsheet nobody opens again.

> Draft: scales and ranking rules vary — classic RPN (S×O×D), the AIAG-VDA 2019
> Action Priority (AP) tables, IEC 60812, MIL-STD-1629A criticality. Pick one,
> write its scales down, and use them for the whole study.

## 1. Set up
- **Scope:** one system or process, with a block diagram or process flow so everyone
  sees the boundary.
- **Team:** 4–7 people — operator, maintainer, engineer, quality, a facilitator who
  owns the worksheet.
- **Scales agreed before scoring** — printed and on the wall. Without anchor
  definitions, scores drift between sessions.

Example 1–10 anchors (adapt):
| Score | Severity (S) | Occurrence (O) | Detection (D) |
|---|---|---|---|
| 10 | injury/regulatory breach without warning | > 1 per week | no way to detect before effect |
| 7–8 | line stop > 8 h / major scrap | ~monthly | detected only by customer or at failure |
| 4–6 | line stop < 8 h / rework | ~yearly | periodic inspection may catch it |
| 2–3 | minor nuisance | < once per 5 yrs | condition monitoring reliably catches it |
| 1 | no effect | practically never | certain detection, automatic |

Note D is inverted: **high D = poor detection.**

## 2. Worksheet columns
`Item/Step | Function | Failure mode | Effect | S | Cause | O | Current controls (prevent / detect) | D | RPN or AP | Recommended action | Owner | Due | Action taken | new S | new O | new D | new RPN/AP`

A spreadsheet works; keep one row per **cause** (one mode often has several causes,
each with its own O and D).

## 3. Fill it — one column at a time across rows
- Work **function by function**; the failure mode is the opposite or degradation of
  the function ("does not seal", "seals intermittently").
- **Effects** at local, system and end level; S is scored on the worst credible effect.
  S belongs to the effect, so all causes of the same mode share S.
- **Causes** at a level you can act on (wrong torque, lubricant degraded, operator
  skips step), using data from CMMS history and failure reports, not just opinion.
- Score **O** from data where possible (failure rate, MTBF); **D** for the current
  controls only, not controls you wish you had.

## 4. Rank
- **Severity first:** any S ≥ 9 gets an action regardless of RPN.
- Then by RPN (S×O×D, 1–1000) or AP (High/Medium/Low per AIAG-VDA tables).
  RPN has known flaws — 9×2×2 = 36 ranks below 4×4×4 = 64 — so never use an RPN cutoff
  alone (e.g. "only > 100").
- Pareto the top 10–20% for actions.

## 5. Actions that actually reduce risk
Priority of action type:
1. **Design out** the mode or reduce S (guarding, redundancy, material change).
2. **Reduce O** (better spec, preventive task, error-proofing/poka-yoke).
3. **Improve D** (sensors, alarms, inspection, condition monitoring).
Each action: one owner (named), a due date, and a definition of done. Review open
actions at every FMEA session and weekly in the maintenance meeting.

## 6. Rescore and close
After an action is implemented and verified (in service or by test), rescore
S/O/D. If the new score didn't drop, the action didn't work — say so.
Keep the FMEA live: update after failures not in the sheet, design changes, and
annually.

## Quick sanity calc
```
RPN = S * O * D        # 1..1000
# spreadsheet: =C2*E2*G2 ; conditional-format S>=9 red regardless of RPN
```

## Gotchas
- Scoring D on hoped-for controls makes risks disappear on paper.
- Endless brainstorming: time-box sessions (2 h) and park out-of-scope items.
- Mixing up mode, effect and cause in one cell — enforce the columns.
- Actions like "train operators" without verification rarely change O.

## Verify
- [ ] Scope diagram and written S/O/D scales exist and were used throughout.
- [ ] One row per cause; S tied to effect, O from data where available.
- [ ] All S ≥ 9 items have actions regardless of RPN/AP.
- [ ] Every action has owner, due date and definition of done.
- [ ] Completed actions were rescored; FMEA has a next review date.
