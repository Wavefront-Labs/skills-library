---
id: computing-software.systems-network-administration.windows-server.adfs-access-control-policies-and-mfa
name: adfs-access-control-policies-and-mfa
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs-access-control-policy, mfa, relying-party-trusts, extranet]
level: advanced
status: docs-checked
description: "Apply AD FS access control policies to relying parties: built-in templates, custom policies for extranet MFA and group restrictions, and testing claims rules."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/access-control-policies-in-ad-fs
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/configure-ad-fs-and-azure-mfa
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/configure-authentication-policies
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/ad-fs-claims-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS access control policies and MFA

Since AD FS 2016, issuance authorization rules are replaced by **access control policies**: reusable templates
assigned to relying party trusts.

## Built-in policies
AD FS ships templates for common cases, such as permit intranet access only, permit everyone and require MFA from
extranet, and permit everyone and require MFA from a specific group. List the exact names on your server first.
```powershell
Get-AdfsAccessControlPolicy | Format-Table Name
Set-AdfsRelyingPartyTrust -TargetName 'Payroll' -AccessControlPolicyName '<template name from the list>'
```

## Custom policy
AD FS Management > Access Control Policies > Add Access Control Policy: rules like "Permit users in **GG-Payroll** and
from **extranet** with MFA; permit users in GG-Payroll from intranet". Multiple conditions in one rule are ANDed;
each rule has one action. A parameterized template takes its values (such as a group) when assigned to each
relying party trust and cannot be edited after creation; a non-parameterized template can be edited later.

## MFA providers
- Microsoft Entra multifactor authentication adapter: `New-AdfsAzureMfaTenantCertificate -TenantID <tenant>` generates
  the certificate (valid two years by default; renew with `-Renew $true`), then `Set-AdfsAzureMfaTenant -TenantId <tenant> -ClientId 981f26a1-7f43-403b-a875-f8b09b8cd720`
  once per farm. Or use certificate authentication or a third-party adapter.
- A method must be enabled as an additional authentication provider in the global authentication policy (for example
  `Set-AdfsGlobalAuthenticationPolicy -AdditionalAuthenticationProvider CertificateAuthentication`; Authentication Methods in AD FS Management).

## Test
- From inside and outside (through WAP) with a member and non-member account.
- Check the AD FS Admin log on the server that handled the request, plus the Security log if auditing is on.

## Gotchas
- Extranet detection relies on the `x-ms-proxy` claim that Web Application Proxy adds; requests that do not come through WAP count as intranet.
- Moving to Entra ID? Conditional Access replaces this (see adfs-to-entra-id-app-migration).

## Verify
- [ ] Non-member gets "access denied"; external member is prompted for MFA; internal member is not.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main (AD FS content, ms.date 2023-2024; AD FS in Windows Server 2016-2025).
Confirmed from Access-Control-Policies-in-AD-FS, configure-ad-fs-and-azure-mfa, Configure-Authentication-Policies and AD-FS-Claims-Types:
permit-model templates, AND semantics, parameterized versus non-parameterized behaviour, the built-in template examples (whats-new-in-windows-server-2016),
the Azure MFA certificate and tenant cmdlets, and the x-ms-proxy claim. Removed the unlisted template names, the New-AdfsAccessControlPolicy example and event ids that no page confirms.
Method: documentation only; no commands were run.
