---
id: engineering-technology.systems-engineering.interface-management.n2-diagrams-and-icd-authoring
name: n2-diagrams-and-icd-authoring
category: engineering-technology
field: systems-engineering
product: interface-management
tags: [interface-management, n2-diagram, n-squared, icd, interface-control-document, ird, idd, interface-working-group, interface-change-control, tbd-burndown, pinout, message-format, mechanical-interface, data-interface, configuration-management, nasa-se-handbook]
level: practitioner
status: docs-checked
description: "Find subsystem interfaces with an N2 matrix, then write and control interface documents: IRD/ICD/IDD/ICP roles, working group, change control, verification."
sources:
  - "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# N2 diagrams and ICD authoring — find every boundary, then freeze it under control

**Goal:** identify all interfaces between subsystems systematically, document each in a controlled interface document both sides agree, and change it only through an agreed process.

## 1. Find the interfaces (N2 matrix)
The NASA SE Handbook lists N-squared diagrams among the interface definition techniques. Practical method (a working convention, not a handbook rule):
1. Place the elements (subsystems, or functions at an earlier stage) on the diagonal, including external systems.
2. Pick one reading convention (outputs along rows or along columns), write it on the chart, and keep to it.
3. For each off-diagonal cell ask what is exchanged: mechanical, power, data, thermal, fluid, optical/RF, human, environmental.
4. Give every non-empty cell an interface ID and two named owners. Mark empty cells as deliberately empty with a reason.

## 2. Interface document types (NASA SE Handbook)
Interface control documentation identifies and captures interface information and approved interface change requests. Types the handbook names: Interface Requirements Document (IRD), Interface Control Document/Drawing (ICD), Interface Definition Document (IDD) and Interface Control Plan (ICP). These are maintained and approved through the configuration management process and become part of the project's technical data package. Agree at kick-off which document is binding.

## 3. What an interface document should pin down
Tailor per interface type; this list is practice guidance: scope and parties, applicable documents with editions, mechanical envelope and mounting, electrical connectors and pinouts, data protocol and field definitions with units and byte order, thermal and fluid limits, imposed environments, verification approach per item, and a TBD/TBR register with owner and need-by date.

## 4. Interface working group and control (handbook)
- An Interface Working Group (IWG) typically establishes communication between those responsible for interfacing systems, end products, enabling products and subsystems, and is responsible for planning, scheduling and executing interface activities. It is a technical team drawn from the interfacing parties (for example project and contractor) and may work independently or as part of a larger change control board.
- After interface requirements are baselined, use the requirements management process to identify changes, evaluate impact, document approval or disapproval and update the requirements database. Interfaces needing approval from all sides need unanimous approval. Changing interface requirements late in the life cycle is more likely to have a significant cost, schedule or technical impact.
- Keep work products: strategy and procedures, rationale for decisions, assumptions made in approving or denying changes, actions taken on anomalies, lessons learned.

## 5. Interfaces and verification
During integration, interface management supports review of integration and assembly procedures so interfaces are properly marked and compatible with specifications and ICDs. Interface control documentation and approved interface requirement changes feed product verification and validation; interface requirements verification is a critical aspect of overall system verification (see engineering-technology.systems-engineering.verification-validation.verification-cross-reference-matrix).

## Gotchas
- Units and byte order cause data-interface errors: state both for every field.
- State connector gender and the viewing face for pin numbering.
- An interface owned by "both" is owned by neither: name one responsible owner.
- Ground support equipment and test harness interfaces are interfaces too.

## Verify
- [ ] N2 includes external systems; every off-diagonal cell is filled or marked empty with a reason.
- [ ] Every interface ID has a document section, two owners and a verification method.
- [ ] Interface documents are signed by both parties and under configuration control.
- [ ] TBD/TBR register has an owner and date for every open item.
- [ ] Every document revision links to an approved change request.

## Checked
2026-11-01. Confirmed in the NASA Systems Engineering Handbook (SP-2016-6105 Rev 2): IRD/ICD/IDD/ICP names and role, configuration-management handling, IWG role and membership, change handling, unanimous approval, late-change impact, work products, link to verification and validation, N-squared diagrams listed as a technique. Removed (not stated in readable sources): the N2 row/column convention as fact, ICD content checklists with figures, ICWG cadence, PDR/CDR baselining targets, EIA-649 classification, DI-IPSC DID citations and the 132-cell example. The N2 steps are labelled as working convention.
Method: documentation only; no commands were run.
