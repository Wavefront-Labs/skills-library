---
id: engineering-technology.chemical-engineering.process-safety.what-if-and-checklist-methods
name: what-if-and-checklist-methods
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-hazard-identification, what-if-and-checklist-methods, what-if-analysis, checklist-method, hazard-identification, pha, process-hazard-analysis, what-if-checklist, ccps, screening-hazard-review]
level: practitioner
status: verified
description: "Use what-if, checklist and what-if/checklist methods for hazard identification of simpler or well-understood processes, with question lists and when HAZOP is needed instead."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What-if and checklist methods

**Goal:** a structured, lighter-weight hazard review where it is appropriate. The choice of method is part of the process hazard analysis programme and, in regulated settings, must meet the regulator's requirements (OSHA 29 CFR 1910.119(e)(2) lists what-if, checklist, what-if/checklist, HAZOP, FMEA, fault tree analysis or an appropriate equivalent methodology, checked against the eCFR; confirm the current text).

## What-if
1. Gather the process description and drawings; assemble a small team (process, operations, safety).
2. Generate questions "What if ... ?" about each area: equipment failure (pump stops, valve sticks), human error (wrong valve opened, wrong material charged), external events (power loss, loss of cooling water, fire), operating conditions (high temperature, contamination).
3. For each question: consequence, existing safeguards, risk ranking, recommendations.
4. Review each node systematically, not randomly, using the P&ID.

## Checklist
Use a pre-written list drawn from codes and past experience: Are relief devices sized for each scenario? Are incompatible materials segregated? Are hazardous areas classified? Are emergency stops accessible? Checklists verify conformance to known standards; they do not find novel hazards.

## What-if/checklist
Combine: the checklist anchors completeness, the what-if questions probe beyond it.

## Selection guidance
- Simple, well-understood processes, minor modifications, or early-stage design: what-if or checklist.
- Complex, novel, high-hazard processes (high pressure, toxic, reactive): HAZOP (and where warranted, LOPA, QRA).
- Equipment-failure focus: FMEA (see the `fmea-for-process-equipment` skill).

## Gotchas
- Checklists are only as good as their last update; keep them under revision control.
- What-if reviews depend on team imagination; use guidewords from HAZOP to prompt.

## Verify
- [ ] The method is justified in the PHA plan against the process complexity.
- [ ] Findings are tracked as actions with owners.
