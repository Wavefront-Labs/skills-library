---
id: computing-software.software-engineering.software-architecture.architecture-views-and-viewpoints
name: architecture-views-and-viewpoints
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, architecture-views, 4-plus-1-views, iso-42010, viewpoints, stakeholders]
level: practitioner
status: draft
description: "Describe an architecture through views and viewpoints: Kruchten's 4+1 views, ISO/IEC/IEEE 42010 concepts, choosing views per stakeholder concern and consistency checks."
sources:
  - https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf
  - https://www.iso-architecture.org/42010/
  - https://www.viewpoints-and-perspectives.info/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture views and viewpoints

No single diagram describes a system. A **view** shows the system from one set of concerns; a **viewpoint** is the convention (notation, rules, audience) for constructing that kind of view.

## ISO/IEC/IEEE 42010 vocabulary
- **Stakeholders** have **concerns** (performance, security, deployability, cost).
- An **architecture description** contains **views**, each conforming to a **viewpoint** that frames certain concerns.
- **Correspondences** relate elements across views (this component runs on that node); **rationale** records decisions.
Use it as a checklist: every important stakeholder concern is addressed by at least one view.

## Kruchten's 4+1 views (1995)
| View | Shows | Typical diagrams | Main audience |
|---|---|---|---|
| Logical | functional decomposition, key abstractions | class/component diagrams, domain model | developers, analysts |
| Process (runtime) | concurrency, distribution, processes/threads, communication | sequence, activity, communication diagrams | integrators, performance engineers |
| Development (implementation) | code organisation: modules, packages, layers, build | package/module diagrams | developers, build/release |
| Physical (deployment) | mapping of software to hardware/infrastructure | deployment diagrams | ops, SRE |
| +1 Scenarios | a few key use cases that tie the four together and validate them | use case/sequence | everyone |

## Rozanski and Woods viewpoints
Context, Functional, Information, Concurrency, Development, Deployment, Operational - plus **perspectives** (security, performance and scalability, availability, evolution) that cut across views rather than being views themselves.

## Practice
1. List stakeholders and their top concerns.
2. Pick the minimum set of viewpoints that covers them (often: context, functional/logical, deployment, runtime for 2-3 critical scenarios).
3. Draw each view with one consistent notation (C4 for structure, UML sequence for runtime).
4. Check correspondence: every container in the logical view is deployed somewhere in the deployment view; every scenario step maps to an element.
5. Record rationale (ADRs) for why the views look as they do.

## Verify
- [ ] Concern-to-view matrix has no uncovered high-priority concerns.
- [ ] Walking the +1 scenarios through the other views finds no missing elements or connections.
