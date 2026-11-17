---
id: computing-software.qa-testing-engineering.test-case-design.failover-and-recovery-testing
name: failover-and-recovery-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [failover-testing, recoverability-testing, reliability-testing, disaster-recovery, rto, rpo, high-availability]
level: practitioner
status: docs-checked
description: "Test failover and recovery: kill primaries, measure detection and switchover time against RTO, verify data loss against RPO, and test failback."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover and recovery testing

**Goal:** demonstrate the system recovers within its RTO and loses no more than its RPO.

## Plan
- List redundant components and their failover mechanism: DB primary/replica (managed failover), load-balanced app nodes, multi-AZ/region, message broker clusters, caches.
- For each: trigger, expected detection time, expected switchover time, expected client impact.

## Run (under realistic load)
1. Start a steady load test (any load tool) with a known transaction mix, logging every request with timestamp and outcome.
2. Write marker records continuously (sequence numbers) to detect data loss.
3. Trigger the failure: `aws rds reboot-db-instance --force-failover`, stop the node/VM, delete a pod, cut network to an AZ (security group/NACL change), kill the broker leader.
4. Measure: time to first error, error window duration, time until throughput back to baseline, lost/duplicated marker records.
5. **Failback** to original topology and measure again (often forgotten, often broken).

## Pass criteria
Error window <= RTO; missing committed records within RPO (often zero); no manual steps beyond the runbook; alerts fired.

## Gotchas
- DNS TTLs and connection pools holding dead connections dominate failover time; check client-side reconnection settings.
- Testing with no load hides split-brain and in-flight transaction issues.

## Verify
Report with timeline graph (throughput and errors), measured RTO/RPO vs targets and runbook gaps.

## Checked

2026-10-28. Confirmed: `aws rds reboot-db-instance --force-failover` checked against the botocore model by check_commands.py (OK). Removed: Syllabus section number, Patroni, k6/JMeter and kubectl specifics.

Method: documentation only; no commands were run.
