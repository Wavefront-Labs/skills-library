---
id: computing-software.cloud-infrastructure-engineering.azure.site-recovery-test-failover-drills
name: site-recovery-test-failover-drills
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, site-recovery, asr-test-failover, test-failover-network, dr-drill, recovery-plans]
level: advanced
status: docs-checked
description: "Run Azure Site Recovery test failovers in an isolated network, validate apps, clean up, and record RTO evidence without affecting replication."
sources: ["https://learn.microsoft.com/azure/site-recovery/azure-to-azure-tutorial-dr-drill", "https://learn.microsoft.com/azure/site-recovery/site-recovery-test-failover-to-azure", "https://learn.microsoft.com/azure/site-recovery/site-recovery-create-recovery-plans"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site Recovery test failover drills

**Goal:** prove DR works on a schedule without touching production or replication.

## Design the test network
- A dedicated **isolated VNet** in the target region (Microsoft recommends a network isolated from the production recovery network; a new VNet is isolated by default) that mimics production.
- Add a test domain controller/DNS: fail over a DC replica in the same recovery plan or restore one into the test VNet; otherwise apps fail on auth.
- Bastion in the test VNet for access.
- Set the test network per replicated item: Compute and Network → *Test failover network*, or pick at test time.

## Run
1. Pick a recovery point: **Latest processed**, **Latest app-consistent**, or a specific one.
2. Run on the **recovery plan** (preferred, applies boot order, scripts and runbooks):
Choose the test network when you start the test failover.
3. Validate: app smoke tests, data freshness (compare last transaction time), dependencies, DNS.
4. **Clean up**: *Cleanup test failover* deletes the VMs created during the test; add notes on results.

## Measure
- RTO = time from start of the job to application validated; RPO = now minus timestamp of chosen recovery point.
- Keep job IDs, timings and validation evidence for audit.

## Gotchas
- Leave no test VMs running: run cleanup after each drill.
- Using the production DR VNet for tests risks IP conflicts and duplicate machines joining the domain.
- Repeat drills on a schedule and after major changes.

## Verify
- [ ] Recovery plan test job `Succeeded`, cleanup done, drill report filed with RTO/RPO numbers.

## Checked

2026-10-28. Confirmed on the Site Recovery DR drill and test failover pages: recovery point choices Latest processed and Latest app-consistent, Cleanup test failover deletes the VMs created, an isolated test network is recommended and should mimic production. Removed: PowerShell cmdlet names and the sample, the same-address-space and no-peering specifics, audit standard names, the replication and public IP claims and the twice-a-year frequency.

Method: documentation only; no commands were run.
