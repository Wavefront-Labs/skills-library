---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.dr-from-code-rpo-rto-rebuild-runbooks-and-automated-tests
name: dr-from-code-rpo-rto-rebuild-runbooks-and-automated-tests
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, disaster-recovery-iac, rpo, rto, rebuild-runbook, rebuild-from-code, dr-test]
level: advanced
status: draft
description: "Set RPO and RTO per service, write a rebuild-from-code runbook that a new engineer can follow, and prove both with a scheduled automated DR rebuild test."
sources: ["AWS Well-Architected Reliability Pillar - Plan for disaster recovery (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html)", "AWS whitepaper - Disaster Recovery of Workloads on AWS (https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)", "Google SRE Book - Testing for Reliability, disaster recovery testing (https://sre.google/sre-book/testing-reliability/)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR from code: RPO/RTO, rebuild runbooks and automated tests

## 1. Targets per service
| Term | Meaning | Driven by |
|---|---|---|
| **RPO** | max data loss window | backup/replication frequency |
| **RTO** | max time to restore service | rebuild automation + data restore speed |

Write them down per service with the business owner, e.g. `orders: RPO 15 min, RTO 1 h`;
`reporting: RPO 24 h, RTO 1 day`. Pick the strategy from them: backup & restore (hours),
pilot light (tens of minutes), warm standby (minutes), multi-site active/active (near zero).

## 2. What "rebuild from code" requires
- **All** infrastructure in IaC: network, IAM, DNS, secrets *definitions*, monitoring. Anything clicked in a console is a DR gap — find it with drift detection and `terraform import`/config-as-code.
- Bootstrap dependencies documented: state backend bucket, CI runners, artifact registry, vault unseal keys, break-glass credentials, DNS registrar access. These are usually what blocks a real DR.
- Data restore separate from infra rebuild: snapshot ids / backup vault / PITR timestamp as inputs.
- Parameterised region/account: `-var region=eu-central-1`, inventories per DR site.

## 3. The runbook (in the repo, next to the code)
```
docs/dr/orders.md
1. Declare incident; decision owner: <role>. Target region: eu-central-1.
2. Prereqs check: access to <break-glass account>, CI runner in DR region, state bucket replica.
3. terraform -chdir=envs/dr init && terraform -chdir=envs/dr apply -var restore_snapshot_id=<id>
4. ansible-playbook -i inventories/dr site.yml --tags base,app
5. Restore data: <command>, verify row counts/checksums.
6. Switch DNS: terraform -chdir=dns apply -var active_region=dr
7. Smoke tests: <script>. Record actual RTO/RPO achieved.
8. Failback procedure: ...
```
Each step: exact command, expected output, time budget, who can do it.

## 4. Automated DR test
Scheduled pipeline (monthly/quarterly) into an isolated account:
```yaml
dr-rebuild-test:
  schedule: "0 3 1 * *"
  steps:
    - terraform -chdir=envs/dr-test apply -auto-approve -var restore_snapshot_id=$(latest_snapshot)
    - ansible-playbook -i inventories/dr-test site.yml
    - ./tests/smoke.sh https://orders.dr-test.example.com
    - ./tests/data_freshness.sh --max-age 15m      # RPO check: newest restored record age
    - record duration as RTO metric; alert if > target
    - terraform -chdir=envs/dr-test destroy -auto-approve
```
Track achieved RTO/RPO over time on a dashboard; a regression is a bug.

## Gotchas
- Restores from backups that were never restored are hopes, not backups.
- Region-specific values (AMI ids, AZ names, KMS keys) hard-coded in code break DR builds — data sources/maps per region.
- Quotas in the DR region (vCPU, IPs) are often too low; request them in advance and check in the test.

## Verify
- [ ] Last DR test date, achieved RTO/RPO are recorded and within targets.
- [ ] A person who did not write the code executed the runbook successfully at least once.
