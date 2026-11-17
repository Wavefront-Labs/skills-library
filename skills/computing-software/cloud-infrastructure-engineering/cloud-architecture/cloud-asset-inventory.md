---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-asset-inventory
name: cloud-asset-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-baseline, cloud-asset-inventory, cmdb, resource-graph, aws-config]
level: practitioner
status: draft
description: "Build an asset inventory and CMDB feed from cloud APIs: AWS Config aggregator, Azure Resource Graph, Google Cloud Asset Inventory, ownership and reconciliation."
sources: ["https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html", "https://learn.microsoft.com/azure/governance/resource-graph/overview", "https://cloud.google.com/asset-inventory/docs/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset inventory and CMDB from cloud APIs

Cloud resources change too fast for manual CMDBs. Pull from provider inventory services.

## Sources
- **AWS**: Config with an organisation aggregator (advanced queries in SQL-like syntax:
  `SELECT resourceId, resourceType, tags WHERE resourceType = 'AWS::EC2::Instance'`);
  Resource Explorer for search.
- **Azure**: Resource Graph (KQL across subscriptions):
  `Resources | where type =~ 'microsoft.compute/virtualmachines' | project name, location, tags`.
- **GCP**: Cloud Asset Inventory (`gcloud asset search-all-resources --scope=organizations/ORG_ID`),
  export to BigQuery for history.

## Steps
1. **Enable org-wide collection** in every account/subscription/project and region.
2. **Define the record**: resource ID, type, account, region, owner, application, environment,
   data classification, creation time, cost (join to billing).
3. **Ownership** from tags and account mapping; report untagged/unowned resources to account owners.
4. **Sync to CMDB/ITSM** (ServiceNow Service Graph connectors exist for all three providers)
   at application/service level; do not push every ephemeral resource.
5. **Reconcile**: periodic comparison against IaC state to find unmanaged resources.

## Gotchas
- Config recording costs per configuration item; scope recording for high-churn types.
- Ephemeral resources (containers, functions) belong in the inventory at service level, not per instance.

## Verify
- [ ] Inventory covers all accounts and regions (count check).
- [ ] Unowned resources below target and trending down.
