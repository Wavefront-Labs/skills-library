---
id: computing-software.systems-network-administration.active-directory.protected-users-group-adoption
name: protected-users-group-adoption
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policies, protected-users-group, protected-users, ntlm, credential-caching, kerberos-aes, delegation, privileged-accounts, event-100-protected-users]
level: practitioner
status: docs-checked
description: "Put admin accounts in Protected Users safely: what it blocks (NTLM, delegation, RC4/DES, caching, 4h TGT), staged adoption, audit logs and which accounts to keep out."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protected Users group adoption

## What membership enforces
Prerequisites: hosts running Windows 10/11 or Windows Server 2012 R2 or later, and a domain functional level of
Windows Server 2012 R2 or later.
Device protections (when the member signs in): CredSSP and Windows Digest do not cache plaintext credentials; NTLM
does not cache plaintext credentials or the NT one-way function; Kerberos stops creating DES or RC4 keys and does not
cache plaintext credentials or long-term keys after the initial TGT; no cached verifier is created at sign-in or
unlock, so offline sign-in stops working.
Domain controller protections for members:
- **No NTLM** authentication.
- **No DES or RC4** in Kerberos pre-authentication (AES only).
- **No delegation**, unconstrained or constrained.
- **TGTs cannot be renewed beyond their initial four-hour lifetime**; the group sets the user-ticket lifetime and
  renewal limits to 240 minutes.
The built-in Administrator (RID 500) is exempt from authentication policies.

## Who goes in
Yes: human admin accounts and accounts with access to sensitive systems, once tested.
No: **service accounts and computer accounts** (Microsoft: never add them; membership gives no local protection
because the password or certificate is always on the host). Do not add accounts that are already members of
Enterprise Admins or Domain Admins until you can guarantee it will not have negative consequences; privileged members
face the same restrictions and can be locked out, so test first. Keep systems that only support NTLM out of scope.

## Staged adoption
1. Ensure account passwords were changed **after** the domain reached the Windows Server 2008 functional level or
   later (otherwise the account has no AES keys and cannot authenticate); migrated accounts need a password reset.
   Check `PasswordLastSet`.
2. Add one test admin and use it for a week across your admin tools. Connections that can only use NTLM fail; connect
   by name so Kerberos can be used.
3. Enable and watch the logs under `Applications and Services Logs > Microsoft > Windows > Authentication` (disabled by
   default): `ProtectedUser-Client` (events 104, 304) on clients, and `ProtectedUserFailures-DomainController`
   (event 100 for an NTLM failure, 104 for a DES/RC4 failure) and `ProtectedUserSuccesses-DomainController` (event 303,
   a TGT was issued) on DCs.
4. Add the rest of the admin group.
```powershell
Add-ADGroupMember 'Protected Users' -Members 'adm-jsmith','adm-mbrown'
Get-ADGroupMember 'Protected Users' | Select Name,objectClass
```

## Common breakages
- Tools connecting by IP address or legacy applications that need NTLM.
- Anything that needs delegation or an account that must sign in offline.
- Applications relying on Digest or CredSSP credential caching.

## Verify
- [ ] Admin sign-ins succeed via Kerberos (ProtectedUserSuccesses event 303 on the DC).
- [ ] An NTLM attempt for a member fails and logs ProtectedUserFailures event 100.

## Checked
2026-10-27. Documentation: Microsoft Learn "Protected Users security group" (Windows Server credentials protection).
Confirmed: operating-system and domain functional level prerequisites; device and DC protections (no NTLM, no DES/RC4,
no delegation, four-hour non-renewable TGT, 240-minute limits, no offline sign-in); the built-in Administrator exemption; never
add service or computer accounts; caution about Enterprise and Domain Admins; AES-key and password-reset guidance; the event
log names and event IDs 100, 104, 303 and 304. Corrected: the draft listed Domain, Enterprise and Schema Admins as a plain
yes; Microsoft says to test first and not to add them until safe. Removed as unconfirmed: the gMSA and break-glass
remarks, the RDP-by-IP and VPN MS-CHAPv2 breakages, the scheduled-task note and the AES256 klist check.
Method: documentation only; no commands were run.
