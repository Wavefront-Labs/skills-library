---
id: computing-software.cybersecurity-defensive.application-security.appsec-metrics
name: appsec-metrics
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [appsec-metrics, security-metrics, mttr, vulnerability-density, appsec-programme, kpi]
level: practitioner
status: draft
description: "Choose and report AppSec programme metrics: coverage, mean time to remediate, SLA compliance, defect density, escape rate and recurrence, with pitfalls to avoid."
sources: ["https://owaspsamm.org/model/governance/strategy-and-metrics/", "https://www.bsimm.com/framework/governance/strategy-and-metrics.html", "https://csrc.nist.gov/pubs/sp/800/55/v1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AppSec programme metrics

Report a handful of metrics that answer three questions: are we covering our software, are we fixing what we
find, and is new code getting better?

## Coverage
- % of production applications (by tier) with SAST, SCA, secrets scanning and DAST running in CI.
- % of tier-1 apps with a current threat model and a pentest in the last 12 months.
- Source: app inventory joined with tool project lists. Unknown apps are a finding in themselves.

## Remediation
- **Mean/median time to remediate** by severity (use median; outliers distort means).
- **SLA compliance**: % of findings closed within SLA, per team.
- **Open backlog age** distribution (how many criticals older than 30 days?).
- KEV/actively exploited items open (should be near zero).

## Quality of new code
- New findings per KLOC changed or per PR, trend over time.
- **Escape rate**: findings first found in pentest, bug bounty or production vs in CI/design.
- **Recurrence**: same CWE reintroduced in a team after training/fix.

## Programme
- SAMM or BSIMM score, annually.
- Security champion coverage (% teams with an active champion).
- Exceptions: count, % expired.

## Presenting
- Per-team views for engineering managers, roll-up trends for leadership, risk statements not raw counts
  ("3 internet-facing apps have unpatched critical dependencies older than 30 days").
- Pair every metric with a target and an owner.

## Pitfalls
- Raw finding counts rise when coverage improves; normalise and explain.
- Gamification: teams suppress or downgrade findings to hit SLA; audit a sample of closures.
- Do not compare teams with very different stacks on finding counts.
- Metrics that are manual to produce die; automate from the vulnerability management system.

## Verify
Dashboard regenerates from source systems, each metric has a defined formula and owner, and leadership saw a
decision-oriented summary in the last quarter.
