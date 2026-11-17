---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-collaboration
name: finops-collaboration
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-principles, finops-collaboration, cross-functional-collaboration, finops-personas, operating-model]
level: practitioner
status: docs-checked
description: "Set up the FinOps cross-functional working model: which personas take part, who owns what, shared data and terms, and a cadence agreed with each group."
sources: ["https://www.finops.org/framework/principles/", "https://www.finops.org/framework/personas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps cross-functional collaboration model

Principle 1 of the FinOps Framework: "Teams need to collaborate". Finance, technology, product and leaders work
together, with coordination from executives to engineers across all personas.

## Steps
1. **Map personas to named people.** The Framework says personas are broad stakeholder groups, not individuals; one
   persona may cover many roles, and in very small organisations one person may hold several. Core personas are FinOps
   Practitioner, Engineering, Finance, Product, Procurement and Leadership; allied personas (ITAM, ITFM, Sustainability,
   ITSM, Security) join where they exist.
2. **Write down who owns each recurring decision**, using the Framework's persona responsibilities as the start:
   engineering owns architecture, resource optimisation and monitoring; finance owns budgeting and forecasting support,
   cost allocation analysis and reporting; procurement owns vendor negotiation and discount management; product owns
   requirements and value delivery; leadership owns priorities and accountability; the FinOps practitioner bridges
   them. Keep the result as a short responsibility table.
3. **Centralise what benefits from scale.** The principle "FinOps should be enabled centrally" says rate, commitment
   and discount optimisation are best centralised so engineers stay focused on usage, while the central function
   encourages and enables best practice in a shared accountability model.
4. **Push ownership of usage to the edge.** Engineers take ownership of cost from design to operations, and teams manage
   usage against budgets they help control.
5. **One accessible, timely, accurate dataset.** Share cost data as soon as it is available, give consistent
   visibility to all levels, and use FOCUS and other methods to normalise data.
6. **Agree a meeting and reporting cadence per group** with those groups; the Framework gives no fixed cadence.
7. **Agree how disagreements and unresolved recommendations escalate**, and record the path.

## Gotchas
- A FinOps team that does optimisation on engineers' behalf builds a queue; keep engineers owning action and FinOps owning insight.
- Procurement or commitment decisions made without engineering and product input produce poor commitments.

## Verify
- [ ] Each business area has named counterparts for the persona groups it needs.
- [ ] The responsibility table is published and used when a decision is disputed.

## Checked
Confirmed on the FinOps Framework Principles page (collaboration, ownership, accessible data, centralised enablement)
and Personas page (core and allied personas, responsibilities, personas as groups not individuals). Removed: the
RACI letter assignments, weekly 15-minute and monthly and quarterly meeting formats, 30-day escalation rule, named
roles such as FP&A analyst and tech lead, and the Practice Operations source (not used for any retained claim).
Method: docs-checked 2026-11-09 against finops.org Framework Principles and Personas pages
