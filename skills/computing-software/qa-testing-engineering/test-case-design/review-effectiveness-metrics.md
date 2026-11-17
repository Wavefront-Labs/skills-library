---
id: computing-software.qa-testing-engineering.test-case-design.review-effectiveness-metrics
name: review-effectiveness-metrics
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [review-effectiveness-metrics, review-metrics, static-testing, reviews, defect-removal-efficiency]
level: practitioner
status: docs-checked
description: "Measure and tune reviews: preparation rate, review size, defects per hour and per KLOC, and review effectiveness against defects found later."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/67407.html
  - https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Review effectiveness metrics

**Goal:** know whether reviews pay off and where to tune them.

## Metrics to collect per review
| Metric | Formula |
|---|---|
| Size | pages, requirements, or LOC reviewed |
| Preparation effort | reviewer hours before the meeting |
| Preparation (checking) rate | size / preparation hours |
| Defects found | count by severity |
| Defect density | defects / size (e.g. per KLOC or per page) |
| Efficiency | defects / total review hours |
| Effectiveness (yield) | defects found in review / (found in review + found later in that artefact) |

## Rules of thumb (published data)
- Code review (SmartBear/Cisco study): review no more than 200-400 LOC at a time, under 500 LOC per hour; the study reports diminishing defect discovery above 400 LOC and a drop in defect density at faster rates.
- Very fast checking rates with few findings usually mean a skimmed review, not clean work.

## Using the data
1. Plot defect density against checking rate; set your team's maximum rate where density falls off.
2. Compute effectiveness quarterly by linking escaped defects back to the reviewed artefact.
3. Classify review findings (logic, interface, missing requirement, standards) to refine checklists.
4. Report trends, not individual reviewer counts.

## Gotchas
- Using metrics to rank people kills honest logging; aggregate at team level.
- Effectiveness needs a lag: defects found later are only known weeks after release.
- Count majors separately; ten typo findings are not equal to one logic defect.

## Verify
A review log with size, effort and findings for each formal review, and a quarterly chart of checking rate vs defect density.

## Checked

2026-10-28. Confirmed: SmartBear page: 200-400 LOC at a time, under 500 LOC per hour, 60 to 90 minutes. Removed: Syllabus-linked claims and the Fagan-style 60-90% removal figure.

Method: documentation only; no commands were run.
