---
id: computing-software.cybersecurity-defensive.application-security.insecure-design
name: insecure-design
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [insecure-design, owasp-a04, secure-design, business-logic-flaws, security-requirements, design-review]
level: practitioner
status: docs-checked
description: "Prevent OWASP A04 insecure design: security requirements per feature, business logic limits, secure design patterns, design review gates and abuse-case tests."
sources: ["https://top10.owasp.org/2021/A04_2021-Insecure_Design/index.html", "https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Insecure design (OWASP A04:2021)

Insecure design is a missing or ineffective control, as opposed to a flawed implementation of a correct
design. Perfect code cannot fix a design that never limited, checked or separated the right things. OWASP
examples: credential recovery by "questions and answers" (which NIST 800-63b, ASVS and the Top 10 prohibit,
since answers can be known by several people); a cinema chain that lets group bookings reach a maximum of
fifteen attendees before a deposit is required, so an attacker books a huge number of seats in a few
requests; a retailer with no bot protection, letting scalpers buy scarce high-end video cards (suggested
domain rule: flag purchases within seconds of availability).

## Practices that prevent it (OWASP "How to Prevent")
1. A secure development lifecycle with AppSec professionals to design security and privacy controls.
2. A library of **secure design patterns or paved-road components** (central authn/authz, safe upload
   service, secrets handling) that teams reuse.
3. **Threat modeling** for critical authentication, access control, business logic and key flows;
   integrate it into refinement sessions.
4. **Security language and controls in user stories**: who may do this, how often, with what data, what is
   logged, which limits apply. Turn chosen abuse cases into acceptance criteria (OWASP Abuse Case cheat sheet).
5. **Plausibility checks** at each application tier, frontend to backend.
6. **Unit and integration tests** for critical flows using both use cases and misuse cases (user A cannot
   read user B's order; a limit is actually refused when exceeded).
7. **Segregate tiers** at system and network level by exposure, and **segregate tenants** by design.
8. **Limit resource consumption** per user or service.

## Spotting it in review
- Workflows where the client controls state transitions or prices (the cheat sheet's business abuse-case
  example: modifying an article's price before the order is placed).
- Missing step-up authentication on sensitive actions.
- Trust in data from another tenant, a partner, or an earlier step without re-validation.
- Features with no limit on cost to the business.

## Gotchas
- Abuse cases drive security requirements and tests, but OWASP's cheat sheet itself notes the formal
  abuse-case framework is heavyweight with few published success stories: keep it pragmatic.
- Log design-flaw findings separately so the shift-left effect can be measured.

## Verify
High-risk features have documented security requirements and a recorded design review, and misuse-case
tests exist for each business limit.

## Checked
2026-11-01. Confirmed in OWASP Top 10:2021 A04 (three scenarios, nine prevention bullets) and the OWASP Abuse
Case Cheat Sheet (abuse cases as requirements and acceptance criteria, business vs technical abuse cases,
heavyweight caveat). Removed: SAMM link (not fetched), invented examples, security-champion gate, scanner
vs pentest effectiveness claim, quota and cooling-off specifics.
Method: documentation only; no commands were run.
