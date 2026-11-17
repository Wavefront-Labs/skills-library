---
id: computing-software.cloud-infrastructure-engineering.google-cloud.chaos-engineering-and-fault-injection-on-gcp
name: chaos-engineering-and-fault-injection-on-gcp
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, ha-dr-design, chaos-engineering, fault-injection, resilience-testing, game-days]
level: advanced
status: docs-checked
description: "Run controlled chaos experiments on GCP: steady-state hypotheses, LB fault injection, database failover tests, and blast-radius guards."
sources: ["https://cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-failures", "https://cloud.google.com/load-balancing/docs/https/traffic-management-global#fault_injection", "https://cloud.google.com/sql/docs/mysql/configure-ha#test", "https://github.com/GoogleCloudPlatform/chaos-engineering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaos engineering and fault injection on GCP

## 1. Structure every experiment
1. **Objectives and scope**: which components, services or regions are in scope, including external dependencies.
2. **Steady state**: the SLI you will watch (error ratio, tail latency) from Cloud Monitoring.
3. **Hypothesis**: a written, measurable statement of what should still hold during the fault.
4. **Environment and blast radius**: prefer a staging or sandbox environment that replicates production. If you test in production, have automated monitoring and manual rollback ready.
5. **Backup plan**: snapshots or backups of critical databases and services before the test, and people ready to intervene manually if automated failover fails.
6. **Inform stakeholders** (operations, DevOps, application owners) of schedule, scope and expected impact.
7. **Escalate gradually** and record findings as follow-up actions.

## 2. Faults you can inject
| Fault | How |
|---|---|
| HTTP errors / latency | External Application Load Balancer URL map `routeAction.faultInjectionPolicy`: delay injection (delays a user-defined portion of requests before the backend) and abort injection (answers a fraction of requests with a user-defined HTTP status). Look up the exact field names in the URL map API reference |
| Database failover | Cloud SQL (needs high availability configured first): `gcloud sql instances failover PRIMARY_INSTANCE_NAME`, or the console Failover button. Wait for any previous failover to complete before starting another |
| Instance / node failure | Custom scripts, for example shutting down a primary node in a multi-zone GKE cluster or disabling a Cloud SQL instance |
| Network outage | Scripts using firewall rules or API restrictions to simulate a region-wide outage, scoped to your test |
| Region failover, release rollback, restore from backup | Include these in periodic recovery tests |

## 3. Tooling
Google's framework page names Chaos Monkey as an example tool and custom scripts as an alternative. The `GoogleCloudPlatform/chaos-engineering` repository holds Chaos Engineering recipes for Google Cloud, including Chaos Toolkit examples and a GKE Chaos Toolkit operator.

## Gotchas
- Do not run first experiments in production, and never without the on-call aware and an abort path.
- Remove injected configuration (route rules, firewall rules) with a script afterwards: forgotten fault rules are outages.
- Check IAM roles and failover configuration before the test so the test fails for the reason you intended.

## Verify
- [ ] Experiment log shows hypothesis, observed SLI, outcome and follow-up actions, and the injected faults were removed.

## Checked
2026-11-09. Confirmed in the Well-Architected reliability page (objectives and scope, environment, backups, stakeholders, simulated failures, gradual escalation, Chaos Monkey), the load-balancing traffic management page (faultInjectionPolicy with delay and abort injection), the Cloud SQL HA page (failover test command and prerequisites) and the chaos-engineering repository README (recipes, Chaos Toolkit examples, GKE operator). Removed: the 0.5 percent example threshold, the YAML field snippet (field names unconfirmed), AlloyDB failover command, kubectl drain/delete commands, Litmus/Chaos Mesh mentions, the quota and reservation remark, and the MIG zone-resize recipe.
Method: documentation only; no commands were run.
