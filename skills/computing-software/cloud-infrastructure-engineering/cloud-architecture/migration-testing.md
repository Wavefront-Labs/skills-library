---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-testing
name: migration-testing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-execution, migration-testing, uat, smoke-tests, data-validation, performance-baseline, test-plan]
level: practitioner
status: draft
description: "Plan migration testing: smoke, functional/UAT, integration, data validation, performance against the pre-migration baseline, failover and security checks with exit criteria."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-playbook/test.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/", "https://www.istqb.org/certifications/certified-tester-foundation-level"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration test plan and UAT

## Test types
| Type | What | Who |
|---|---|---|
| Smoke | Services start, ports open, logs flowing, monitoring agent reporting | Migration pod |
| Functional / UAT | Key business transactions per test scripts | App owner / business users |
| Integration | Each interface (inbound/outbound) works from the new location | App + partner teams |
| Data validation | Row counts, checksums, sample record comparison, last transaction present | DBA |
| Performance | Response times and batch duration vs pre-migration baseline | Perf / app team |
| Resilience | Instance/AZ failure behaviour, backup job runs and restores | Ops |
| Security | Ports exposure scan, agent coverage, IAM | Security |

## Steps
1. **Baseline before migration**: capture response times, batch durations, error rates.
2. Agree test scripts and **exit criteria** with the owner (e.g. all P1 scripts pass, no Sev1/2
   defects, performance within 10% of baseline).
3. Run tests on the test launch; fix and repeat.
4. During cutover, run a reduced smoke + critical-path set before go/no-go.
5. Record evidence; owner signs off.

## Gotchas
- No baseline, so "it feels slower" debates can't be settled.
- Testing from inside the cloud network only; real users come through VPN/internet.
- Batch jobs and month-end processes untested until month-end.

## Verify
- [ ] Signed UAT with evidence.
- [ ] Performance comparison table vs baseline.
