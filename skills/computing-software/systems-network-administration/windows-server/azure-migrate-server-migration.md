---
id: computing-software.systems-network-administration.windows-server.azure-migrate-server-migration
name: azure-migrate-server-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, workload-migration, server-migration, azure-migrate, discovery-and-assessment, replication-appliance, rehost, test-migration]
level: practitioner
status: docs-checked
description: "Rehost Windows Servers to Azure with Azure Migrate: appliance discovery, assessments and sizing, dependency analysis, replication, test migration and cutover."
sources:
  - https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview
  - https://learn.microsoft.com/en-us/azure/migrate/tutorial-migrate-vmware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate servers to Azure with Azure Migrate

## Discover and assess
1. Azure Migrate project > Discovery and assessment > deploy the **Azure Migrate
   appliance** (OVA template for VMware).
2. The appliance discovers servers and supports dependency analysis.
3. Create an **Azure VM assessment** from the discovered servers.
4. Use dependency analysis to group servers that must move together.

## Replicate
- Settings per server include target resource group, VNet/subnet, size and disks; Azure Hybrid Benefit for Windows Server licences can be applied.

## Test migration
Run a test migration into an isolated VNet, validate the application, clean up. Repeat
until it works.

## Migrate (cutover)
- Stop the application before the final replication and migrate; update DNS afterwards.

## Verify
- [ ] Each migrated server passes app tests; replication stopped and source shut down.

## Checked
2026-10-28: Confirmed on Learn pages migrate-services-overview and tutorial-migrate-vmware: Azure Migrate appliance and OVA template for VMware, dependency analysis, Azure Hybrid Benefit option during replication settings. Removed: VHD/script appliance forms, performance history durations, reserved instance and cost output, agentless/agent-based replication detail, shutdown option, post-migration checklist, Server 2008 and domain controller gotchas.
Method: documentation only; no commands were run.
