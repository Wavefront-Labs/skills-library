---
id: computing-software.messaging-and-integration.redpanda.rolling-upgrade-limits-and-procedure
name: rolling-upgrade-limits-and-procedure
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rolling-upgrade, upgrade, maintenance-mode, rollback, license, breaking-changes, finalization]
level: advanced
status: docs-checked
description: "Rolling-upgrade a Redpanda cluster: one feature release at a time, rollback and downgrade limits, license check, breaking changes by version, and per-broker maintenance steps."
sources:
  - https://docs.redpanda.com/streaming/current/upgrade/rolling-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redpanda versions are AB.C.D (two-digit year, feature release, patch). A rolling upgrade puts each broker in maintenance mode, upgrades and restarts it, then moves on.

**Limits.**
- New features turn on only after every broker is upgraded.
- Upgrade one feature release at a time (22.2 to 22.3); skipping is unsupported.
- From 24.3, enterprise features without a valid license block feature-release upgrades: check with `rpk cluster license info`.
- Roll back to the original version only while at least one broker still runs it and the cluster has not restarted; deferred finalization (enterprise, upgrading to 26.2+) keeps a rollback path open.
- Downgrades are only between patch releases of one feature release after finalization.
- Remote Read Replica clusters are upgraded first.

**Breaking changes to review:** 26.2 enables Schema Registry contexts by default; 26.1 FIPS needs SASL/SCRAM passwords of 14+ characters; 25.3 forbids explicit schema IDs outside import mode; 25.2 removes HTTP Proxy ephemeral credentials; 24.2 resets unspecified AlterConfigs values and sets `transaction_max_timeout_ms` to 15 minutes.

**Procedure per broker.**

```bash
rpk cluster info -b --detailed
rpk cluster health
rpk cluster maintenance enable <node-id> --wait
rpk cluster maintenance status
rpk cluster health --watch --exit-when-healthy
sudo apt install redpanda=<version>
sudo systemctl restart redpanda
rpk cluster maintenance disable <node-id>
rpk cluster maintenance status
```
Use `yum update redpanda-<version>` on RedHat. Before starting, consider temporarily raising `replication.factor` for single-replica topics, since they go unavailable. Expect transient client latency, CPU spikes while replicas rebalance, and under-replicated alerts. Finish with `rpk cluster health`.

## Checked

2026-11-04. Limits, breaking-change list, restart impact and commands were confirmed on the Rolling Upgrade page; the list of breaking changes is abridged.

Method: documentation only; no commands were run.
