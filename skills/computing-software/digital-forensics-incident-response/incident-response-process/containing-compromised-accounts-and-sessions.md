---
id: computing-software.digital-forensics-incident-response.incident-response-process.containing-compromised-accounts-and-sessions
name: containing-compromised-accounts-and-sessions
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [account-containment, session-revocation, password-reset, entra-id, active-directory, containment, dfir]
level: practitioner
status: docs-checked
description: "Contain compromised accounts: disable and double-reset in AD, disable and revoke sessions in Entra ID, handle app session tokens, and disable malicious apps."
sources: ["https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access", "https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-compromised-malicious-app"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containing compromised accounts and sessions

**Goal:** the attacker's stolen password, tokens and sessions stop working. Disabling an account
and revoking tokens is not instant: the delay depends on how each application grants access.

## On-premises AD (hybrid environments start here)
```powershell
Disable-ADAccount -Identity jdoe
# Reset twice, with random values (never example passwords), to mitigate pass-the-hash
# when on-premises password replication is delayed
Set-ADAccountPassword -Identity jdoe -Reset -NewPassword (Read-Host -AsSecureString)
Set-ADAccountPassword -Identity jdoe -Reset -NewPassword (Read-Host -AsSecureString)
```
Microsoft notes you may reset only once if you can safely assume the account is not compromised.
For service accounts, rotate and update every consumer or the service breaks.

## Entra ID
Admin centre: Entra ID > Users > All users > the user > Account status > Edit, clear
**Account enabled**, then **Revoke sessions** on the Overview page. Scriptable form:
```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","Directory.AccessAsUser.All"
$User = Get-MgUser -Search UserPrincipalName:'jdoe@contoso.com' -ConsistencyLevel eventual
Update-MgUser -UserId $User.Id -AccountEnabled:$false
Revoke-MgUserSignInSession -UserId $User.Id      # revokes refresh tokens
Get-MgUserRegisteredDevice -UserId $User.Id -All | ForEach-Object {
    Update-MgDevice -DeviceId $_.Id -AccountEnabled:$false }   # disable the user's devices
```
Roles: User Administrator for non-admin users, Privileged Authentication Administrator for admin
accounts, Cloud Device Administrator (at least) for devices.

## How long access lasts after revocation
- Entra access tokens last 1 hour by default; apps using access tokens lose access when the
  token expires. Continuous Access Evaluation (CAE) lets admins revoke access and session
  tokens for CAE-capable apps.
- Browser apps use their own session tokens (cookies). Entra cannot revoke an app-issued session
  token; the app must revoke it, so deprovision the user in each application too.
- Offline or unmanaged devices keep locally stored data; Intune wipe needs the device online.

## Compromised or malicious apps (OAuth, service principals)
- Review consent grants in the audit log (activity "Consent to application") for broad
  permissions or consents by users who should not grant them.
- Containment: disable sign-in to the app (service principal `accountEnabled = false`, e.g.
  `Update-MgServicePrincipal`), coordinated with an eviction event if admin credentials are also
  compromised. Weigh business impact first.
- Recovery: add a new credential, remove old password and key credentials on both the
  application and its service principals, rotate Key Vault secrets the principal could read.
- A soft-deleted application can be recovered for 30 days; watch audit logs for it being
  re-enabled or recovered.

## Verify
Sign-in logs show only failed attempts after containment time; no successful refresh token use;
no new credentials on the app or service principal.

## Checked
Date: 2026-11-08. Confirmed on Microsoft Learn "Revoke user access in an emergency in Microsoft Entra
ID" (AD disable and double reset, Graph cmdlets, 1 hour default token life, CAE, app session
tokens, roles, devices) and the "Compromised and malicious applications investigation" playbook
(consent audit, disabling the service principal, credential rotation, 30-day soft delete).
Removed as unsupported by either page: the Kerberos TGT 10 h claim, adminCount and SPN checks,
authentication-method cmdlet, inbox rules, the password-hash-sync re-enable claim, 60-90 min token
figure, and the Okta and Google Workspace notes.
Method: documentation only; no commands were run.
