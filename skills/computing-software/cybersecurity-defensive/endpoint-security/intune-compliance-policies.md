---
id: computing-software.cybersecurity-defensive.endpoint-security.intune-compliance-policies
name: intune-compliance-policies
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [mobile-device-management, intune-compliance-policy, device-compliance, conditional-access, grace-period, noncompliance-actions, mdm]
level: practitioner
status: draft
description: "Design Intune compliance policies per platform and tie them to Conditional Access, with grace periods, noncompliance actions and reporting."
sources: ["Microsoft Learn - Device compliance policies in Microsoft Intune", "Microsoft Learn - Use compliance with Conditional Access", "CompTIA Security+ SY0-701 objective 4.1 (mobile device management)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intune compliance policies

**Goal:** only devices meeting a security baseline can reach corporate resources, enforced by
Conditional Access rather than by trust.

## Settings per platform (typical baseline)
| Platform | Compliance requirements |
|---|---|
| Windows | BitLocker, Secure Boot, code integrity, minimum OS build, firewall/AV/antispyware on, Defender for Endpoint risk score at or below Low/Medium, TPM |
| macOS | FileVault, SIP, firewall, minimum OS, Gatekeeper |
| iOS/iPadOS | Not jailbroken, minimum OS, passcode, Defender/MTD threat level |
| Android Enterprise | Not rooted, Play Integrity, minimum security patch level, encryption, passcode |

Tenant-wide settings: "Mark devices with no compliance policy assigned as" **Not compliant**;
compliance status validity period (default 30 days).

## Noncompliance actions
Mark noncompliant after a **grace period** (e.g. 1-3 days for OS updates), send email/push
notification immediately, remotely lock or retire only for serious cases.

## Conditional Access
Policy: All users (exclude break-glass) > cloud apps (start with Office 365, then all) >
Grant: Require device to be marked as compliant (or hybrid joined), with "require one of" MFA
for unmanaged scenarios via app protection policies.

## Rollout
1. Assign compliance policies to all devices; watch reports for a week before enforcement.
2. Enable CA in report-only mode; review sign-in logs "Report-only: Failure".
3. Enforce for pilot groups, then broadly; publish a self-help page for "device not compliant".

## Gotchas
- Minimum OS version set too high blocks users the day it changes; plan updates first.
- Compliance evaluation lag: devices check in every few hours; fixes are not instant.
- Linux and unsupported platforms need explicit handling (block, or browser-only access).

## Verify
- [ ] Compliance report: over 95% compliant, with reasons for the rest.
- [ ] Test noncompliant device (BitLocker off) is blocked from Exchange Online.
