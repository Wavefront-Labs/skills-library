---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-architecture-principles
name: cloud-architecture-principles
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, togaf, architecture-principles, cloud-architecture-principles, preliminary-phase, principle-catalogue]
level: practitioner
status: draft
description: "Write cloud architecture principles in TOGAF form (name, statement, rationale, implications) that are testable, few in number and used in design reviews."
sources: ["https://pubs.opengroup.org/togaf-standard/adm-techniques/chap02.html", "https://pubs.opengroup.org/togaf-standard/adm/chap02.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing cloud architecture principles

TOGAF defines a principle as name, statement, rationale and implications. Good principles
constrain decisions; bad ones ("we value security") constrain nothing.

## Steps
1. **Gather drivers**: business strategy, regulatory constraints, existing enterprise
   principles, lessons from incidents and audits.
2. **Draft 8-15 principles**, each with:
   - **Name**: short and memorable ("Managed services first").
   - **Statement**: one unambiguous sentence.
   - **Rationale**: the business benefit, in business terms.
   - **Implications**: what teams must do, stop doing or fund. This is where principles bite.
3. **Test quality** (TOGAF criteria): understandable, robust (supports decisions in
   ambiguous cases), complete, consistent (principles may tension but must not contradict),
   stable.
4. Typical cloud set: managed services before self-managed; everything as code; identity is
   the perimeter; design for failure; cost is an architecture attribute with an owner;
   data classified before it moves; buy before build for commodity capability.
5. **Ratify** through the architecture board, publish in the repository, and reference
   principles by name in ADRs and review checklists.
6. Review annually; retire principles nobody cites.

## Gotchas
- Principles without implications are slogans.
- Too many principles means none are remembered; 15 is a ceiling.
- Write the conflict rule (e.g. security over cost for restricted data) instead of pretending there is none.

## Verify
- [ ] Each principle has rationale and at least two concrete implications.
- [ ] Recent ADRs cite principles by name.
