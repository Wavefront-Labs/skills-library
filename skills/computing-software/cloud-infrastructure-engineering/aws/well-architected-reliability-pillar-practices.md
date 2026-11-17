---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-reliability-pillar-practices
name: well-architected-reliability-pillar-practices
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, reliability-pillar-practices, reliability-pillar, failure-management, change-management, service-quotas]
level: practitioner
status: docs-checked
description: "Well-Architected Reliability pillar in practice: quotas and network foundations, distributed design, change management and failure management with tested recovery."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected Reliability pillar practices

The pillar has 13 questions (REL 1 to REL 13), each with numbered best practices (for example `REL01-BP01`). Use
the lists below as an evidence checklist; titles are from the Reliability pillar contents page.

## Foundations (REL 1-2)
- [ ] REL01-BP01/BP02: service quotas and constraints known and managed across accounts and Regions, including
      the recovery Region.
- [ ] REL02-BP01/BP02: highly available connectivity for public endpoints; redundant connectivity between private
      networks in the cloud and on premises.

## Workload architecture (REL 3-5)
- [ ] REL03: segment the workload and build services around business domains.
- [ ] REL04: know your distributed-system dependencies; loosely coupled dependencies; constant work; idempotent
      mutating operations (REL04-BP04).
- [ ] REL05: graceful degradation, throttle requests, control and limit retries (REL05-BP03), fail fast and limit queues,
      set client timeouts (REL05-BP05), stateless systems where possible, emergency levers.

## Change management (REL 6-8)
- [ ] REL06: monitor all components, calculate metrics, notify and automate responses, analyse logs, review
      monitoring scope, trace requests end to end.
- [ ] REL07: obtain and scale resources automatically on impairment or demand; load test the workload (REL07-BP04).
- [ ] REL08: runbooks for standard activities such as deployment; functional and resiliency testing in the
      deployment; immutable infrastructure; automated deployments.

## Failure management (REL 9-13)
- [ ] REL09: back up all data that needs it, secure and encrypt backups, automate backups, and periodically
      recover data to verify backup integrity (REL09-BP04).
- [ ] REL10: deploy to multiple locations, automate recovery for single-location components, and use bulkhead
      architectures to limit scope of impact (REL10-BP03).
- [ ] REL11: monitor to detect failures, fail over to healthy resources, automate healing, rely on the data plane
      rather than the control plane during recovery (REL11-BP04), use static stability (REL11-BP05), notify on
      availability-impacting events, architect for availability targets and SLAs.
- [ ] REL12: playbooks to investigate failures, post-incident analysis, test scalability and performance, test
      resiliency with chaos engineering (REL12-BP04), conduct game days regularly (REL12-BP05).
- [ ] REL13: recovery objectives for downtime and data loss defined (REL13-BP01) and a defined recovery strategy
      that meets them (REL13-BP02); see the Disaster Recovery of Workloads on AWS whitepaper for the strategies.

## Review tips
Ask "when did you last test it?" for backups, failover, scaling and DR; an untested practice is not in place.
Typical high-risk findings: single-location stateful tiers, restores never tested, unlimited retries, unmonitored
quotas, manual deployments without rollback.

## Verify
- [ ] Reliability answers cite test dates (restore, failover, game day) and alarm names.
- [ ] High-risk issues tracked to closure with milestones in the WA Tool.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Reliability pillar and Framework documentation
(Framework published 6 November 2024). Confirmed: the question groupings REL 1 to REL 13 and the quoted best-practice
titles (REL01-BP01 to REL13-BP02, including REL04-BP04, REL05-BP03/BP05, REL07-BP04, REL09-BP04, REL10-BP03,
REL11-BP04/BP05, REL12-BP04/BP05) against the pillar contents page, and the DR whitepaper title. Removed invented
details with no pillar page behind them: "N+1 AZ" capacity, "twice a year" game days, and cells and shuffle
sharding. Replaced prose-title `sources` with real URLs.
Method: documentation only; no commands were run.
