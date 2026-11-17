---
id: computing-software.cybersecurity-defensive.security-architecture.dr-failover-testing
name: dr-failover-testing
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, dr-failover-test, disaster-recovery, failover, failback, rto-validation, game-day, chaos-engineering]
level: advanced
status: draft
description: "Plan and run DR failover tests: walkthrough to full failover, success criteria against RTO/RPO, isolated bubbles, failback, and turning findings into fixes."
sources: ["https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/testing-disaster-recovery.html", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR failover testing

A DR plan that has never been executed is a hypothesis. NIST SP 800-34 describes tests, training
and exercises; aim to progress from talking to doing.

## Test types (increasing realism)
1. **Plan walkthrough / tabletop**: owners talk through the runbook; finds missing steps and contacts.
2. **Component tests**: restore one database, fail over one load balancer, recover DNS.
3. **Isolated (bubble) failover**: replicas brought up in an isolated network (Azure Site Recovery
   "Test failover", AWS DRS drills, VMware SRM test recovery); production keeps running.
4. **Planned production failover**: real traffic moves to the DR site, runs there, then fails back.
5. **Unannounced / game day**: simulate loss of a region or site (chaos engineering), measure response.

## Define success before the test
- Measured RTO (time from declaration to service accepting traffic) vs target.
- Measured RPO (last transaction present after recovery) vs target.
- Functional checks: login, a business transaction end to end, integrations, batch jobs.
- Security controls present in DR: logging to SIEM, EDR, MFA, firewall rules, backups running.

## Running an isolated test
- Isolate network (no IP conflicts or duplicate AD DCs talking to production).
- Recover dependencies in order: identity (DC/IdP), DNS, PKI, databases, apps, front ends.
- Time every step; log deviations from the runbook.
- Clean up test resources afterwards (they cost money and are unmonitored attack surface).

## Failback
Often harder than failover: data written in DR must replicate back; plan and test it, including
reverse replication setup.

## Findings
Typical: expired credentials in DR, firewall rules not replicated, licence servers, hard-coded IPs,
certificates bound to production names, missing runbook steps, people who left. Each finding gets an
owner and due date; retest.

## Cadence
Critical tier: isolated test at least twice a year, planned failover yearly; after major changes.

## Gotchas
- Ransomware scenarios differ: replicas may be encrypted too; test recovery from immutable backups,
  not just replication.
- Testing only infrastructure, not business processes, overstates readiness.

## Verify
Test report with measured RTO/RPO per service vs targets, functional checks passed, and closed findings
from the previous test.
