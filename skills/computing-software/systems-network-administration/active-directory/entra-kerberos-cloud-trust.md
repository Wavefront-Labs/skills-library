---
id: computing-software.systems-network-administration.active-directory.entra-kerberos-cloud-trust
name: entra-kerberos-cloud-trust
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, entra-kerberos, cloud-kerberos-trust, azureadkerberos, windows-hello-for-business, fido2, set-azureadkerberosserver, krbtgt-azuread, hybrid-identity, azure-files]
level: advanced
status: docs-checked
description: "Set up Entra Kerberos (the AzureADKerberos RODC-like object) so cloud sign-ins with WHfB/FIDO2 get on-prem Kerberos tickets; key rotation and scope."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-passwordless-security-key-on-premises
  - https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/deploy/hybrid-cloud-kerberos-trust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Kerberos (cloud Kerberos trust)

**What:** Entra ID can issue Kerberos TGTs for one or more on-premises AD domains. A user signing in to Windows with a
FIDO2 security key or Windows Hello for Business (cloud Kerberos trust) gets a partial TGT from Entra that contains only
the user's SID and no authorization data; on-premises DCs exchange it for a full TGT, and service tickets and
authorization stay under DC control.

## Prerequisites (from Microsoft)
- DCs on Windows Server 2016 or later with the listed updates; AES256_HMAC_SHA1 must be allowed when the "Network security:
  Configure encryption types allowed for Kerberos" policy is configured on DCs.
- Enough read-write DCs in each AD site where WHfB users sign in.
- An AD account in Domain Admins for the domain and Enterprise Admins for the forest, and an Entra Hybrid Identity
  Administrator.

## Create the Kerberos server object (per domain)
```powershell
Install-Module -Name AzureADHybridAuthenticationManagement -AllowClobber
$domain = 'ad.example.com'
$upn = 'admin@example.com'     # Hybrid Identity Administrator; required when MFA or passwordless is enforced
Set-AzureADKerberosServer -Domain $domain -UserPrincipalName $upn -DomainCredential (Get-Credential)
Get-AzureADKerberosServer -Domain $domain -UserPrincipalName $upn -DomainCredential (Get-Credential)
```
Run on any machine that can reach a DC; skip `-DomainCredential` on a domain-joined machine signed in as a domain admin.
Enter the domain credential in UPN format so the RPC bind uses Kerberos. This creates an object **AzureADKerberos** in the
Domain Controllers OU that appears as an RODC but is not a physical server, and a disabled user
`CN=krbtgt_AzureAD,CN=Users,<domain DN>` that holds the TGT encryption key.

## Security model
- The same rules as RODCs apply to AzureADKerberos: members (direct or indirect) of privileged built-in groups cannot use
  cloud Kerberos trust or FIDO2 SSO, because of the default Password Replication Policy. Microsoft advises not relaxing
  that policy.
- **Rotate** the krbtgt key on the same schedule as other DC krbtgt keys, using this tool only so AD and Entra stay in sync:
```powershell
Set-AzureADKerberosServer -Domain $domain -UserPrincipalName $upn -DomainCredential (Get-Credential) -RotateServerKey
```
- Remove with `Remove-AzureADKerberosServer`, not by deleting the objects manually.

## Enable WHfB cloud Kerberos trust on clients
Intune or GPO setting **Use cloud trust for on-premises authentication** (Use Cloud Trust For On Prem Auth) = Enabled, with
WHfB enabled.

## Verify
- [ ] `Get-AzureADKerberosServer` shows `KeyVersion` equal to `CloudKeyVersion` and matching domain and ID values.
- [ ] A sign-in with a security key or WHfB can open an on-premises file share without a password prompt.

## Checked
Checked 2026-10-27 against Microsoft Learn: entra-docs (FIDO2 SSO to on-premises resources, module install, key rotation)
and the Windows Hello for Business cloud Kerberos trust page. Confirmed cmdlet names and parameters, the AzureADKerberos and
`krbtgt_AzureAD` objects, the privileged-group restriction, rotation guidance and the client policy name. Removed the
`klist cloud_debug` check, the Azure Files and "no PKI" statements and `-Scope CurrentUser`, which the pages do not state.
Method: documentation only; no commands were run.
