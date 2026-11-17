---
id: computing-software.cybersecurity-defensive.identity-access-management.account-lockout
name: account-lockout
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [account-lockout, smart-lockout, lockout-policy, password-spray, extranet-lockout, denial-of-service, password-policy]
level: practitioner
status: draft
description: "Configure account lockout without enabling DoS: AD lockout thresholds, Entra smart lockout and on-prem alignment, extranet lockout, RID 500 handling and lockout source tracing."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout", "https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/account-lockout-threshold", "https://pages.nist.gov/800-63-4/sp800-63b.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Account lockout and smart lockout

Lockout slows online guessing but lets attackers lock out users on purpose. Tune for both.

## Active Directory
- Default domain policy or FGPP: lockout threshold 5-10 (Microsoft baseline: 10), observation window 15 min, duration 15 min. 0 (never lock) leaves guessing unchecked; very low thresholds cause help desk load and DoS.
- NIST 800-63B: no more than 100 consecutive failed attempts before throttling/lockout - combine with banned passwords so slow sprays still fail.
- Built-in Administrator (RID 500) is exempt by default; `Allow Administrator account lockout` setting enables network lockout for it - use with LAPS.

## Entra smart lockout
- Distinguishes familiar vs unfamiliar locations; default lockout after 10 failures for 60 s, increasing.
- Customise (P1): threshold and duration. For hybrid with pass-through auth, set Entra threshold **lower** than AD's and duration **longer**, so cloud locks out before AD does.
- Identical bad passwords repeated do not count again (prevents users locking themselves with an old saved password).

## AD FS
Extranet Smart Lockout in enforce mode (see adfs-hardening), threshold below AD.

## Tracing lockouts
- Event 4740 on the PDC emulator (caller computer name), 4625/4771 on DCs for the source.
- Common sources: old credentials on phones (ActiveSync), mapped drives, scheduled tasks, services.
- A spray shows many users locking from one/few IPs - escalate as attack.

## Verify
- [ ] Entra threshold < AD threshold and duration longer (hybrid).
- [ ] SIEM alert on lockout spikes across many accounts.
