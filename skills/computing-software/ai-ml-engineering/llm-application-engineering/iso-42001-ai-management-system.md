---
id: computing-software.ai-ml-engineering.llm-application-engineering.iso-42001-ai-management-system
name: iso-42001-ai-management-system
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, iso-42001, ai-management-system, ai-governance, certification, annex-a-controls]
level: practitioner
status: draft
description: "Implement an ISO/IEC 42001 AI management system: scope and AI policy, risk and impact assessments, Annex A controls and Statement of Applicability, audits and certification."
sources:
  - https://www.iso.org/standard/81230.html
  - https://www.iso.org/standard/77304.html
  - https://www.iso.org/standard/42005
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ISO/IEC 42001 AI management system

**Goal:** the organisation governs its AI systems through a certifiable management system that integrates with existing ISO 27001 / 9001 processes.

## Structure
Harmonised management-system clauses:
- **4 Context:** internal/external issues, interested parties, AI roles (provider, producer, user), AIMS scope.
- **5 Leadership:** AI policy, roles and responsibilities, top-management commitment.
- **6 Planning:** AI risk assessment and treatment, AI system impact assessment, AI objectives.
- **7 Support:** resources, competence, awareness, communication, documented information.
- **8 Operation:** operational planning and control, performing risk assessments, treatments and impact assessments.
- **9 Performance evaluation:** monitoring and measurement, internal audit, management review.
- **10 Improvement:** nonconformity, corrective action, continual improvement.

## Annex A controls (objectives)
Policies related to AI; internal organisation; resources for AI systems (data, tooling, compute, people); assessing impacts of AI systems; AI system life cycle (requirements, design, verification, deployment, operation, monitoring); data for AI systems (quality, provenance, preparation); information for interested parties (documentation, user information, incident reporting); use of AI systems (responsible use, intended use); third-party and customer relationships. Annex B gives implementation guidance; Annex C lists AI objectives and risk sources; Annex D covers domain use.

## Implementation steps
1. Define scope (which AI systems, sites, roles) and inventory AI systems.
2. Gap assessment against clauses and Annex A.
3. AI policy and governance roles (AI committee, system owners).
4. Risk assessment method (ISO/IEC 23894 guidance) and impact assessment process (ISO/IEC 42005) for affected individuals and society.
5. Statement of Applicability: each Annex A control included or excluded, with justification.
6. Implement controls, reusing ISO 27001 processes (document control, audit, supplier management).
7. Run internal audit and management review; fix nonconformities.
8. Certification audit by an accredited body: Stage 1 (documentation readiness), Stage 2 (effectiveness); then surveillance audits yearly and recertification every three years.

## Evidence auditors ask for
AI inventory, risk and impact assessments per system, SoA, lifecycle records (requirements, test results, release approvals), monitoring reports, incident logs, supplier assessments, training records, management review minutes.

## Verify
- [ ] Every in-scope AI system has a current risk and impact assessment.
- [ ] SoA justifies every exclusion.
- [ ] Internal audit completed with corrective actions tracked to closure.
