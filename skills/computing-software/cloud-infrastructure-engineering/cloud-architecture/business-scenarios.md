---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.business-scenarios
name: business-scenarios
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, business-scenarios, togaf, requirements-elicitation, smart-objectives, problem-statement]
level: practitioner
status: draft
description: "Use the TOGAF business scenario technique to derive architecture requirements: problem, environment, objectives, human and computer actors, roles and SMART success measures."
sources: ["https://pubs.opengroup.org/togaf-standard/business-architecture/business-scenarios.html", "https://pubs.opengroup.org/togaf-standard/adm/chap04.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business scenarios technique

## Phases of the technique
1. **Identify, document and rank the problem** driving the scenario.
2. **Document the business and technical environment** (current processes, systems, constraints).
3. **Identify and document objectives** - SMART (specific, measurable, actionable, realistic,
   time-bound).
4. **Identify human actors** and their place in the business model.
5. **Identify computer actors** (systems) and their roles.
6. **Document roles, responsibilities and measures of success** per actor.
7. **Check for fitness for purpose and refine** with the stakeholders.

## Cloud example
Problem: Month-end reporting takes 5 days because data is extracted manually from 12 systems.
Objective: Reports available 24 hours after period close by Q3, with lineage.
Actors: Financial controller, data engineer; ERP, data platform, BI tool.
Measures: close-to-report time, manual steps count, data quality incidents.

## Outputs
- Requirements (functional and non-functional) traced to objectives.
- Inputs to the architecture vision and Phase B/C/D.
- Scenario document reviewed by business owners.

## Gotchas
- Writing scenarios about technology ("move ERP to cloud") rather than business problems.
- Skipping step 7: scenarios not validated by the people who live the process.

## Verify
- [ ] Objectives are SMART and have measures.
- [ ] Each derived requirement traces to a scenario objective.
