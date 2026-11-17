---
id: computing-software.cloud-infrastructure-engineering.azure.hybrid-identity-entra-connect
name: hybrid-identity-entra-connect
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, hybrid-identity, entra-connect, entra-connect-sync, cloud-sync, password-hash-sync, phs, pass-through-authentication, pta, seamless-sso, federation, adfs, staging-mode, ou-filtering, password-writeback, device-writeback, hybrid-join, synchronization-rules, sourceanchor, ms-ds-consistencyguid, entra-connect-health]
level: advanced
status: docs-checked
description: "Design and run hybrid identity: PHS, PTA or federation, Connect Sync versus Cloud Sync, sourceAnchor, staging mode, sync cycle, deletion threshold and sync errors."
sources: ["https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-design-concepts", "https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-staging-server", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-scheduler", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-prevent-accidental-deletes", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sso-faq", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/tshoot-connect-sync-errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid identity — sync on-prem AD to Entra ID without locking yourself in

**Goal:** one identity per human, cloud auth that survives an on-prem outage, and a sync
server you can rebuild from notes.

## 1. Pick the authentication method
Read "Choose the right authentication method" first; it compares the options and their
requirements. In outline:
- **Password hash sync (PHS)**: validation happens in the cloud, so it keeps working when AD is unavailable.
- **Pass-through authentication (PTA)**: passwords are validated on-prem by authentication
  agents; for most customers three agents in total are sufficient for availability and
  capacity, installed close to domain controllers.
- **Federation (AD FS)**: needed for scenarios such as certificate and smart-card authentication
  that the cloud methods do not cover (see the comparison table); costly to run.
- **Seamless SSO** creates the `AZUREADSSO` computer account in each forest. Roll over its
  Kerberos decryption key at least every 30 days with `Update-AzureADSSOForest`, and run that
  command only once per forest per roll-over or the feature stops working until tickets expire.

## 2. Connect Sync vs Cloud Sync
- **Entra Connect Sync** runs on an on-premises server (a second server can sit in staging mode).
- **Cloud Sync** uses lightweight provisioning agents (outbound connections only, cloud
  managed config, multiple agents for high availability, a service sync interval of two
  minutes) and natively handles multiple disconnected forests; it also supports group
  provisioning to AD and, with device sync enabled, computer objects for hybrid join.
- See the Cloud Sync / Connect feature comparison table before choosing; use Connect Sync
  where Cloud Sync lacks a feature you need.

## 3. Deploy Connect Sync properly
1. Run **IdFix** on AD first; it finds duplicates and formatting problems before sync.
2. **sourceAnchor**: `objectGUID` is the default and fine for a single forest or for
   multiple forests where users never move. If users move between forests or domains, use
   `ms-DS-ConsistencyGuid`, which Connect fills from `objectGUID` when empty. The value can
   only be set at initial installation; changing it later means uninstall and reinstall, and
   every additional Connect server must use the same attribute.
3. Build a second server in **staging mode** for standby. Only one sync server may be syncing
   changes at any time; if the active one is unreachable, make sure it cannot come back
   unexpectedly when you promote the other.
4. The default sync cycle is every 30 minutes; trigger one with
   `Start-ADSyncSyncCycle -PolicyType Delta` (`Initial` for a full sync cycle).
5. Protect the sync service account like a privileged account.

## 4. Troubleshooting
- Synchronization Service Manager shows run results and export errors; the troubleshooting
  page documents each, including `AttributeValueMustBeUnique`, `InvalidSoftMatch` and `LargeObject`.
- **Prevent accidental deletes** is on by default and blocks an export with more than 500
  deletes. After you verify the deletes are intended, run
  `Disable-ADSyncExportDeletionThreshold` for the run, then restore protection with
  `Enable-ADSyncExportDeletionThreshold -DeletionThreshold 500`.
- Entra Connect Health monitors sync health (see the choose-authentication page for its role).

## Gotchas
- Decide `sourceAnchor` once (see above).
- Cloud values for attributes mastered on-prem are overwritten by the next sync.
- A UPN suffix not verified in the tenant is a classic sync problem; IdFix and the sync
  errors page cover it.
- Switching an Entra Connect server to active while another is still active disrupts Password
  Writeback on the other, because only one active server can use it.

## Verify
- [ ] Entra admin center shows a recent sync and no export errors.
- [ ] The staging server completes import and sync cycles and exports nothing it should not.
- [ ] Break-glass cloud-only admins exist and are excluded from sync and Conditional Access.

## Checked
2026-10-28. Confirmed against the choose-authentication, design-concepts (sourceAnchor), Cloud Sync,
staging server, scheduler, prevent-accidental-deletes, SSO FAQ and sync-errors pages: three PTA
agents, `AZUREADSSO` and its 30-day key roll-over, sourceAnchor rules, 30-minute cycle and
cmdlets, 500-delete threshold and cmdlets, Cloud Sync two-minute interval and disconnected forests.
Removed as unconfirmed: PHS two-minute interval, PTA and PHS side effects, licence requirements,
the writeback permission list and cmdlets, `MSOL_` account rights, device writeback cmdlets,
the soft-match procedure, group writeback retirement, `Set-MsolDirSyncEnabled` timing,
Get-ADSync object cmdlets, and the Cloud Sync versus Connect capability table.
Method: documentation only; no commands were run.
