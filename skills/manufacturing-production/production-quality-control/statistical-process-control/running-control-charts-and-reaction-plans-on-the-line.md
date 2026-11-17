---
id: manufacturing-production.production-quality-control.statistical-process-control.running-control-charts-and-reaction-plans-on-the-line
name: running-control-charts-and-reaction-plans-on-the-line
category: manufacturing-production
field: production-quality-control
product: statistical-process-control
tags: [statistical-process-control, spc, control-chart, xbar-r, i-mr, p-chart, np-chart, c-chart, u-chart, control-limits, specification-limits, western-electric-rules, nelson-rules, special-cause, common-cause, rational-subgroup, subgroup-size, sampling-frequency, reaction-plan, out-of-control-action-plan, ocap, cpk, ppk, capability, tampering, over-adjustment, spc-software, infinityqs, q-das, winspc, operator-spc, production-quality-control]
level: practitioner
status: draft
description: "Keep a running process in control: take rational subgroups, plot and read control charts with the run rules, follow the reaction plan, avoid tampering, and keep capability honest."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running control charts and reaction plans on the line

**Goal:** the chart tells you *when* to act and *when to leave the process alone*, and
everyone on the line reacts the same way. Designing the SPC system (which
characteristics, which charts) is covered in
engineering-technology.industrial-manufacturing-systems-engineering.quality-engineering.control-chart-design-and-spc-rollout;
this skill is running it day to day.

## 1. Two kinds of limit — never mix them
- **Specification limits** (from the drawing/customer): is this part good?
- **Control limits** (calculated from the process, ±3σ of the plotted statistic): has the process changed?
A point can be inside spec and out of control (act: something changed) or in control
and out of spec (the process is not capable — management problem, not an operator reaction).
**Never draw spec limits on an Xbar chart** — averages are less spread than individuals.

## 2. Taking the sample
- **Rational subgroup**: consecutive parts made under the same conditions (e.g. 5 in a
  row from the same cavity/spindle), so within-subgroup variation is just short-term noise.
- Take subgroups at the planned frequency **and** after any change: start-up, tool
  change, material lot change, shift change, adjustment.
- Measure with the specified gauge; record time and any event (new coil, tool change) on the chart.

## 3. Reading the chart: common run rules
(Western Electric/Nelson; your site picks which ones are active)
1. One point beyond a control limit.
2. Seven to nine points in a row on one side of the centreline (shift).
3. Six points in a row steadily rising or falling (trend — tool wear, temperature).
4. Two of three points beyond 2σ on the same side.
5. Fourteen points alternating up and down (over-adjustment or two streams mixed).
6. Fifteen points hugging the centreline (limits wrong, or mixed streams/data edited).
Check the **range/MR chart first**: if variation is out of control, the Xbar limits aren't trustworthy.

## 4. Reaction plan (OCAP)
Each chart should have a written reaction plan. Typical:
1. Confirm the measurement (re-measure, check gauge zero).
2. Look for the assignable cause: tool, material, setting, operator change, machine alarm.
3. Correct the cause; note the action **on the chart** at that point.
4. **Contain**: check parts produced since the last in-control subgroup; segregate if any could be out of spec.
5. Take a new subgroup to confirm return to control.
6. Escalate if no cause found or rule violations repeat.

## 5. Don't tamper
Adjusting the process after every in-control point that "looks a bit high" **increases**
variation (Deming's funnel). If the chart is in control, leave it. Allowed adjustments
(e.g. tool-wear offset) should be defined in the reaction plan with a trigger and a size.

## 6. Recalculating limits and capability
- Recalculate control limits only after a **documented, intentional process change**
  and enough new data (often 20–25 subgroups), not because points keep going out.
- Capability (Cpk/Ppk) is valid only from in-control data; report which data range it used.
- Typical targets: Cpk ≥ 1.33 ongoing, ≥ 1.67 for critical or new processes (customer-specific).

## Gotchas
- Filling in a subgroup at end of shift from memory — fabricated SPC is worse than none.
- "Sorting" measurements: only plotting good parts, or re-measuring until within limits.
- Using spec limits as control limits ("the chart has never gone out" — because it can't).
- Combining two cavities/spindles in one subgroup, hiding a difference between them.
- Ignoring the attribute chart because "it's only cosmetic defects".

## Verify
- [ ] Subgroups taken at the planned frequency and after every event.
- [ ] Range/MR chart checked before the Xbar chart.
- [ ] Every rule violation has an annotation: cause, action, containment, confirmation.
- [ ] No adjustments made on in-control signals outside the reaction plan.
- [ ] Control limits' source and date are known; capability reported from in-control data only.
