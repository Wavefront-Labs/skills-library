---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migration-cutover-runbook
name: migration-cutover-runbook
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, migration-planning, migration-runbook, cutover-runbook, rollback, go-live]
level: advanced
status: docs-checked
description: "Write and run a cutover runbook for Migrate to Virtual Machines: test-clones, window, final replication, traffic switch, go/no-go, rollback, finalize."
sources: ["https://docs.cloud.google.com/migrate/virtual-machines/docs/5.0/discover/lifecycle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration cutover runbook

Built around the Migrate to Virtual Machines lifecycle: replication, optional test-clone, cut-over, finalize. Everything the tool does is from Google's lifecycle page; the surrounding runbook structure (owners, triggers, comms) is your own design and the thresholds below are examples to replace.

## 1. Before the window
- **Test-clone** each VM in the wave. A test-clone is created from the latest replication data with the current target details, can be made any time after the first replication step finishes, and does not touch the running source. It is a static snapshot: later replication data and target changes only apply to new test-clones. Run it in a sandbox isolated from the source VM, because the source is still running. Testing is optional but strongly recommended; app owners sign off functional tests.
- Delete test-clone instances when testing ends: they keep billing until you delete them, and finalize does not remove them.
- Pick the maintenance window in advance: cut-over includes a short VM downtime and the page says to schedule it in a maintenance window.
- Decide how you will redirect traffic to the migrated VM and back (DNS, load balancer, firewall). Lowering DNS TTLs ahead of time is a common choice; set the value yourself.
- Comms plan: stakeholders, status channel, on-call for each tier.

## 2. Runbook table (template)
| Step | Owner | Action | Check | Rollback |
|---|---|---|---|---|
| 1 Announce start | lead | status post | | |
| 2 Stop app writes | app | maintenance page | no writes in logs | lift page |
| 3 Cut-over | infra | the tool shuts down the source VM, completes (or starts) the final replication, stops replication, then creates the Compute Engine instance from the final data | instance created | below |
| 4 Redirect traffic | net | DNS or load balancer change | clients reach the new VM | revert change |
| 5 Validate | app | smoke tests, synthetic checks, data checks | pass | go to rollback |
| 6 Go/no-go | lead | decision recorded | | |

Because replication runs continuously, the final replication should involve a relatively small amount of data.

## 3. Failure and rollback (per the lifecycle page)
- **Cut-over fails** (for example a network issue): the source VM stays stopped and the final replication data stays valid; retry the cut-over.
- **Cut-over succeeds but the new instance malfunctions:** delete the Compute Engine VM and start the source VM. Rollback is not automated, you redirect traffic back yourself, and data written to the new instance is not copied back. After fixing the cause, restart replication and retry.
- Write go/no-go and rollback triggers before the window, with your own numbers (example: "smoke tests still failing after a set time-box", "data mismatch in critical tables", "latency worse than baseline for an agreed period"). Include a hard stop time for rollback.

## 4. After
- **Finalize** only for VMs in the Cut-Over state and only once the migrated VM is confirmed working: it deletes all replication data and other storage tied to the VM and sets the state to Finalized. After it, you can only delete the migration or add/remove the VM from a group, and rollback is no longer possible from replication data. Replication data is kept until you finalize, so storage is billed until then.
- Hypercare with owners on call, compare service levels with pre-migration, update inventory, check cost.

## Gotchas
- Hard-coded IPs and hostnames in clients, firewalls and partner allowlists break silently: inventory them during discovery.

## Verify
- [ ] Runbook rehearsed on a test-clone; every step has an owner, check and rollback; post-cutover validation signed off before finalize.

## Checked
Checked 2026-11-08 against the Migrate to Virtual Machines 5.0 "VM migration process" (lifecycle) page for test-clone, cut-over and finalize behaviour, downtime, rollback and billing. Removed: Database Migration Service test promote and replication-delay steps, specific DNS TTL value, restart-source-VM-as-rollback for all cases, and the cited "migration-to-gcp-deploying-your-workloads" page, which has no cutover guidance. Also removed the chkdsk-on-first-boot note (unread troubleshooting page).
Method: documentation only; no commands were run.
