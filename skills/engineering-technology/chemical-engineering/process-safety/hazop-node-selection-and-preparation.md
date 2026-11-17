---
id: engineering-technology.chemical-engineering.process-safety.hazop-node-selection-and-preparation
name: hazop-node-selection-and-preparation
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-hazard-identification, hazop-node-selection-and-preparation, hazop, hazop-preparation, study-nodes, design-intent, iec-61882, hazop-team, process-hazard-analysis, pha-preparation]
level: practitioner
status: gated
description: "Prepare a HAZOP: choose study nodes and design intent, assemble the team and P&ID package, set risk matrix and scope, following IEC 61882 and CCPS practice."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAZOP node selection and preparation

**Goal:** a HAZOP that is well-scoped and uses its meeting time on analysis. HAZOP is a team method led by a trained, experienced facilitator; this skill describes practice and defers to the governing standard (IEC 61882 for HAZOP studies (gated: unconfirmed, source is paywalled or blocked); CCPS Guidelines for Hazard Evaluation Procedures) and to your regulator's requirements (for example OSHA 29 CFR 1910.119(e) process hazard analysis in the United States, Seveso/COMAH in Europe; confirm the current text for your jurisdiction).

## Preparation steps
1. **Define scope and objectives**: which units and which modes (normal, start-up, shutdown, maintenance); which hazards (safety, environment, operability).
2. **Collect the package**: up-to-date P&IDs, PFDs, heat and material balance, cause-and-effect or interlock descriptions, relief valve data and design basis, equipment data sheets, hazardous area drawings, previous incident and HAZOP reports, operating and start-up procedures.
3. **Divide into nodes**: a node is a section of the process with a clear design intent (for example "Transfer of feed from tank T-101 to reactor R-201 via pump P-101"). Mark nodes on the P&IDs with colours; keep nodes small enough to analyse in about 30 to 60 minutes (practice rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
4. **Write the design intent** for each node: the purpose, normal flows, temperatures, pressures and compositions.
5. **Choose the risk matrix** (severity by likelihood) and the tolerable-risk criteria beforehand so the team does not argue them in the room.
6. **Team**: facilitator (leader), scribe, process engineer, operations representative, instrument/control engineer, maintenance, safety; add specialists as needed (reaction chemistry, mechanical). Typical meeting length is a few hours per day for a limited number of days.
7. **Logistics**: schedule, room, display of P&IDs, software or worksheet template, agreed recording style.

## Gotchas
- An out-of-date P&ID wastes the study; check revision against the plant as built (for existing plants, field verification).
- Missing operating modes (start-up, emergency shutdown) are where many incidents occur.
- Nodes that are too big produce shallow analysis.

## Verify
- [ ] Nodes marked and design intents written and agreed with operations.
- [ ] Risk matrix, scope and team approved before the first session.
