---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-communication-plan
name: architecture-communication-plan
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, architecture-communication-plan, togaf, stakeholder-management, communications]
level: practitioner
status: draft
description: "Write an architecture communications plan: stakeholder groups, what each needs, channel, cadence, owner and feedback loop, tied to the stakeholder map."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap03.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap03.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture communications plan

## Steps
1. **Start from the stakeholder map** (power/interest grid): group stakeholders by concern:
   executives (outcomes, cost, risk), delivery teams (standards, patterns, deadlines), security
   and compliance (controls), operations (run model), finance (funding).
2. **Per group define**: key messages, the architecture views they need (viewpoints), channel
   (steering pack, wiki, town hall, design clinic, ADR feed), cadence, owner, and when feedback
   is collected.
3. **Event-driven messages**: decisions, principle changes, waivers granted, deprecations; push
   them, do not wait for people to read the repository.
4. **Two-way**: office hours and a channel for questions; track recurring questions and fix
   the docs.
5. **Measure reach**: attendance, page views, questions per release, survey of delivery leads.

## Gotchas
- One deck for every audience; executives and engineers need different views.
- Decisions communicated only in board minutes never reach teams.

## Verify
- [ ] Plan table: group, message, view, channel, cadence, owner.
- [ ] Decision and deprecation notices pushed to affected teams.
