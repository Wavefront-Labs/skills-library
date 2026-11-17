---
id: computing-software.systems-network-administration.active-directory.cloud-sync-vs-connect-sync
name: cloud-sync-vs-connect-sync
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, cloud-sync, cloud-sync-vs-connect-sync, entra-connect, coexistence, migration, multi-forest, device-writeback, exchange-hybrid]
level: practitioner
status: docs-checked
description: "Choose between Entra Cloud Sync and Connect Sync, run both side by side on disjoint scopes, and migrate pilot OUs from Connect Sync to Cloud Sync safely."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/connect-to-cloud-sync-decision-guide#comparison-between-microsoft-entra-connect-and-cloud-sync
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/tutorial-pilot-aadc-aadccp
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Sync vs Connect Sync

## Decide (use the current comparison table; it changes)
Microsoft describes Cloud Sync as the strategic direction and says new sync features are developed there first.
From the Microsoft decision guide:
- Cloud Sync only: disconnected forests, multiple active agents with automatic failover, group provisioning to AD,
  on-demand provisioning, cloud-managed configuration.
- Connect Sync only: pass-through authentication configuration and AD FS setup (PTA and Seamless SSO keep working after
  a migration), advanced sync rules, full attribute-based filtering (Cloud Sync is limited), device writeback, cross-forest
  references, merging attributes across domains and reconciliation.
- Both: users, groups and contacts, password hash sync, password writeback, Exchange hybrid attributes, directory
  extensions, device synchronization (enabled separately in Cloud Sync), Seamless SSO.
- Scale: Cloud Sync supports up to 150,000 objects per domain and groups up to 50,000 members; Connect lists 250,000
  members for groups.
- Neither provisions users from the cloud to AD in GA; user provisioning to AD is in preview.

## Coexistence
Both engines can export to one tenant, but an object must not be managed by both. The Microsoft pilot procedure keeps the
pilot objects in Connect Sync scope and stops Connect from exporting them with a `cloudNoFlow` inbound rule and a
`JoinNoFlow` outbound rule. Do not exclude the pilot OU from Connect: removing objects from Connect scope removes them
from the connector spaces and metaverse and can export reference deletes such as group membership removals.
Objects need `ms-ds-consistencyGUID` populated so Cloud Sync hard-matches them; Connect does not populate it by default
for group objects. Connect Sync must be version 1.4.32.0 or later.

## Pilot migration (per Microsoft tutorial)
1. On the Connect server run `Set-ADSyncScheduler -SyncCycleEnabled $false`.
2. In the Synchronization Rules Editor create an inbound rule per object type (user, group, contact) that sets
   `cloudNoFlow` to `True` for the pilot OU or group, with a unique precedence.
3. Create the matching outbound rule with link type `JoinNoFlow` scoped to `cloudNoFlow` = `True`.
4. Install the provisioning agent, create a Cloud Sync configuration scoped to the pilot OU and enable it.
5. Run `Set-ADSyncScheduler -SyncCycleEnabled $true` and `Start-ADSyncSyncCycle`. Connect then stops exporting adds,
   deletes and non-reference attribute updates for those objects (reference attributes such as `member` and `manager`
   can still flow).
6. Check pilot users with provision on demand. Repeat for more OUs.

## Verify
- [ ] No object is managed by both engines; no unexpected deletes in the Entra audit logs.
- [ ] Pilot users' changes in AD reach Entra through Cloud Sync.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Cloud Sync decision guide comparison table, what-is-cloud-sync
and the Connect-to-Cloud-Sync pilot tutorial. Corrected: device synchronization is now supported by Cloud Sync, and the
pilot keeps objects in Connect scope with `cloudNoFlow` and `JoinNoFlow` rules instead of excluding the OU. The
comparison table moved to the decision-guide page; sources updated.
Method: documentation only; no commands were run.
