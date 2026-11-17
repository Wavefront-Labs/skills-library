---
id: computing-software.cybersecurity-defensive.threat-modelling.abuse-and-misuse-cases
name: abuse-and-misuse-cases
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [abuse-cases, misuse-cases, security-requirements, threat-modelling, user-stories, business-logic]
level: practitioner
status: docs-checked
description: "Write abuse cases per feature in a short workshop, record them with IDs and risk ratings, and turn selected ones into security requirements (OWASP Abuse Case Cheat Sheet)."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Abuse and misuse cases

Note: OWASP has moved this cheat sheet to a "Historical" archive, saying reviewers found
abuse cases rarely used in practice, that the abuse case framework seems heavyweight with few
published success stories, and that the material is a getting-started tutorial. Use the
approach below as a lightweight option, not a standard.

## Definition (cheat sheet)
An abuse case is a way of using a feature that the implementer did not expect, allowing an
attacker to influence the feature or its outcome through their action or input. It can be used
to discover attacks ("what can go wrong") and to record them in a form less intimidating to
developers. Generic requirements such as "the application must be secure" are too vague to
help a team, which is why the attacks to defend against are listed.

## Defining the list (workshop approach)
- Participants: a business analyst (explains each feature), a risk analyst (rates business
  risk), a penetration tester (proposes attacks, ideally two with different backgrounds),
  technical leads, and a QA or functional tester (knows how the feature should work, not work
  and fail). An AppSec person helps identify countermeasures.
- Start with about 4 hours, depending on the number of features. The output is a list of
  abuse cases for all features, each with a risk rating for filtering and prioritisation.
- Mark each case as Technical (for example XSS in a comment field) or Business (for example
  changing an article's price before ordering).
- Timing: in agile, after the meeting that puts user stories into a sprint; in waterfall, when
  the business features are identified.
- Selected cases become security requirements in the feature specification (waterfall) or
  acceptance criteria of the user story (agile), which lets cost and effort be estimated.
  Give every abuse case a unique ID (for example `ABUSE_CASE_001`).

## Tracking sheets (cheat sheet example)
- FEATURES: ID, name, short description.
- ABUSE CASES: ID, feature ID impacted, attack description, attack reference ID if any
  (example: CAPEC-17), business risk rating, CVSS severity and vector if applicable, kind
  (Technical or Business), applicable countermeasure ID, handling decision (To Address or
  Risk Accepted).
- COUNTERMEASURES (optional): ID, short description, hint. It helps judge whether a fix is
  easy, which can change the risk rating.

## Business-logic examples (OWASP SAMM text quoted in the sheet)
Abuse of functionality, also called a business logic attack, depends on how functions are
designed and implemented; an example is using a password reset flow to enumerate accounts.
Identify the important business rules and turn them into experiments that check the
application enforces them. SAMM's example: on a stock trading application, can an attacker
start a trade at the start of the day, lock in a price, hold it open to the end of the day
and complete it only if the price rose?

## Verify
- [ ] Each selected abuse case has an ID, a risk rating and a handling decision.
- [ ] Each case to address appears as a requirement or acceptance criterion.

## Checked
Confirmed 2026-11-09 against the OWASP Abuse Case Cheat Sheet, the definition, workshop, timing and sheet-layout sections (lines 1-120 of the local copy), including its Historical archive statement.
Removed as unconfirmed: the persona and prompt brainstorm lists, the discount-code examples with the 10-character code and 5-attempts rate limits, the atomic-redemption advice, the test-derivation step, OWASP OAT and ASVS as idea sources, and the fraud-team gotchas. The ASVS and Threat Modeling Manifesto sources were not used and were dropped from `sources`.
Method: docs-checked 2026-11-09 against cheatsheetseries.owasp.org Abuse_Case_Cheat_Sheet
