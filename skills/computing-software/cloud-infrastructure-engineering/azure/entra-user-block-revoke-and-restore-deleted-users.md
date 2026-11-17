---
id: computing-software.cloud-infrastructure-engineering.azure.entra-user-block-revoke-and-restore-deleted-users
name: entra-user-block-revoke-and-restore-deleted-users
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, user-lifecycle, revoke-sessions, soft-delete, restore-user, hybrid-sync]
level: practitioner
status: docs-checked
description: "Run the Entra ID user lifecycle: block sign-in and revoke sessions for leavers, soft-delete, restore within 30 days or hard-delete, and handle synced users."
sources: ["https://learn.microsoft.com/entra/fundamentals/users-restore", "https://learn.microsoft.com/entra/identity/users/users-revoke-access", "https://learn.microsoft.com/graph/api/directory-deleteditems-restore", "https://learn.microsoft.com/cli/azure/ad/user"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra user lifecycle: block, revoke, delete, restore

**Goal:** cut a leaver off quickly, keep the account recoverable, and bring back a wrongly deleted user.

## Leaver: block then revoke (order matters)
```bash
# 1. block new sign-ins
az ad user update --id user@contoso.com --account-enabled false
```
```powershell
# 2. revoke refresh tokens / session cookies (forces re-authentication, which now fails)
Connect-MgGraph -Scopes User.ReadWrite.All
Update-MgUser -UserId user@contoso.com -AccountEnabled:$false
Revoke-MgUserSignInSession -UserId user@contoso.com
```
- Roles: User Administrator can disable non-admin users; Privileged Authentication Administrator is needed for admin accounts.
- Access tokens last 1 hour by default and an app using one loses access only when it expires, unless the app supports
  continuous access evaluation (Microsoft describes this as rolling out for Office 365 applications). If the disabled
  state is synced to an app, it may revoke sessions itself.
- Hybrid: disable the account on-premises as well; Entra ID is not the source of authority for synced users.

## Delete and restore
- A deleted user stays suspended and restorable for **30 days**; after that permanent deletion starts automatically and
  cannot be stopped. A permanently deleted user can't be restored by anyone, including Microsoft Support.
- Restore from **Deleted users** in the Entra admin center (at least User Administrator), or with Microsoft Graph
  `POST /directory/deletedItems/<object-id>/restore`, or PowerShell `Restore-MgDirectoryDeletedItem
  -DirectoryObjectId <id>`. Roles that can restore users through Graph: Authentication Administrator, Privileged
  Authentication Administrator, User Administrator.
- If a proxy address of the deleted user is now used by an active user, the restore request accepts the optional
  boolean `autoReconcileProxyConflict: true` to remove the conflicting addresses; otherwise resolve the conflict first.
- To skip the 30 days, permanently delete from the same Deleted users list (irreversible).

## Synced (hybrid) users
- Source of authority is on-premises AD. If the user still exists there, the sync engine may restore the user at the
  next sync cycle, so delete or disable on-premises first.
- A soft-deleted synced user can be restored by a match during a sync cycle, but the same 30-day window applies.

## Verify
- [ ] `az ad user show --id <upn> --query accountEnabled` returns `false` after the block.
- [ ] Deleted-users list shows the user with days remaining before permanent deletion.

## Checked
2026-10-27. Confirmed against Learn "Restore or remove a recently deleted user", "Revoke user access in an emergency",
Graph "Restore deleted item" and the az ad user CLI reference. Removed: Graph REST paths for revokeSignInSessions and
listing/deleting deleted items, cmdlets `Get-MgDirectoryDeletedItemAsUser` and `Remove-MgDirectoryDeletedItem`, the
60-90 minute token figure (docs say 1 hour default), the CAE app list, device/MFA/PIM/Intune leaver steps, object-ID,
licence and group restoration claims, mailbox retention, OU out-of-scope soft-delete, sign-in error 50057 and the
"Unknown principal" note, none confirmed in fetched pages.
Method: documentation only; no commands were run.
