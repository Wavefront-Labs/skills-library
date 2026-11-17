---
id: computing-software.cloud-infrastructure-engineering.azure.log-analytics-dedicated-cluster-and-workspace-replication
name: log-analytics-dedicated-cluster-and-workspace-replication
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, log-analytics, log-analytics-dedicated-cluster, workspace-replication-failover, commitment-tier, customer-managed-key]
level: sme
status: docs-checked
description: "Decide on Log Analytics dedicated clusters (commitment tier, CMK, cross-workspace query) and configure workspace replication with switchover and failback."
sources: ["https://learn.microsoft.com/azure/azure-monitor/logs/logs-dedicated-clusters", "https://learn.microsoft.com/azure/azure-monitor/logs/workspace-replication", "https://learn.microsoft.com/azure/azure-monitor/logs/customer-managed-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log Analytics dedicated clusters and workspace replication

**Goal:** meet compliance, cost and regional-resilience requirements for large Log Analytics estates.

## Dedicated cluster: when
- Ingestion of **100 GB/day or more** across workspaces in a region (cluster commitment tiers start at 100 GB/day).
- Need **customer-managed keys**, Lockbox, double encryption, or availability zones for the data.
- One commitment tier shared by the workspaces linked to the cluster; cluster cost is attributed proportionately to those workspaces (default billing type), or to the cluster resource.

```bash
az monitor log-analytics cluster create -g rg -n la-cluster -l westeurope --sku-capacity 100
az monitor log-analytics workspace linked-service create -g rg --workspace-name law1 -n cluster \
  --write-access-resource-id <clusterId>
```
- Commitment tier billing starts as soon as the cluster is created, regardless of ingestion. Linking a workspace changes its billing plan to `LACluster`; other workspace and query configuration is unchanged.
- Availability zones are enabled by default on dedicated clusters in regions that support them (`isAvailabilityZonesEnabled`).
- CMK: assign the Key Vault Crypto Service Encryption User role to the cluster identity, then run `az monitor log-analytics cluster update` with `--key-vault-uri` and `--key-name` (see the customer-managed keys page for the full sequence).

## Workspace replication
- Workspace replication is a paid feature that protects against region-wide incidents; it complements availability zones.
- Enable it with a `PUT` on the workspace (REST, `api-version` from the docs page) whose body sets `properties.replication` to `{"enabled": true, "location": "<SecondaryRegion>"}`. For a workspace linked to a dedicated cluster, enable replication on the cluster first; the workspace's secondary location must match the cluster's.
- To replicate data collected with data collection rules, associate each DCR with the **workspace data collection endpoint**; such DCRs can target only that workspace.
- Switchover is a manual action: `az monitor log-analytics workspace failover` (REST: `POST .../locations/<secondaryRegion>/workspaces/<name>/failover`) and `az monitor log-analytics workspace failback` once the primary is healthy. The permissions needed are in the Monitoring Contributor built-in role.
- Tables on the Auxiliary plan are not replicated; do not enable replication on workspaces that rely on them.

## Gotchas
- Replication does not copy data ingested before it was enabled.
- Auxiliary-plan tables are not replicated and are unavailable after switchover.
- After disabling replication on every linked workspace, disable it on the cluster.
- Switchover is manual; nobody gets paged unless you alert on primary ingestion failure.

## Verify
- [ ] `az monitor log-analytics cluster show` reports the expected `sku.capacity` and key vault properties.
- [ ] Workspace `properties.replication.provisioningState` is `Succeeded`; a test switchover in non-prod returns queries from the secondary.

## Checked
2026-10-28. Confirmed on the dedicated clusters, workspace replication and customer-managed keys pages: commitment tiers start at 100 GB/day, billing from creation, `LACluster`, Lockbox, double encryption, availability zones default, role name for CMK, `cluster update --key-vault-uri/--key-name`, replication properties, cluster-first enablement, workspace DCE association, manual switchover with `workspace failover`/`failback`, Auxiliary tables unsupported, pre-enablement data not copied. Removed: 31-day minimum commitment, two link operations per 30 days, creation duration, faster cross-workspace query claim, the unlisted `az resource update` command, Data Export/Basic limitation remark, replicated-GB billing wording.
Method: documentation only; no commands were run.
