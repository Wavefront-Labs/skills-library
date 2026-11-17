---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.business-information-map
name: business-information-map
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, information-map, togaf, phase-b, conceptual-data-model, business-glossary]
level: practitioner
status: draft
description: "Build a business information map and conceptual data model: key information concepts, owners, relationships and which capabilities create or use each."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap04.html", "https://www.businessarchitectureguild.org/page/BIZBOK", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business information map and conceptual data model

## Steps
1. **List information concepts** in business language (Customer, Policy, Claim, Order,
   Product, Invoice); 20-60 concepts for an enterprise; no tables or attributes yet.
2. **Define each** in a glossary entry: definition, examples, synonyms used by different units,
   business owner (accountable for meaning and quality).
3. **Relationships**: a conceptual model with cardinality in words ("a Customer holds many
   Policies"). Keep it on one page.
4. **Cross-map to capabilities** (create/read/update/delete matrix): which capability creates
   the authoritative record, which consume it. Multiple creators of the same concept flag a
   master data problem.
5. **Annotate classification and residency** per concept (personal data, regulated,
   confidential) so cloud placement and protection decisions inherit it.
6. **Hand off** to Phase C as the input for the logical data model and data entity catalogue.

## Gotchas
- Arguing about one universal definition: record variants per unit and pick the authoritative.
- Jumping to physical schemas loses business stakeholders.

## Verify
- [ ] Glossary with owners and classification per concept.
- [ ] Capability/information CRUD matrix shows one creator per concept or a flagged issue.
