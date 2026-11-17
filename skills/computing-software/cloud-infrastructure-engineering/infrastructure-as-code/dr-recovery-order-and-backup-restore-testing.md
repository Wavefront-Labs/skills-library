---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.dr-recovery-order-and-backup-restore-testing
name: dr-recovery-order-and-backup-restore-testing
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, disaster-recovery-iac, recovery-order, restore-test, disaster-recovery]
level: advanced
status: draft
description: "Map service dependencies into a recovery order for rebuild-from-code DR, and test backups by restoring them automatically and checking data integrity."
sources: ["AWS Well-Architected Reliability - disaster recovery (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html)", "AWS Backup restore testing (https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html)", "NIST SP 800-34 contingency planning (https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# DR recovery order and restore testing

## Recovery order
Rebuilding from code fails if layers come up in the wrong order. Build a dependency map:
1. Identity and access (IdP, break-glass accounts, KMS keys)
2. Networking (VPC/VNet, DNS zones, VPN/Direct Connect)
3. Secrets (Vault, secret managers) and state backends
4. Automation platform (CI runners, AAP, artifact registries, hub)
5. Data stores (restore from backups/replicas)
6. Shared services (queues, caches, logging, monitoring)
7. Applications (by tier), then ingress/CDN, then DNS cutover

Capture it as code: an ordered pipeline or AAP workflow whose nodes are these layers, with health checks between nodes. Document circular dependencies (monitoring needs network; network change needs monitoring) and break them with minimal bootstrap configs.

## Restore testing
- **Automate**: scheduled restore of the latest backup into an isolated account/subscription, e.g. AWS Backup restore testing plans, or a pipeline that restores a DB snapshot to a temp instance.
- **Validate integrity**, not just "restore succeeded": row counts vs source metrics, checksums, application-level queries, schema version.
```yaml
- name: Restore latest snapshot to a test instance
  amazon.aws.rds_instance:
    db_instance_identifier: restore-test-{{ ansible_date_time.date }}
    creation_source: snapshot
    db_snapshot_identifier: "{{ latest_snapshot }}"
    db_instance_class: db.t3.medium
    state: present
- name: Integrity check
  community.postgresql.postgresql_query:
    login_host: "{{ restored_endpoint }}"
    query: SELECT count(*) FROM orders WHERE created_at > now() - interval '2 days'
  register: q
- ansible.builtin.assert: {that: q.query_result[0].count | int > 0}
```
- Measure restore duration against RTO; measure snapshot age against RPO.
- Clean up test restores automatically.

## Gotchas
- Backups encrypted with keys that do not exist in the DR region/account are unrestorable: replicate keys.
- Restore tests must include secrets and IaC state backups, not only databases.

## Verify
- [ ] Monthly restore test report shows duration, data checks passed and cleanup done.
