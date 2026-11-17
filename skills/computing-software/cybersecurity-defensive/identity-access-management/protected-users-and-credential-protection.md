---
id: computing-software.cybersecurity-defensive.identity-access-management.protected-users-and-credential-protection
name: protected-users-and-credential-protection
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, protected-users, credential-protection, tier-0, ntlm, delegation, account-is-sensitive-and-cannot-be-delegated, authentication-policy-silos]
level: advanced
status: docs-checked
description: "Protect privileged AD credentials with the Protected Users group, 'sensitive and cannot be delegated', authentication policies and silos, and know what each breaks."
sources: ["https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/how-to-configure-protected-accounts", "https://adsecurity.org/?p=1667"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protected Users and credential protection

**Goal:** privileged account credentials cannot be cached, relayed over NTLM, or delegated
where attackers can harvest them.

## Protected Users group (domain functional level 2012 R2+)
Members get, on supported clients and DCs:
- No NTLM authentication, no DES/RC4 in Kerberos pre-auth (AES only).
- No cached credentials (no offline logon), no CredSSP/WDigest plaintext caching.
- No Kerberos delegation (unconstrained or constrained).
- TGT lifetime is limited (see the Protected Users article for the value).

Add Tier 0 and Tier 1 human admin accounts. **Do not** add service accounts, computer
accounts, or break-glass accounts (they might need NTLM/offline logon in an emergency).

## Complementary settings
- **"Account is sensitive and cannot be delegated"** on all privileged accounts (works on older levels too).
- **Authentication policy silos**: restrict Tier 0 accounts to sign in only from Tier 0 hosts (DCs, PAWs) and set TGT lifetime.
- Deny logon rights via GPO: Tier 0 accounts denied logon to workstations and member servers (Deny log on locally / through RDS / as batch / as service).
- **Credential Guard** on admin workstations and servers.
- LSA protection on all systems.

## Rollout
1. Check admins' accounts can use AES Kerberos keys.
2. Pilot with a few admins first; watch for failures (ProtectedUser-Client events such as 104 and 304
   on clients, plus DC-side logs).
3. Add the rest; document the TGT lifetime impact (re-authentication).

## Gotchas
- Apps requiring NTLM or delegation break for members: admins should not use privileged accounts for those apps anyway.
- If all Domain Admins are in Protected Users and Kerberos breaks (time skew, DC issue), you can lock yourself out: keep a break-glass outside the group.
- Old OS versions ignore the protections client-side.

## Verify
- [ ] All privileged human accounts are members or flagged sensitive; report lists exceptions with reasons.
- [ ] Test: NTLM authentication with a member account fails as expected.

## Checked

2026-10-28. Confirmed against the Protected Users page and adsecurity.org: domain functional level 2012 R2, no NTLM, no DES/RC4, no CredSSP or WDigest plaintext caching, no cached credentials, no delegation, ProtectedUser-Client events (for example 104 and 304). Removed: 4-hour TGT figure, 2-week pilot figure, event id range 100-104, AES key password-age claim, FAST requirement, RunAsPPL name.

Method: documentation only; no commands were run.
