---
id: computing-software.systems-network-administration.active-directory.password-writeback-and-sspr
name: password-writeback-and-sspr
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, password-writeback, sspr-writeback, self-service-password-reset, entra-connect, reset-password-permission, hybrid-identity, minimum-password-age]
level: practitioner
status: docs-checked
description: "Enable Entra self-service password reset with writeback to AD via Connect Sync or Cloud Sync: connector permissions, policy interplay, and testing."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback
  - https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-writeback
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password writeback and SSPR

**Goal:** users reset or change their password in the cloud (SSPR, or a forced change at sign-in), and the new password is
written to on-premises AD, so one password works everywhere.

## Enable
1. Licensing: at least Entra ID P1 (or a trial) for SSPR with writeback. An account with at least Hybrid Identity
   Administrator is needed.
2. **Connect Sync**: wizard > Customize synchronization options > Optional features > **Password writeback**.
   **Cloud Sync**: enable writeback in the Entra admin center (Password reset > On-premises integration, option
   *Write back passwords with Microsoft Entra Cloud Sync* once provisioning agents are detected), or with
   `Set-AADCloudSyncPasswordWritebackConfiguration -Enable $true -Credential (Get-Credential)` from the agent's
   `Microsoft.CloudSync.Powershell.dll` module.
3. Entra admin center > Entra ID > Password reset > On-premises integration: tick **Write back passwords to your on-premises
   directory** (and **Allow users to unlock accounts without resetting their password** if wanted) > Save.
4. Enable SSPR for a pilot group first and have users register authentication methods.

## AD permissions for the connector account (Connect Sync)
Microsoft's tutorial requires on the account Entra Connect uses: **Reset password**, **Change password**, **Write**
on `lockoutTime`, **Write** on `pwdLastSet`, and the **Unexpire Password** extended right on the root object of each domain.
Apply them to **This object and all descendant objects** (or similar) or they do not show; inheritance must not be
disabled on the target accounts. Allow up to an hour or more for ACL replication. For a custom connector account use:
```powershell
Import-Module "$env:ProgramFiles\Microsoft Azure Active Directory Connect\AdSyncConfig\AdSyncConfig.psm1"
Set-ADSyncPasswordWritebackPermissions -ADConnectorAccountName <ACCOUNT> -ADConnectorAccountDomain ad.example.com
```
Administrators cannot use the reset tool to reset their own password for writeback. Accounts with "Password never
expires" do not get the force-change flag set in AD.

## Policy interplay
- On-premises password policies can prevent resets from being processed. For writeback to work most efficiently,
  Microsoft says **Minimum password age** must be 0 (set it under Account Policies in the Group Policy editor), and 0 is
  required if users must change or reset more than once a day. Run `gpupdate /force` or wait for replication.
- Writeback happens after the on-premises policy is evaluated, so a violating password is rejected.

## Troubleshoot
- Check the Cloud Sync or Connect health state and the SSPR audit logs in Entra (Audit logs > Self-service password
  management).

## Verify
- [ ] Pilot user resets in the cloud, then signs in to a domain PC with the new password.
- [ ] A reset that violates the on-premises policy is rejected.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): the SSPR writeback tutorial, the writeback concept page and the
Cloud Sync agent install page. Confirmed licensing, the required AD permissions including Unexpire Password, the minimum
password age guidance, the portal options and the Cloud Sync cmdlet. Removed the unsourced `PasswordResetService` event ID
ranges, the "adminCount=1 does not inherit" statement and the claims about fine-grained policies and banned-password
interplay.
Method: documentation only; no commands were run.
