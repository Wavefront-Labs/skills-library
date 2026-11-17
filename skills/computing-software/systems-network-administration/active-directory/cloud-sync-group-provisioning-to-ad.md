---
id: computing-software.systems-network-administration.active-directory.cloud-sync-group-provisioning-to-ad
name: cloud-sync-group-provisioning-to-ad
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, cloud-sync-group-provisioning, group-writeback, security-groups, provisioning]
level: advanced
status: docs-checked
description: "Provision Entra ID cloud security groups down to AD DS with Cloud Sync group provisioning, so on-premises apps and file shares can use cloud-managed groups."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-configure-entra-to-active-directory
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-prerequisites-provision-entra-to-active-directory
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-gmsa-cmdlets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Sync group provisioning (Entra ID to AD DS)

Cloud-created security groups are written into an AD OU so Kerberos apps and NTFS ACLs can use them. Cloud Sync uses the
configuration type **Microsoft Entra ID to AD sync**; groups-only is generally available, while users-only and
users-and-groups options are in preview (Microsoft page dated 2026-08-19).

## Requirements
- Entra account with at least Hybrid Identity Administrator.
- AD schema with `msDS-ExternalDirectoryObjectId` (Windows Server 2016 or later schema).
- Provisioning agent build 1.1.2334.0 or later, on a domain-joined server (Windows Server 2025 or 2022 recommended), able
  to reach domain controllers on TCP 389 and TCP 3268 (Global Catalog lookup is needed to drop invalid memberships).
- If members come from Connect Sync, Entra Connect Sync build 2.2.8.0 or later, and synced users must have
  `onPremisesObjectIdentifier` set.
- Licensing: the first two new configurations per tenant need Entra ID P1; configurations 3 to 20 need Entra ID Governance.
  Maximum 20 configurations (domains) per tenant.
- Only members that have an AD account are written: synced users, cloud users provisioned to AD, or other cloud security
  groups. Others are skipped.

## Configure
1. Entra admin center > Entra ID > Entra Connect > Cloud sync > **New configuration** > **Microsoft Entra ID to AD sync**,
   select the domain, **Create**.
2. **Scoping filters**: scope by assignment (attribute value filters are only advised with **All users and groups**; with
   **Selected users and groups** they add processing without narrowing scope) and choose target containers.
3. **Attribute mappings**: the group defaults include `member` from `members` and `UniversalScope` = `True`.
4. Test with provision on demand, then enable.

A default clause limits groups to `securityEnabled IS TRUE AND dirSyncEnabled IS FALSE AND mailEnabled IS FALSE`
(cloud-only security groups, not mail-enabled).

The wizard assigns the agent's service account permissions on a clean install only. After an upgrade, grant them with
```powershell
Set-AADCloudSyncPermissions -PermissionType UserGroupCreateDelete -TargetDomain "<DOMAIN_FQDN>" -EACredential (Get-Credential)
```
(Enterprise Admin credential). Those rights are not applied to AdminSDHolder objects.

## Use on-premises
```powershell
Get-ADGroup -SearchBase 'OU=<TARGET_OU>,DC=ad,DC=example,DC=com' -Filter * -Properties member
```
Then grant the group on shares or app roles.

## Gotchas
- `adminDescription`, `msDS-ExternalDirectoryObjectId` and `ObjectGUID` are service-managed group mappings: do not edit
  them, and do not edit provisioned groups by hand in AD.
- A nested security group is written without its members: put every member group in scope too.
- Users must sign out and in (or get a new ticket) to see new group SIDs in their token.

## Verify
- [ ] Group exists in the OU with the right members; access works after the user gets a new token.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): configure Entra ID to AD provisioning (2026-08-19), its
prerequisites include (2026-08-07) and the agent gMSA cmdlet page. Confirmed the agent build, ports, license tiers,
permission cmdlet and the nested-group and service-managed attribute notes. Removed the old agent version 1.1.1370.0,
the unsourced default OU name, the update-timing claim and the "assigned or dynamic" claim; the cited tutorial URL no
longer exists in the repository, so the sources point to the current pages.
Method: documentation only; no commands were run.
