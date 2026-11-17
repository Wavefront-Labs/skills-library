---
id: computing-software.cloud-infrastructure-engineering.azure.entra-tenant-user-settings-and-default-permissions
name: entra-tenant-user-settings-and-default-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, authorization-policy, default-user-permissions, guest-access, app-registration, user-consent]
level: practitioner
status: docs-checked
description: "Harden Entra ID tenant-wide user settings: app registration, tenant and group creation, guest access level, who can invite, and user consent via authorizationPolicy."
sources: ["https://learn.microsoft.com/entra/fundamentals/users-default-permissions", "https://learn.microsoft.com/graph/api/resources/authorizationpolicy", "https://learn.microsoft.com/graph/api/resources/defaultuserrolepermissions", "https://learn.microsoft.com/entra/external-id/external-collaboration-settings-configure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra tenant user settings and default permissions

**Goal:** reduce what an ordinary member or guest can do by default, one of the first hardening steps
in any tenant review.

## Read the current state
```bash
az rest --method GET --url https://graph.microsoft.com/v1.0/policies/authorizationPolicy
```
Key properties:
| Property | Hardened value | Effect |
|---|---|---|
| `defaultUserRolePermissions.allowedToCreateApps` | false | Members cannot register apps (use a governed request process) |
| `defaultUserRolePermissions.allowedToCreateSecurityGroups` | false | Members cannot create security groups |
| `defaultUserRolePermissions.allowedToCreateTenants` | false | Members cannot create tenants |
| `defaultUserRolePermissions.allowedToReadOtherUsers` | usually leave true | Whether members can read other users; setting false can break apps, test first |
| `allowInvitesFrom` | `adminsAndGuestInviters` | Only Global Administrator, User Administrator and Guest Inviter roles invite guests. Other values: `none`, `adminsGuestInvitersAndAllMembers`, `everyone` |
| `guestUserRoleId` | Restricted Guest User template ID | Role granted to guests: User, Guest User or Restricted Guest User (template IDs are in the authorizationPolicy page) |
| `defaultUserRolePermissions.permissionGrantPoliciesAssigned` | empty, or a restrictive consent policy | Whether and under which app consent policy users can consent |

`allowedToUseSSPR` is documented as whether tenant **administrators** can use self-service password reset, not members.

```bash
az rest --method PATCH --url https://graph.microsoft.com/v1.0/policies/authorizationPolicy \
  --headers Content-Type=application/json \
  --body '{"allowInvitesFrom":"adminsAndGuestInviters","defaultUserRolePermissions":{"allowedToCreateApps":false,"allowedToCreateSecurityGroups":false,"allowedToCreateTenants":false}}'
```
Required permission: `Policy.ReadWrite.Authorization`.

## User consent
- `permissionGrantPoliciesAssigned` controls whether users may consent to apps and which permission grant policy
  applies. Pair a restrictive setting with an admin consent workflow so users can request apps.

## Guests
- Guest user access levels in external collaboration settings: same access as members; limited access to properties and
  memberships of directory objects (the default, blocks enumerating users and groups); or access restricted to their
  own profile (most restrictive). The most restrictive is the hardened choice.
- External collaboration settings also hold who can invite and domain allow/deny lists for invitations.

## Gotchas
- "Restrict access to Microsoft Entra administration portal" limits a set of commonly visited admin center pages;
  it is not a security boundary against Graph or PowerShell. Treat it as a convenience setting.
- With app registration off, grant the Application Developer role to the people who need it.
- Setting `allowedToReadOtherUsers` is done by updating authorizationPolicy through Graph; test pickers before rollout.

## Verify
- [ ] GET authorizationPolicy reflects the hardened values.
- [ ] A test member account is refused when registering an app; a guest cannot list users.

## Checked
2026-10-27. Confirmed against Learn "Default user permissions", Graph resources authorizationPolicy and
defaultUserRolePermissions, authorizationPolicy update (PATCH, `Policy.ReadWrite.Authorization`) and "Configure external
collaboration settings". Fixed: `allowedToUseSSPR` was described as member SSPR (documented as administrators). Removed:
the `microsoft-user-default-low` policy ID, portal consent navigation, cross-tenant access (B2B direct connect and
MFA/device trust) statements, and the claim that the portal restriction "only hides" the portal (the docs say it limits
a set of pages).
Method: documentation only; no commands were run.
