---
id: computing-software.qa-testing-engineering.test-case-design.project-risk-management-for-testing
name: project-risk-management-for-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [project-risks, risk-management, test-management, risk-mitigation, istqb, ctfl]
level: practitioner
status: draft
description: "Manage project risks to testing: identify schedule, environment, skills and supplier risks, assess, assign owners and mitigations, and escalate when they materialise."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Project risk management for testing

**Goal:** protect the test effort from the things that stop it happening on time, as distinct from product risks (things wrong with the software). ISTQB CTFL 5.2.

## Typical project risks to testing
- **Organisational:** late delivery of builds, scope creep, budget cuts, priority changes.
- **People:** key tester leaving, missing skills (performance, security, domain), part-time allocation.
- **Technical:** test environment late or unstable, test data unavailable or not masked, tools not licensed, integrations with third-party sandboxes down.
- **Supplier:** vendor delivers late or with poor quality; contractual acceptance unclear.
- **Process:** requirements unstable, poor defect turnaround, no code freeze.

## Process
1. Identify at test planning with dev lead, PM, ops; revisit at each milestone or sprint review.
2. Assess likelihood and impact (1-5 each) and note the trigger that shows it is materialising.
3. Choose a response: mitigate (book environments early, cross-train), transfer (contract penalties), accept (with a contingency plan), avoid (change approach).
4. Assign an owner and due date; most project risks are owned outside the test team.
5. Record in the test plan risk section or the project RAID log.
6. When triggered, escalate with impact on test completion ("environment 2 weeks late = regression shortened, residual risk in payments").

## Verify
The test plan lists project risks with owner, response and trigger, and status reports flag any triggered risk with its impact on scope or date.
