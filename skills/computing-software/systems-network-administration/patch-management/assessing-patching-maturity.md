---
id: computing-software.systems-network-administration.patch-management.assessing-patching-maturity
name: assessing-patching-maturity
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patching-maturity, maturity-model, essential-eight, cis-controls, patch-metrics, nist-sp-800-40, patch-management]
level: advanced
status: draft
description: "Assess an organisation's patch management maturity across inventory, prioritisation, deployment, verification and exceptions, using evidence and frameworks like Essential Eight."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight/essential-eight-maturity-model
  - https://www.cisecurity.org/controls/continuous-vulnerability-management
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assessing patching maturity

**Goal:** a defensible picture of where the patch programme is weak, so investment goes to the constraint.

## Dimensions to score (1 = ad hoc ... 5 = optimised)
| Dimension | Level 1 | Level 3 | Level 5 |
|---|---|---|---|
| Inventory | Partial lists | Discovery reconciled weekly with CMDB | Continuous discovery, coverage >98% |
| Intelligence and triage | Reactive to news | Daily triage with logged decisions | Automated applicability, SSVC/KEV-driven |
| Prioritisation | Everything monthly | Tiered SLAs by criticality/exposure | Risk-based, exploit-aware, measured |
| Deployment | Manual per host | Automated rings with pre/post checks | Automated, self-healing, routine zero-touch |
| Verification | Job success = done | Authenticated rescans | Continuous verification, closed-loop tickets |
| Exceptions | Undocumented | Risk acceptances with expiry | Compensating controls tested, reviewed monthly |
| Coverage of non-OS | OS only | OS + major apps | OS, apps, firmware, network, containers, cloud images |
| Metrics | None | Coverage and latency per tier | Trends driving decisions and budget |

## Evidence, not interviews
For each score, collect artefacts: inventory reconciliation reports, triage log, SLA reports by tier, a sample of 10 recent critical advisories traced end to end (release -> decision -> deployed -> verified, with timestamps).

## External yardsticks
- ACSC Essential Eight "Patch applications" and "Patch operating systems" maturity levels set concrete timeframes (e.g. internet-facing services patched within 48 hours when an exploit exists at higher maturity levels; check the current model for exact figures).
- CIS Control 7 (Continuous Vulnerability Management) safeguards by implementation group.
- NIST SP 800-40r4 recommends tracking maturity alongside operational metrics.

## Output
A one-page scorecard with current and target levels, the top three constraints, and a 6-12 month roadmap tied to measurable metric changes.

## Verify
Re-assess after the roadmap period; scores move only when the evidence changed.
