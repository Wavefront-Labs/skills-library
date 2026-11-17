---
id: computing-software.it-support-helpdesk.intune-mdm.compliance-noncompliance-actions-and-grace-periods
name: compliance-noncompliance-actions-and-grace-periods
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, noncompliance-actions, grace-period, mark-noncompliant, compliance-policy, retire-noncompliant, notification-templates, intune]
level: practitioner
status: docs-checked
description: "Design Intune actions for noncompliance: mark noncompliant schedule, email and push notices, remote lock, retire list, grace periods that avoid surprise Conditional Access blocks."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/configure-noncompliance-actions"
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/overview"
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/monitor-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compliance-noncompliance-actions-and-grace-periods

Each compliance policy has **Actions for noncompliance**, run on a schedule (days after
the device first becomes noncompliant).

## Available actions
| Action | Effect | Notes |
|---|---|---|
| Mark device noncompliant | Built-in default; schedule 0 days = immediately | Raising the delay gives a **grace period**: device shows "In grace period" (a noncompliant state the admin allows for a while) |
| Send email to end user | Uses a notification message template | Can also go to Entra groups; uses the profile email address, not the UPN; expected within 6 hours |
| Send push notification | Company Portal / Intune app notification | Android, iOS/iPadOS; delivery isn't guaranteed, don't use for urgent notices |
| Remotely lock | Locks the device | Android, iOS/iPadOS, macOS |
| Add device to retire list | Device appears in the Retire noncompliant devices list (Devices > Compliance) | Admin still confirms; retiring removes company data |

## A sane schedule
```text
Day 0   Send email + push: "Your device needs <x>; here's how"   (template with KB link)
Day 0   Mark noncompliant after 3 days   (grace for updates/encryption to finish)
Day 3   Email again: "Access to email will stop today"
Day 30  Add to retire list (corporate devices: review instead)
```
For security-critical settings (no encryption, jailbroken/rooted, threat level high) use
0 days grace; for OS-version requirements give longer. The schedule accepts whole days and
0.25 steps in the admin center.

## Notification templates
Endpoint security > Device compliance > Notifications > Create notification: subject (up to
78 characters), body, company contact info, link to KB. One message per locale; variables
such as `{{UserName}}` and `{{DeviceName}}` are supported.

## Support
- "I got an email saying my device isn't compliant": open the device in Intune > Device
  compliance > the failing setting. Fix that setting, then **Check compliance** from
  Company Portal or Settings > Access work or school > Sync.
- Devices with no compliance policy follow the tenant setting "Mark devices with no
  compliance policy assigned as" (default Compliant; set Not compliant when using
  Conditional Access).
- Compliance status validity period (default 30 days, configurable 1 to 120): devices that
  don't report in time are treated as noncompliant.

## Gotchas
- Pilot policy changes before broad assignment.
- No email address on the user's profile means no email is sent.
- Each push or email instance fires once; add a second instance at a later day for a reminder.

## Verify
Assign the policy to a test device that fails one setting, confirm "In grace period",
the email arrives with the right text, and after the grace days it turns Not compliant.

## Checked
2026-11-01. Confirmed against the Intune Learn pages on noncompliance actions, compliance
overview and compliance monitoring: action list, platform support, zero-day default, 6-hour
email expectation, 78-character subject, 30-day default validity (1 to 120), tenant
no-policy default. Removed: claim that grace-period devices count compliant for Conditional
Access, Windows push support, CC wording, grace-period exemption claim, re-evaluation and
user-behaviour claims, and the 7-14 day figure.
Method: documentation only; no commands were run.
