---
id: computing-software.systems-network-administration.active-directory.entra-password-protection-on-premises
name: entra-password-protection-on-premises
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, entra-password-protection, banned-passwords, custom-banned-password-list, dc-agent, proxy-service, audit-mode, enforced-mode, password-spray]
level: practitioner
status: docs-checked
description: "Deploy Entra Password Protection to DCs: proxy and DC agent install, audit then enforce, custom banned words, and reading the DC agent event log."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-ban-bad-on-premises-deploy
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-ban-bad-on-premises-monitor
  - https://learn.microsoft.com/en-us/entra/identity/authentication/concept-password-ban-bad-on-premises
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Password Protection for on-premises AD

**What:** DCs reject new passwords that match Microsoft's global banned list or your custom banned list, checked on every
password change or reset. A DC agent applies the policy; a proxy service fetches it from Entra.

## Components
- **Proxy service** on member servers (it can run on a DC for testing only, never on an RODC), with outbound HTTPS to Entra
  (`login.microsoftonline.com`, `enterpriseregistration.windows.net`, `autoupdate.msappproxy.net`). Microsoft recommends at
  least two proxies per forest. Needs .NET 4.7.2 and TLS 1.2 outbound, and DCs must be allowed to log on to it ("Access
  this computer from the network").
- **DC agent** on every writable DC. DCs reach the proxy over RPC (port 135 plus a dynamic or static RPC port); each DC
  keeps a local cache of the last policy, so brief proxy outages do not matter. Each proxy supports only DCs of the forest it
  is registered to.
- Licensing: users synced from on-premises AD DS need Entra ID P1 or P2 for the custom banned list and on-premises
  protection (cloud-only users need only Free for the global list); confirm against the current license page.

## Deploy
Install `AzureADPasswordProtectionProxySetup.exe` on each proxy (no reboot), then in an elevated PowerShell:
```powershell
Import-Module AzureADPasswordProtection
Register-AzureADPasswordProtectionProxy -AccountUpn 'admin@example.com'   # Global Administrator the first time in a tenant, Security Administrator after
Register-AzureADPasswordProtectionForest -AccountUpn 'admin@example.com'  # once per forest; needs domain admin rights in the forest root
```
Then install `AzureADPasswordProtectionDCAgentSetup.msi` on each DC. Installing or removing the agent requires a restart
(the password filter DLL loads at boot); `/norestart` defers it. Reboot DCs one at a time.
In the Entra admin center password protection settings:
- **Custom banned passwords**: limited to 1,000 terms.
- Enable password protection on Windows Server Active Directory, and start in **Audit** mode (the default initial mode).

## Audit, then enforce
In Audit mode the DC agent logs what it would block to
`Applications and Services Logs > Microsoft > AzureADPasswordProtection > DCAgent > Admin`.
| Outcome | Enforce mode | Audit mode |
|---|---|---|
| Pass | 10014 | 10015 |
| Fail (customer policy) | 10016, 30002 | 10017, 30003 |
| Fail (Microsoft policy) | 10016, 30004 | 10017, 30005 |
| Fail (both policies) | 10016, 30026 | 10017, 30027 |
| Fail (user name) | 10016, 30021 | 10017, 30022 |
Review the log (and include at least one DC promotion and demotion during audit, since stronger validation can affect DC
automation), tell users, then switch to **Enforced**.

```powershell
Get-AzureADPasswordProtectionDCAgent
Get-AzureADPasswordProtectionSummaryReport -DomainController dc01
```
`Get-AzureADPasswordProtectionDCAgent` lists installed agent versions in the forest; the summary report counts the Admin
log events by outcome.

## Verify
- [ ] Every writable DC is listed by `Get-AzureADPasswordProtectionDCAgent` with a current version.
- [ ] In Enforced mode, a password containing a custom banned term is rejected on a test account.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): on-premises password protection deploy, monitor and license pages.
Confirmed component requirements, the registration cmdlets and roles, the restart requirement, the 1,000-term limit, the log
path and the event ID table. Corrected the event IDs: 10014 and 10016 are enforce-mode pass and fail, 10015 and 10017 are
audit-mode, and the 30xxx IDs are companion detail events (not "rejected in enforce"). Removed the portal path, the
sample password and the user-message wording, which the pages do not state.
Method: documentation only; no commands were run.
