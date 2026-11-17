---
id: computing-software.it-support-helpdesk.desktop-support.finding-account-lockout-sources
name: finding-account-lockout-sources
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, identity-support, account-lockout, lockout-source, event-4740, event-4771, caller-computer-name, lockoutstatus, smart-lockout, stale-credentials, entra-sign-in-logs]
level: practitioner
status: docs-checked
description: "Find what keeps locking an AD or Entra account: event 4740 caller computer, stale credentials on phones and services, Entra smart lockout."
sources:
  - "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# finding-account-lockout-sources

Goal: stop the repeat lockout cycle by finding the device or process still using an old
password.

## On-premises AD
Pull lockout events from the domain controller that logged them, with the caller:
```powershell
Get-WinEvent -ComputerName DC01 -FilterHashtable @{LogName='Security'; Id=4740; StartTime=(Get-Date).AddDays(-1)}
```
Event 4740 has a "Caller Computer Name" field: the computer from which the logon attempt
was received and after which the account was locked out. That is where the bad attempts came
from. If the caller is a server that fronts other clients (mail, federation, RADIUS/VPN),
the real source is behind it: check that server's own logs for the client.

## Usual culprits on the caller machine
- Saved credentials (Credential Manager, mapped drives), scheduled tasks or services
  running as the user, old sessions still signed in on other servers.
- Phones and tablets with corporate email or Wi-Fi still using the old password, often the
  most common cause after a password change.

## Entra ID (cloud)
Smart lockout uses familiar versus unfamiliar locations, with separate lockout counters for
each, so a bad actor can be locked out while the genuine user keeps signing in. The
documented default is 10 failed attempts and a 60 second lockout duration (public cloud
tenants; check the page for your cloud). Blocked sign-ins return AADSTS50053. Use the
sign-in logs to see IP, client app and location; unknown foreign IPs point to password
spray rather than the user, so escalate to security instead of only unlocking.

## Gotchas
- Unlocking without fixing the source just restarts the timer.
- Event 4740 is only logged if the relevant audit policy is enabled on the domain
  controllers; the event page lists the subcategory as Audit User Account Management.

## Verify
After removing the stale credential, no new 4740 appears for the account.

## Checked
2026-11-01. Confirmed against Microsoft Learn "Event 4740 (S) A user account was locked out"
(Caller Computer Name meaning) and "Protect user accounts from attacks with Microsoft Entra
smart lockout" (familiar/unfamiliar counters, 10 attempts and 60 s defaults, AADSTS50053).
Removed: PDC emulator step, 4771/4625 failure code, LockoutStatus.exe, cmdkey/quser/WMI
commands, error 50126, threshold advice, 24-hour check, ADFS/NPS event numbers, dead
troubleshooting source URL.
Method: documentation only; no commands were run.
