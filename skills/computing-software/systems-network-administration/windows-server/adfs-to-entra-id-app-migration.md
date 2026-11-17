---
id: computing-software.systems-network-administration.windows-server.adfs-to-entra-id-app-migration
name: adfs-to-entra-id-app-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs, adfs-to-entra-migration, entra-id, ad-fs-application-activity, saml-migration, staged-rollout, decommission-adfs]
level: advanced
status: docs-checked
description: "Migrate AD FS relying parties to Entra ID: application activity report, mapping claim rules, moving SAML apps, staged rollout to cloud auth and AD FS decommission."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/migrate-adfs-apps-stages
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/migrate-from-federation-to-cloud-authentication
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/decommission/adfs-decommission-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate AD FS applications to Entra ID

## Inventory
- With Microsoft Entra ID P1 or P2, deploy Microsoft Entra Connect Health for AD FS and use the AD FS application report
  to discover migratable apps and assess their readiness. Without those licences, use the AD FS to Entra app migration
  PowerShell tools in the AzureAD Deployment-Plans repository.
- List trusts locally: `Get-AdfsRelyingPartyTrust | Select Name,Identifier,Enabled`.

## Per application
1. Create an Enterprise application (gallery app if available, else non-gallery SAML).
2. Basic SAML configuration: Identifier = RP identifier, Reply URL = ACS.
3. Attributes and claims: translate claim rules (LDAP attribute = user attribute from
   Entra; group-based roles = app roles or group claims; transforms with claim
   transformations). Rules that query SQL or custom stores need redesign.
4. Conditional Access replaces access control policies (MFA, device, location).
5. Give the SP the Entra federation metadata, test with a pilot group, cut over.

## Move authentication off AD FS (federated domains)
- Enable Password Hash Sync (as backup even when keeping PTA).
- **Staged rollout**: Entra Connect > Change user sign-in > enable staged rollout for
  pilot groups with PHS or PTA and Seamless SSO.
- Convert the domain when ready with the Entra Connect wizard (Additional tasks > Change user sign-in) or
  `Update-MgDomain -DomainId <domain name> -AuthenticationType "Managed"`. Federated users then sign in to Entra directly.
- Staged rollout needs the Hybrid Identity Administrator role; nested and dynamic groups are not supported for it. Turn the
  staged rollout features off once cutover is finished.

## Decommission
- Confirm no sign-in activity remains (AD FS event logs or Entra Connect Health) before removing the Microsoft 365 trust.
- Follow the AD FS decommission guide: uninstall AD FS (secondary nodes first), delete the farm DNS entries and TLS/SSL
  certificates, and remove the content of the DN shown as `CertificateSharingContainer` in `Get-AdfsProperties` (ADSI Edit).

## Gotchas
- Apps that use legacy auth (Kerberos, NTLM, header-based): extend them with Microsoft Entra application proxy or a Secure
  Hybrid Access partner. Line-of-business apps using OAuth, OpenID Connect or WS-Federation can be registered as app registrations.
- If you keep AD FS for some apps, you use both AD FS and Entra ID after converting domains.

## Verify
- [ ] Every RP has an owner, a target, and a cut-over date; zero RPs left before decommission.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from entra-docs migrate-adfs-discover-scope-apps, migrate-adfs-apps-stages, migrate-from-federation-to-cloud-authentication and the AD FS decommission guide:
discovery options and licence condition, Update-MgDomain -AuthenticationType Managed, Change user sign-in task, staged rollout role and group limits,
decommission steps and CertificateSharingContainer. Removed the Export-Clixml line, the 30-day wait, event 1200, the CN=ADFS container path and the hybrid-join/SCP claim, none of which the pages state.
Method: documentation only; no commands were run.
