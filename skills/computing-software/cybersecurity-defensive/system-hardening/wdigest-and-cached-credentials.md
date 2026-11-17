---
id: computing-software.cybersecurity-defensive.system-hardening.wdigest-and-cached-credentials
name: wdigest-and-cached-credentials
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-hardening, wdigest, uselogoncredential, cached-logons, cachedlogonscount, credential-theft, lsass]
level: practitioner
status: docs-checked
description: "Remove easy credential exposure on Windows: keep WDigest disabled and alert on UseLogonCredential changes, limit cached domain logons, and related LSASS hygiene settings."
sources: ["https://support.microsoft.com/en-us/topic/microsoft-security-advisory-update-to-improve-credentials-protection-and-management-may-13-2014-93434251-04ac-b7f3-52aa-9f951c14b649", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/cached-domain-logon-information", "https://attack.mitre.org/techniques/T1003/005/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WDigest and cached credentials

## WDigest
With `UseLogonCredential` = 1, WDigest stores credentials in memory. Windows 8.1/Server 2012 R2 and later do not store them by default (value
defaults to 0 when absent). On Windows 7/8/Server 2008 R2/2012 the KB2871997 update adds the control and the default stays 1 until
set to 0. An attacker with admin rights can set it back to 1 and wait for the next logon:
`HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest` `UseLogonCredential` = 1.

Actions:
- Enforce `UseLogonCredential` = 0 with Group Policy (the setting is delivered by the policy described in the Microsoft advisory) so drift is corrected.
- **Alert** on any write of `UseLogonCredential` (EDR or registry auditing). A change back to 1 is a strong sign of hands-on-keyboard credential theft.
- Applications that genuinely need Digest auth are rare; check before enforcing on old servers.

## Cached domain logons
Windows caches information about previous domain logons so users can log on when no logon server is available.
- The `CachedLogonsCount` registry value sets how many are cached: valid range 0 to 50, 0 turns logon caching off, and by default all versions of Windows remember 10 cached logons except Windows Server 2008.
- Set it low on servers and always-connected machines; laptops need at least 1 for offline logon.
- Privileged accounts should not log on interactively to lower-tier machines where their logon information would be cached.

## Related LSASS hygiene
- LSA protection and Credential Guard to protect what remains in memory (see the Windows security documentation).

## Gotchas
- An attacker with admin can change any of these registry values; detection on change matters as much as the setting.
- Setting `CachedLogonsCount=0` on laptops locks users out when offline.

## Verify
Registry shows `UseLogonCredential` 0 (or absent on Windows 8.1/Server 2012 R2 and later) on all hosts, `CachedLogonsCount`
matches policy per tier, and a lab change to `UseLogonCredential` raises an alert.

## Checked

2026-10-28. Confirmed against: Microsoft security advisory (May 2014) for WDigest defaults and the UseLogonCredential registry value; Microsoft Learn 'Cached domain logon information' for CachedLogonsCount range and default.

Removed as unconfirmed: CIS recommendation figures, Sysmon/4657 event ids, KQL example, ADMX setting name, Protected Users and SeDebugPrivilege bullets, RunAsPPL name, Mimikatz claim.

Method: documentation only; no commands were run.
