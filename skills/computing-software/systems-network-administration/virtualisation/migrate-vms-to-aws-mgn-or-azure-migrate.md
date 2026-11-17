---
id: computing-software.systems-network-administration.virtualisation.migrate-vms-to-aws-mgn-or-azure-migrate
name: migrate-vms-to-aws-mgn-or-azure-migrate
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [aws-mgn, azure-migrate, v2v, cloud-migration, rehost]
level: practitioner
status: gated
description: "Rehost on-premises VMware, Hyper-V or physical servers to Azure with Azure Migrate (appliance, replication, test migration, cutover) or to AWS with MGN."
sources:
  - https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview
  - https://learn.microsoft.com/en-us/azure/migrate/migrate-replication-appliance
  - https://learn.microsoft.com/en-us/azure/migrate/tutorial-migrate-hyper-v
  - https://learn.microsoft.com/en-us/azure/migrate/tutorial-migrate-vmware
  - https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration to AWS or Azure with MGN or Azure Migrate

**Goal:** lift-and-shift servers into the cloud with continuous replication and a short cutover.

## Azure Migrate
1. Create an Azure Migrate project. Deploy the **appliance** for discovery and assessment: a template for VMware
   (OVA) or Hyper-V (VHD), or a PowerShell installer script (for VMware or Hyper-V without a template, Azure
   Government, and always for physical or other-cloud servers).
2. **Assess**: sizing, cost and readiness.
3. **Replicate**:
   - VMware: **agentless** (uses the same appliance as discovery) or **agent-based**. Agent-based uses a replication
     appliance (OVA for VMware, or a downloaded installer on a physical server) and the Mobility service on each
     machine.
   - Hyper-V: install the **Hyper-V Replication provider** on the hosts with the downloaded registration key.
   - Physical and other-cloud servers: agent-based.
   - Initial replication creates a VM snapshot and copies the disk data to replica managed disks in Azure; delta
     replication follows.
4. **Test migration** (recommended at least once per machine, once delta replication begins): creates an Azure VM
   from replicated data, preferably in a non-production virtual network; the source stays running. Clean up the
   test resources afterwards.
5. **Migrate**: choose whether to shut the source VM down for a planned migration with no data loss; then select
   **Complete migration** to clean up migration resources. **Stop replication** and **Start replication** are
   available while replicating.

Agent-based replication ports (replication appliance): HTTPS 443 inbound from the machines for management, HTTPS
9443 inbound for replication data (the data port can be changed), and 443 outbound to Azure.

## AWS Application Migration Service (MGN)
Microsoft cannot document this; the AWS user guide is the source, and it was not readable for this review. These
steps summarise the usual flow and are unconfirmed:
1. Initialise MGN in the target region and configure the replication settings template (gated: unconfirmed, source is paywalled or blocked).
2. Install the replication agent on each source server with suitable AWS credentials (gated: unconfirmed, source is paywalled or blocked).
3. Source servers need outbound HTTPS 443 to the service endpoints and TCP 1500 to the replication servers (gated: unconfirmed, source is paywalled or blocked).
4. Configure the launch template per server, run a test launch, then a cutover launch and finalise the cutover
   (gated: unconfirmed, source is paywalled or blocked).
Confirm every port, installer name and step against the current AWS Application Migration Service user guide.

## Common gotchas
- Check each tool's list of supported operating systems and boot requirements before choosing a method.
- Licensing for Windows and SQL Server differs per cloud: check each provider's current terms.
- Plan bandwidth: initial replication of large disks can take a long time.

## Verify
Test instances boot, pass application tests, and resolve dependencies (DNS, AD, databases) from the cloud network
before the cutover is scheduled.

## Checked

Date checked: 2026-10-27. Documentation: Azure Migrate overview, replication appliance and Hyper-V and VMware migration tutorials (azure-docs main branch, 2026).
Confirmed for Azure Migrate: appliance deployment methods; agentless versus agent-based VMware; replication provider for Hyper-V; snapshot-based initial replication; test migration and complete migration steps; replication appliance ports 443 and 9443. AWS MGN details are marked as gated because the AWS documentation could not be read.

Method: documentation only; no commands were run.
