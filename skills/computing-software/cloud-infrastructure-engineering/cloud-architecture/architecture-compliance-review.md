---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-compliance-review
name: architecture-compliance-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, togaf, architecture-compliance-review, compliance-assessment, conformance, architecture-conformance]
level: practitioner
status: draft
description: "Conduct an architecture compliance review of a cloud implementation against the target architecture, principles and standards, with graded findings."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-capability/chap05.html", "https://pubs.opengroup.org/togaf-standard/adm/chap10.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Architecture compliance review

TOGAF compliance levels: irrelevant, consistent, compliant, conformant, fully conformant, and
non-conformant. Most reviews just need to decide conformant vs non-conformant per area with
evidence.

## Steps
1. **Timing**: at design complete, before production go-live, and after significant change.
2. **Scope and checklist** tailored to the project: principles, reference architecture
   adherence, approved services, identity and network model, data classification controls,
   resilience (tested DR), observability, cost tagging, operational readiness.
3. **Collect evidence, not assertions**: IaC repository, policy compliance reports
   (Azure Policy, AWS Config, Security Command Center), architecture diagrams versus
   deployed resources (resource graph queries), test results.
4. **Grade findings**: critical (must fix before go-live), major (fix within agreed period),
   minor (improvement), with an owner and due date each.
5. **Outcome**: compliant, compliant with conditions, or non-compliant requiring a
   dispensation request.
6. **Feed back**: recurring findings indicate standards or templates to fix centrally.

## Gotchas
- Reviewing documents only misses drift between design and what is deployed.
- Automate the repeatable checks (policy-as-code) and reserve human review for judgement.

## Verify
- [ ] Findings have severity, owner, due date and closure evidence.
- [ ] Recurring findings reported to the board quarterly.
