---
id: computing-software.cybersecurity-defensive.application-security.security-release-criteria
name: security-release-criteria
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-release-criteria, release-gate, bug-bar, final-security-review, sdl, appsec]
level: practitioner
status: draft
description: "Define security release criteria: a bug bar by severity, required activities per risk tier, automated pipeline gates, final security review and the exception process."
sources: ["https://learn.microsoft.com/en-us/previous-versions/windows/desktop/cc307404(v=msdn.10)", "https://www.microsoft.com/en-us/securityengineering/sdl/practices", "https://csrc.nist.gov/pubs/sp/800/218/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security release criteria

Microsoft's SDL introduced the **bug bar** (which severity of security bug blocks release) and the **final
security review** (FSR). The aim: an objective, pre-agreed definition of "secure enough to ship".

## 1. Tier applications by risk
Example: Tier 1 internet-facing or handles regulated data; Tier 2 internal with sensitive data; Tier 3
internal low risk. Criteria scale with tier.

## 2. Bug bar
| Severity | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Critical | Blocks release | Blocks | Blocks |
| High | Blocks | Blocks unless exception | Fix within 30 days |
| Medium | Fix within 30-60 days | 90 days | Backlog |
| Low | Backlog | Backlog | Backlog |
Severity comes from a defined method (CVSS plus context, or an internal rating), not the scanner default.

## 3. Required activities per tier
- Threat model current for the release scope (Tier 1-2).
- SAST and SCA with no new findings above the bar; secrets scan clean.
- DAST or authenticated scan on staging (Tier 1).
- Pentest for major releases or annually (Tier 1).
- Security sign-off on new external interfaces or authentication changes.

## 4. Automate what can be automated
Pipeline gates fail the build on new findings above the bar (SAST, SCA, container scan, IaC scan). Manual
activities are recorded as checklist items in the release ticket, with links to evidence.

## 5. Final security review
For Tier 1 major releases: AppSec reviews open findings, threat model status, pentest results and exceptions,
and records one of: passed, passed with exceptions, or failed.

## 6. Exceptions
Documented with risk owner (business, not just engineering), compensating controls, and expiry date.
Expired exceptions block the next release.

## Gotchas
- Criteria nobody can meet get bypassed; baseline legacy debt and gate on new findings.
- Gate on severity *after* triage, or false positives block releases and destroy trust.
- Publish criteria before projects start so teams can plan.

## Verify
Release tickets show criteria evidence, the pipeline blocks a test build with a seeded high finding, and every
active exception has an owner and unexpired date.
