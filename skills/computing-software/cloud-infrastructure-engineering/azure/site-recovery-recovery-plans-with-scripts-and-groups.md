---
id: computing-software.cloud-infrastructure-engineering.azure.site-recovery-recovery-plans-with-scripts-and-groups
name: site-recovery-recovery-plans-with-scripts-and-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, site-recovery, asr, recovery-plans, recovery-plan-scripts, automation-runbooks, manual-actions, failover-orchestration, recoveryplancontext, dns-cutover, dr-runbook]
level: advanced
status: docs-checked
description: "Build ASR recovery plans: ordered VM groups, pre/post Automation runbooks using RecoveryPlanContext, manual actions, and test/planned/unplanned failover of the whole plan."
sources: ["https://learn.microsoft.com/en-us/azure/site-recovery/recovery-plan-overview", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-create-recovery-plans", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-runbook-automation", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site Recovery recovery plans — orchestrated failover in application order

**Goal:** one click (or one API call) fails over an entire application tier-by-tier, runs the
fix-ups that turn booted VMs into a working service, and pauses where a human must decide.

## 1. Structure
- A recovery plan gathers machines into recovery groups for failover; a machine can belong to only one group in a plan. Use one plan per application boundary.
- **Groups** boot in order (Group 1 → 2 → …).
  Typical: Group 1 domain controllers/DNS or databases, Group 2 app tier, Group 3 web/front-end.
- Each group can have **pre-steps** and **post-steps**: Azure Automation runbooks (when failing over to Azure), scripts, or **manual actions** that pause the plan.

## 2. Create
Vault → *Recovery Plans* → *+ Recovery plan* → source/target, deployment model → select items.
Then *Customize*: add groups, move VMs, *Add pre action / Add post action*.

## 3. Runbooks that receive the plan context
Automation account (target region, system-assigned identity with rights on the target RGs,
DNS zone, LB, Traffic Manager). The plan passes `RecoveryPlanContext`:
```powershell
param([parameter(Mandatory=$false)][Object]$RecoveryPlanContext)
Connect-AzAccount -Identity | Out-Null
# $RecoveryPlanContext.FailoverType says whether this is a test or production failover;
# $RecoveryPlanContext.FailoverDirection says primary or secondary location.
# Branch on FailoverType so drills do not change production DNS (see the context variable table for its values).
```
Common post-actions: add VMs to target LB pools/App Gateway, update private DNS or Traffic Manager
endpoint priority, re-point connection strings, attach public IPs, run smoke tests and post a
Teams message. Make every script **idempotent** and branch on `FailoverType` so drills don't touch prod DNS.

## 4. Run the plan
- **Test failover** of the plan into an isolated VNet → check app → *Cleanup test failover* with notes.
- For a real failover use the recovery plan's failover action, then follow the vault's re-protect and failback articles.

## Gotchas
- Runbooks can fail if the Automation identity lacks rights in the *target* region resources.
- Manual actions block the whole plan until acknowledged; name them with an explicit check ("Confirm DB accepts writes").
- Scripts must be in an Automation account the plan can reach during a regional outage — host it in the target region.

## Verify
- [ ] Plan groups reflect the app's dependency order and contain every replicated VM of the app.
- [ ] A test failover runs all runbooks successfully (job log green) without changing production DNS.
- [ ] Measured end-to-end time from the job is within the RTO and recorded in the DR runbook.

## Checked
2026-10-28. Confirmed on the recovery plan overview and runbook automation pages: groups, scripts and Azure Automation runbooks, manual action pauses, the plan passes only the `RecoveryPlanContext` parameter with `FailoverType` (test or production) and `FailoverDirection`, test failover into an isolated network then Cleanup test failover with notes.
Removed (not confirmed): the 100-VM limit, one-vault/direction rule, group parallel start, the `New-/Edit-AzRecoveryServicesAsrRecoveryPlan` cmdlets, RecoveryPlanContext value strings and VmMap properties, the planned/unplanned/commit/re-protect steps, job-view duration claim and plan-membership gotcha.

Method: documentation only; no commands were run.
