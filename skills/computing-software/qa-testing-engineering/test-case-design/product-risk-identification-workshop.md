---
id: computing-software.qa-testing-engineering.test-case-design.product-risk-identification-workshop
name: product-risk-identification-workshop
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [product-risk-identification, risk-workshop, risk-based-testing, risk-register, test-planning]
level: practitioner
status: draft
description: "Facilitate a product risk identification workshop: invite the right roles, use quality characteristics and past defects as prompts, and produce a usable risk register."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/test-manager
  - https://www.iso.org/standard/81291.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Product risk identification workshops

**Goal:** a shared list of what could go wrong with the product, so testing effort follows risk (ISTQB CTFL 5.2, ISO/IEC/IEEE 29119-2 risk-based testing).

## Who
Product owner, developers, architect, tester(s), ops/SRE, support, security if relevant. 6-10 people, 60-90 minutes per feature area or release.

## Inputs
Scope (stories, architecture diagram), defect history and incident post-mortems, support ticket themes, regulatory needs, dependency changes.

## Prompts (run them in order)
1. **Quality characteristics (ISO 25010)**: for each of functional suitability, performance, compatibility, usability, reliability, security, maintainability, portability: "How could this fail here?"
2. **Change**: what is new, complex, rewritten, or written by a new team?
3. **History**: which components produced the most defects/incidents (defect clustering)?
4. **Business impact**: money flows, legal/compliance, safety, reputation, data loss.
5. **Usage**: most used flows, most valuable customers, peak periods.
6. **Dependencies**: third-party APIs, migrations, infra changes.
7. **Pre-mortem**: "It is three months after release and this failed badly. What happened?"

## Writing risks
Format: *cause -> event -> consequence*. "Because the tax engine is rewritten, VAT may be miscalculated for EU B2B orders, causing incorrect invoices and fines." Vague risks ("performance") are not testable.

## Output: risk register row
| ID | Risk | Characteristic | Owner | Likelihood | Impact | Level | Mitigation | Status |

Likelihood/impact scoring happens next (see risk-matrix-likelihood-impact).

## Gotchas
- Only testers in the room = only test risks found; business impact needs the business.
- Project risks (late environment, staff) belong in the project risk log, not the product register.
- Silent participants: use silent brainstorming on sticky notes before discussion.

## Verify
Every risk is phrased cause-event-consequence, has an owner, and every high-change area of the release appears at least once.
