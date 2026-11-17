---
id: computing-software.systems-network-administration.windows-server.nps-extension-for-entra-mfa
name: nps-extension-for-entra-mfa
category: computing-software
field: systems-network-administration
product: windows-server
tags: [nps, nps-extension-mfa, radius-clients, entra-id, multifactor-authentication]
level: advanced
status: docs-checked
description: "Add Microsoft Entra MFA to RADIUS (VPN, RD Gateway) with the NPS extension: install, certificate script, UPN matching, timeouts and failure modes."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-nps-extension
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-nps-extension-advanced
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS extension for Microsoft Entra MFA

The extension adds cloud-based MFA (phone call, text message, app notification or verification code) to an NPS-based
authentication infrastructure. After the primary authentication, NPS calls Microsoft Entra for the second factor.

## Deploy
1. Plan which RADIUS clients need MFA: once the extension is enabled, all authentications for a RADIUS client sent to that NPS server require MFA. To protect some clients but not others, use two NPS servers and install the extension on only one. Users must be synced to Entra ID and registered for MFA.
2. Install the NPS extension, then run the configuration script installed under the AzureMfa Config folder as administrator:
```powershell
cd "$env:ProgramFiles\Microsoft\AzureMfa\Config"
.\AzureMfaNpsExtnConfigSetup.ps1
```
   The script signs in to your tenant and creates a certificate that is registered for the NPS extension. For Azure Government or Azure operated by 21Vianet, edit the script's Environment parameter first.
3. The certificate created by the script is valid for 2 years. Before it expires run the script again with the same tenant ID on each NPS server; delete expired certificates because they can stop the extension starting.
4. Configure the VPN or other RADIUS client to use these NPS servers with a timeout of at least 60 seconds (90 or 120 seconds if needed), so the user has time to respond. Duplicate or discarded requests in the NPS logs during an MFA prompt are expected behaviour.

## Authentication protocols
- PAP supports phone call, one-way text message, mobile app notification, OATH hardware tokens and app verification code.
- CHAPV2 and EAP support phone call and mobile app notification.
- The extension does not support changing passwords during sign-in.

## UPN matching
By default the extension uses the UPN from on-premises AD DS. If it differs from the Entra name, set `LDAP_ALTERNATE_LOGINID_ATTRIBUTE` (string, under `HKLM\SOFTWARE\Microsoft\AzureMfa`) to the AD attribute to use instead (for example mail).

## Users not enrolled for MFA
`REQUIRE_USER_MATCH` (under `HKLM\Software\Microsoft\AzureMFA`): not set behaves as TRUE and rejects users not enrolled. FALSE lets unenrolled users authenticate without MFA; enrolled users must still complete MFA.

## Verify
- [ ] A registered test user receives the MFA prompt and connects; an unregistered user behaves as the `REQUIRE_USER_MATCH` setting dictates.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed per-client MFA scope, the AzureMfa Config script path and name, 2-year certificate validity and renewal, the 60-second (up to 120) timeout recommendation, protocol support (PAP versus CHAPV2 and EAP), LDAP_ALTERNATE_LOGINID_ATTRIBUTE and REQUIRE_USER_MATCH semantics. Corrected: EAP is supported for phone call and app notification, not unsupported. Removed the unconfirmed event-log names and reason 21.

Method: documentation only; no commands were run.
