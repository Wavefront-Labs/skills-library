---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.server-replication
name: server-replication
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-execution, server-replication, rehost, aws-application-migration-service, azure-migrate-server-migration, migrate-to-virtual-machines, block-level-replication]
level: practitioner
status: draft
description: "Rehost servers with block-level replication tools (AWS MGN, Azure Migrate, Google Migrate to VMs): agents, staging, test launches, cutover and cleanup."
sources: ["https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html", "https://learn.microsoft.com/azure/migrate/migrate-services-overview", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/getting-started"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Block-level server replication rehost

## Flow (common to the tools)
1. **Install** replication agent (or agentless via vCenter for VMware) on source servers.
2. **Initial sync** of disks to a staging area in the target (low-cost replication servers and
   volumes), then continuous block-level replication.
3. **Launch settings**: target instance type, subnet, security groups, licence, post-launch
   actions (install cloud agents, remove VMware tools).
4. **Test launch**: boot a test instance in an isolated subnet; app owner validates.
5. **Cutover launch**: stop app writes on source, wait for replication lag to reach zero, launch
   cutover instances, switch DNS/traffic.
6. **Finalise**: mark cutover complete, stop replication, archive source, clean staging.

## Prerequisites
- Network: source to staging subnet over TCP 443 (control) and the tool's replication port
  (AWS MGN TCP 1500) via VPN/Direct Connect or internet with encryption.
- Bandwidth estimate: initial sync size / available bandwidth; throttle during business hours.
- IAM roles for the service; target landing zone ready.

## Gotchas
- High-churn disks (databases) may never catch up over thin links; use native DB replication.
- Test launches with production IPs/hostnames cause conflicts; isolate test subnets.
- Drivers: Windows needs appropriate network/storage drivers for target hypervisor (tools inject
  them, but check old OS).
- Forgetting to stop replication and delete staging resources costs money.

## Verify
- [ ] Test launch validated by app owner before scheduling cutover.
- [ ] Replication lag near zero at cutover; data validation checks pass.
