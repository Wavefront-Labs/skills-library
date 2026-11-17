---
id: computing-software.systems-network-administration.windows-server.asr-recovery-plans-and-test-failover
name: asr-recovery-plans-and-test-failover
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-site-recovery, asr, recovery-plans, test-failover, failover-groups, automation-runbook, dr-drill]
level: advanced
status: docs-checked
description: "Build ASR recovery plans with ordered groups, scripts and manual actions, run test failovers in an isolated VNet, clean up and execute planned or unplanned failover."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-create-recovery-plans
  - https://learn.microsoft.com/en-us/azure/site-recovery/recovery-plan-overview
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-failover
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-active-directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASR recovery plans and test failovers

## Recovery plan design
- Machines in one group fail over in parallel; groups start in order (Group 2 only after all of Group 1 has failed
  over and started). Typical tiers: infrastructure, databases, app, web.
- Pre and post actions per group: Azure Automation runbooks or scripts (attach public IP, update DNS, change a load
  balancer, NSG on a NIC) and manual actions that pause the plan for acknowledgement.
- One plan per application. A plan holds up to 100 protected instances. Run a test failover for each app every
  quarter so the plan stays current.

## Test failover
Vault > Recovery Plans > plan > Test failover:
- Recovery point: Latest processed (low RTO), Latest app-consistent, Latest (processes pending data first, lowest
  RPO), Latest multi-VM processed, Latest multi-VM app-consistent (plans with multi-VM consistency), Custom (single VM).
- Azure virtual network: a network isolated from production (a new Azure VNet is isolated by default). It should
  mimic production: same subnet names and count, same IP range, DNS pointing at the DNS VM's target IP.
- Validate the app, then **Cleanup test failover**; this deletes the VMs created by the test.

PowerShell (Az.RecoveryServices):
```powershell
$rp = Get-AzRecoveryServicesAsrRecoveryPlan -Name 'App-Finance'
Start-AzRecoveryServicesAsrTestFailoverJob -RecoveryPlan $rp -Direction PrimaryToRecovery -AzureVMNetworkId $testVnet.Id
Start-AzRecoveryServicesAsrTestFailoverCleanupJob -RecoveryPlan $rp -Comment 'Q4 DR test OK'
```

## Real failover
- **Planned** failover is documented for Hyper-V VMs: source VMs shut down, latest data syncs, no data loss.
- **Unplanned**: choose a recovery point and optionally shut down source machines first. After failover **Commit**
  (deletes the other recovery points), then re-protect toward the source and fail back later.

## Domain controllers in DR
Few apps and one DC: replicate the DC with Site Recovery. For a test, replicate a DC/DNS VM and test-fail it over
into the isolated network first (using its latest app-consistent point) before the app plan. Do not include all DCs
in the test network; you may need to seize FSMO roles and clean up metadata there. Make such changes only on a DC
dedicated to testing, never connect it to production.

## Verify
- [ ] Test failover recorded each quarter with achieved RTO and RPO.

## Checked
Date 2026-10-27. Documentation: recovery plan overview, test failover to Azure, failover, Active Directory pages and
Az.RecoveryServices cmdlet references (Start-AzRecoveryServicesAsrTestFailoverJob, cleanup job, Get recovery plan).
Confirmed: group semantics, 100-instance limit, recovery point options, isolated network requirements, cleanup
behaviour, cmdlet parameters, planned failover scope, DC test guidance.
Method: documentation only; no commands were run.
