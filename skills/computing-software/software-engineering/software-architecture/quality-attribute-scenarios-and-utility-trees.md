---
id: computing-software.software-engineering.software-architecture.quality-attribute-scenarios-and-utility-trees
name: quality-attribute-scenarios-and-utility-trees
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, quality-attribute-scenarios, utility-tree, atam, non-functional-requirements, quality-attributes]
level: practitioner
status: draft
description: "Turn vague quality goals into testable quality-attribute scenarios (six-part form) and prioritise them in a utility tree, as used in ATAM and arc42."
sources:
  - https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/
  - https://www.oreilly.com/library/view/software-architecture-in/9780136885979/
  - https://quality.arc42.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quality-attribute scenarios and utility trees

"The system must be fast and secure" cannot guide design or be tested. SEI's method (Bass, Clements, Kazman, *Software Architecture in Practice*) turns each goal into a scenario.

## Six-part scenario
| Part | Example (performance) | Example (availability) |
|---|---|---|
| Source | 1,000 concurrent users | internal health check |
| Stimulus | submit search queries | detects primary DB node failure |
| Artifact | search API | order database cluster |
| Environment | normal operation, peak hour | normal operation |
| Response | results returned | failover to replica, writes resume |
| Response measure | p95 < 300 ms, p99 < 800 ms | within 30 s, no committed orders lost (RPO 0) |
Write the measure as something you can test or monitor. Cover other attributes: modifiability ("a developer adds a new payment provider in under 3 days without changing order code"), security ("an attacker with a stolen session token cannot access another tenant's data; attempts are logged and alerted within 5 min"), deployability, testability, usability.

## Utility tree
Root "Utility" -> quality attributes -> refinements -> concrete scenarios, each rated (H/M/L) on two axes:
- **Importance** to the business.
- **Difficulty/risk** to achieve architecturally.
```
Utility
├── Performance
│   └── Latency: search p95 < 300 ms at 1k users          (H, M)
├── Availability
│   └── DB failover < 30 s, RPO 0                         (H, H)
└── Modifiability
    └── new payment provider < 3 dev-days                 (M, L)
```
(H, H) scenarios drive the architecture and get analysed first.

## Using them
- Elicit in a workshop with stakeholders (Quality Attribute Workshop, or as step 5 of ATAM).
- Map each high-priority scenario to architectural tactics (caching, replication, redundancy, modular boundaries) and record decisions as ADRs.
- Turn measures into fitness functions: load tests with thresholds (k6), chaos experiments for failover, architecture tests for modifiability rules, SLOs and alerts.

## Verify
- [ ] Every top quality goal has at least one scenario with a numeric response measure.
- [ ] Each (H, H) scenario has a linked decision and an automated or scheduled check.
