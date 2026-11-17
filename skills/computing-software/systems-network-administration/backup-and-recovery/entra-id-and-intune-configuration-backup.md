---
id: computing-software.systems-network-administration.backup-and-recovery.entra-id-and-intune-configuration-backup
name: entra-id-and-intune-configuration-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [entra-id-backup, saas-backup, microsoft-365-backup, intune, conditional-access, microsoft-graph]
level: advanced
status: docs-checked
description: "Back up Entra ID and Intune configuration (conditional access, apps, groups, device policies) with Graph exports or tools, given native soft-delete limits."
sources:
  - https://learn.microsoft.com/en-us/entra/architecture/recoverability-overview
  - https://github.com/microsoft/EntraExporter
  - https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention
  - https://learn.microsoft.com/en-us/graph/api/conditionalaccessroot-list-policies
  - https://learn.microsoft.com/en-us/graph/api/intune-deviceconfigv2-devicemanagementconfigurationpolicy-list
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra ID and Intune configuration backup

Microsoft runs the service, but recoverability is a shared responsibility: your tenant
configuration is yours. An admin mistake, malicious deletion or a bad automation run can
wipe conditional access policies or device configs.

## What native features cover
| Object | Native recovery |
|---|---|
| Users, Microsoft 365 groups, cloud security groups, applications | soft delete into the Entra recycle bin; hard-deleted automatically after **30 days** unless restored |
| All other object types | hard deleted immediately, cannot be recovered; re-create and reconfigure |
| Misconfigurations (in-place edits) | not recycle-binned; for object types Microsoft Entra Backup and Recovery supports, difference reports and recovery jobs can roll back; otherwise reapply your documented known-good state |

Check Microsoft's "Recover from deletions" page for the current table of soft-deletable
types before relying on any other type (including Conditional Access policies and Intune
objects) being recoverable.

Audit log retention is 7 days on Entra ID Free and 30 days on P1 and P2. Route logs to an
Azure storage account via Azure Monitor (or Sentinel) to keep them longer.

## Export known-good state
Microsoft recommends documenting tenant state in an external versioned repository (for
example Azure DevOps or GitHub) with enough retention, using one of:
- Tenant configuration management (TCM) snapshot APIs in Microsoft Graph: cover a subset of
  Entra, Intune and Exchange Online resources; the tenant keeps snapshots for seven days, so
  download them. Keep TCM exports separate from direct Graph exports: TCM scope is limited.
- Microsoft Graph APIs directly, for objects TCM does not cover.
- The open-source Microsoft Entra Exporter PowerShell module, or non-Microsoft
  configuration-as-code tools. The EntraExporter repository is marked archived (read-only)
  on GitHub, so check its status before adopting it.

Settings in the legacy multifactor authentication portal for Application Proxy and
federation might not be exported by the Exporter or Graph. Store exports securely with a
limited set of admins.

## Graph examples
Conditional Access policies: `GET https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies`
(PowerShell `Get-MgIdentityConditionalAccessPolicy`), permission `Policy.Read.All`.

Intune settings catalog policies: `GET https://graph.microsoft.com/beta/deviceManagement/configurationPolicies`,
permission `DeviceManagementConfiguration.Read.All` (a read-only option listed on the
page). Intune `/beta` APIs are supported but change more often; Microsoft recommends v1.0
where available. Use an app registration with read-only permissions and app-only
authentication, and look up each other object's permission on its Graph API page.

Write each export as JSON into a dated folder and commit to a private Git repo for change
history.

## Restore considerations
- Recreated objects get new IDs, so references (CA policies targeting groups, app
  assignments) must be remapped. Map dependencies before you need them: deleting a group
  used for app assignment locks its members out of the app.
- Rehearse restoration of each object type with test objects, ideally in a test tenant, and
  predefine communications.

## Gotchas
- Store the backup app's credentials (certificate) outside the tenant you protect.
- Pin module versions and test exports regularly, especially against beta endpoints.

## Verify
A scheduled export job succeeds and commits diffs; periodically re-create a deleted CA policy
and an Intune profile in a test tenant from the export.

## Checked
2026-11-08. Confirmed against the Entra recoverability page (read in full), Entra data retention page, Graph CA policy list and Intune configurationPolicies list pages, and the EntraExporter repository page. Corrected: cloud security groups are soft deleted, audit retention is 7 days on Free, Conditional Access soft delete was not supported by the cited pages (removed), EntraExporter is archived. Removed unconfirmed claims about IntuneManagement, Microsoft365DSC ID mapping, Intune having no recycle bin, and a list of Graph permissions and `$expand` use.
Method: documentation only; no commands were run.
