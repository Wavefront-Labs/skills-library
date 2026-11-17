---
id: computing-software.cybersecurity-defensive.identity-access-management.ldap-signing-and-ldaps
name: ldap-signing-and-ldaps
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, ldaps, ldap-signing, channel-binding, active-directory, ntlm-relay, event-2889]
level: practitioner
status: docs-checked
description: "Enforce LDAP signing and channel binding and move clients to LDAPS in Active Directory: auditing event 2889, certificates on DCs, client fixes and phased enforcement."
sources: ["https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server", "https://support.microsoft.com/en-us/topic/2020-2023-and-2024-ldap-channel-binding-and-ldap-signing-requirements-for-windows-kb4520412-ef185fb8-00f7-167d-744c-f299a66fc00a", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-over-ssl-3rd-certification-authority"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP signing and LDAPS

**Goal:** stop cleartext LDAP binds (password exposure) and NTLM relay to LDAP (a common AD
privilege-escalation path) by requiring signing, channel binding and LDAPS.

## 1. Audit current usage
- On DCs, enable diagnostic logging: `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Diagnostics`
  `16 LDAP Interface Events` = 2.
- Event **2887** (daily summary of unsigned/simple binds) and **2889** (per client: IP and
  account doing unsigned SASL or simple binds without TLS).
- Event **3039**/**3040/3041** for channel binding audit (with
  `LdapEnforceChannelBinding` = 1 when-supported mode).
Collect 2889 events in the SIEM for a few weeks and build the list of clients to fix.

## 2. Certificates for LDAPS
Each DC needs a valid server authentication certificate matching its FQDN (see the LDAPS certificate article; AD CS
domain controller templates can auto-enrol). Test:
```
openssl s_client -connect dc01.example.internal:636 -showcerts
ldp.exe  -> Connect, port 636, SSL
```
Clients must trust the issuing CA.

## 3. Fix clients
- Applications doing simple binds on 389 (Linux apps, appliances, printers' scan-to-email,
  VPNs, Java apps): switch to LDAPS 636 or StartTLS, using a dedicated low-privilege bind account.
- Windows clients sign by default with Negotiate; old settings may disable it
  (*Network security: LDAP client signing requirements* = Negotiate signing).

## 4. Enforce
- DC GPO: *Domain controller: LDAP server signing requirements* = **Require signing**.
- Channel binding: `HKLM\System\CurrentControlSet\Services\NTDS\Parameters\LdapEnforceChannelBinding`
  = 1 (when supported), then 2 (always) after clients are fixed.
- Optionally block 389 from non-admin networks at firewalls for non-Windows clients once
  migrated.

## Gotchas
- Requiring signing does not stop simple binds over TLS (which are fine); it rejects unsigned
  binds over plain 389.
- LDAPS on 636 is not affected by signing settings; channel binding applies to LDAPS.
- Certificate expiry on DCs breaks LDAPS clients suddenly; monitor expiry.
- NTLM relay to LDAPS is addressed by channel binding (set to always once clients are fixed) or EPA, not by signing; signing protects 389.

## Verify
No 2889 events for 30 days; `ldapsearch -x -H ldap://dc01 -D user -w pass` simple bind is
rejected; LDAPS bind works; relay tooling in a lab fails.

## Checked

2026-10-28. Confirmed against the LDAP signing troubleshoot article and the KB4520412 article: 16 LDAP Interface Events diagnostic at level 2, events 2887 (daily summary) and 2889 (per client), channel binding events 3039, 3040 and 3041, LdapEnforceChannelBinding registry value, Require signing policy. Removed: strongerAuthRequired error string, enforced/audit variant claim, DC certificate EKU and SAN specifics, overclaim that only channel binding = 2 stops relay.

Method: documentation only; no commands were run.
