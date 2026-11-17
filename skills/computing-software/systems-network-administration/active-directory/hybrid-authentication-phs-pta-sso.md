---
id: computing-software.systems-network-administration.active-directory.hybrid-authentication-phs-pta-sso
name: hybrid-authentication-phs-pta-sso
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, password-hash-sync, pass-through-authentication, seamless-sso, federation, staged-rollout, azureadssoacc, hybrid-identity, leaked-credentials]
level: practitioner
status: docs-checked
description: "Choose hybrid sign-in: password hash sync vs pass-through auth vs federation, enable seamless SSO, roll the AZUREADSSOACC key, and move off AD FS with staged rollout."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sso-faq
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-staged-rollout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid authentication: PHS, PTA, federation, seamless SSO

## Choose
| Method | Where the password is checked | Depends on on-prem at sign-in | Notes |
|---|---|---|---|
| **Password hash sync (PHS)** | Entra | no | simplest; also the basis for the *Users with leaked credentials* report |
| **Pass-through auth (PTA)** | on-prem DCs via PTA agents | yes (agents and DCs) | when policy forbids hashes in the cloud; install one or more agents, Microsoft recommends three in total |
| **Federation (AD FS)** | AD FS farm | yes | only for requirements Entra cannot meet natively |
Entra ID Protection requires PHS regardless of the sign-in method for its leaked-credentials report (the report needs
Entra ID P2), and PHS configured in advance lets you fail over if the primary method fails.

## Seamless SSO
Domain-joined devices on the corporate network get silent Kerberos sign-in to Entra, mainly useful where devices cannot be
Entra joined or hybrid joined.
- Enabled in Entra Connect; creates the computer account **AZUREADSSOACC** in each AD forest.
- Add `https://autologon.microsoftazuread-sso.com` to the Local Intranet zone (rolled out by GPO); allowlist the URL
  explicitly on any outbound HTTP proxy.
- **Roll over the Kerberos decryption key at least every 30 days.** Run `Update-AzureADSSOForest` once per forest, on the Connect
  server, with Domain Administrator and Hybrid Identity Administrator credentials (the admin must not be in Protected Users;
  use SAM format `domain\user` for the AD account):
```powershell
cd "$env:ProgramFiles\Microsoft Azure Active Directory Connect"
Import-Module "$env:ProgramFiles\Microsoft Azure AD Sync\Bin\ADSync\ADSync.psd1"
Import-Module .\AzureADSSO.psd1
New-AzureADSSOAuthenticationContext        # prompts for Hybrid Identity Administrator
$creds = Get-Credential                     # Domain Administrator of the forest
Update-AzureADSSOForest -OnPremCredentials $creds
```
- Protect AZUREADSSOACC: only Domain Admins should manage it, keep Kerberos delegation off it, store it in an OU safe from
  accidental deletion, and keep it out of any quarantine container.
- Kerberos encryption: Seamless SSO supports AES256, AES128 and RC4. Microsoft recommends setting `AzureADSSOAcc$` to
  AES-256 (stored in `msDS-SupportedEncryptionTypes`). Its page says the default Kerberos encryption type in AD DS changes
  from RC4 to AES-256 with the July 2026 Windows Server update, so RC4-only accounts may break. Roll over the key
  before switching the account from RC4 to AES, or Seamless SSO can stop working.

## Moving from federation to cloud auth
Staged rollout is a temporary testing mechanism: enable PHS (or PTA), add pilot groups to cloud authentication in Entra
Connect > Staged rollout while the domain stays federated, and keep a federated IdP as fallback. It needs the Hybrid
Identity Administrator role and is not meant to be permanent. When testing succeeds, convert the domain from federated
to managed (see Microsoft's federation-to-cloud migration guide) and decommission AD FS.

## Verify
- [ ] Entra sign-in logs show the expected authentication method per user.
- [ ] PTA agents (if used) all show active in the portal.
- [ ] `AZUREADSSOACC` key rolled within 30 days.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): choose-ad-authn, Seamless SSO quick start, how-it-works and FAQ
(rollover steps), and staged rollout. Confirmed the 30-day rollover, cmdlets, the module file `AzureADSSO.psd1`, the
intranet-zone URL, PTA agent guidance, staged-rollout limits and the July 2026 encryption-type change. Corrected the
module path (the module file is in the Entra Connect install folder, and the ADSync module must be imported first) and the
leaked-credential licensing note; replaced the Graph federation-removal claim with a pointer to Microsoft's migration guide.
Method: documentation only; no commands were run.
