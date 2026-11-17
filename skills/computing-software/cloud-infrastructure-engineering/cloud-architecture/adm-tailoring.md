---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.adm-tailoring
name: adm-tailoring
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, togaf, architecture-principles, adm-tailoring, agile-architecture, togaf-adm]
level: advanced
status: draft
description: "Tailor the TOGAF ADM for agile cloud delivery: which phases to keep, iteration cycles, minimal artefacts per phase and integration with product teams."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap02.html", "https://pubs.opengroup.org/togaf-standard/guides/agile-architecture.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap03.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tailoring the ADM for agile cloud delivery

TOGAF expects tailoring: the Preliminary phase explicitly adapts the method, and the ADM
supports iteration cycles (architecture capability, development, transition planning,
governance). Running every phase with full deliverables on every change is a misuse.

## Steps
1. **Classify the work by level**: strategic (enterprise, multi-year), segment (a domain or
   portfolio) and capability (one product or platform increment). Use the full cycle only
   at strategic level.
2. **Pick minimal artefacts per phase** for capability-level work:
   - A: one-page vision with stakeholders, drivers and success measures.
   - B-D: a C4 context and container diagram plus key ADRs.
   - E/F: a backlog of epics sequenced by dependency rather than a migration plan document.
   - G: lightweight compliance via PR checklists and policy-as-code.
   - H: change requests feeding the backlog; fitness functions to detect drift.
3. **Run iteration cycles** aligned to planning increments (e.g. quarterly): revisit vision
   and roadmap each increment, not once.
4. **Embed architects** in product teams or as an enabling team; the board reviews only
   decisions that cross team boundaries or breach principles.
5. **Document the tailoring** (what you skip and why) in the architecture repository so
   auditors and new staff see a deliberate method.

## Gotchas
- Tailoring to nothing leaves no traceability for regulators; keep the decision log.
- Big upfront target architectures go stale before delivery; set direction and guardrails instead.

## Verify
- [ ] Written tailoring statement exists and is approved.
- [ ] Each level has a defined artefact set and review trigger.
