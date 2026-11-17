---
id: computing-software.cybersecurity-defensive.endpoint-security.smart-app-control
name: smart-app-control
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [smart-app-control, windows-11-security, app-reputation, code-integrity, consumer-app-control, windows-endpoint-protections]
level: practitioner
status: docs-checked
description: "Understand Windows 11 Smart App Control: evaluation vs on modes, reputation and signature checks, why it suits unmanaged devices, and when to use App Control for Business instead."
sources: ["https://support.microsoft.com/en-us/topic/what-is-smart-app-control-285ea03d-fa88-4d56-882e-6698afdb7003", "https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/overview", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart App Control

A built-in App Control policy for Windows 11 that blocks apps that are untrusted (unknown reputation in
Microsoft's cloud intelligence) and unsigned/invalidly signed - including scripts and MSI.

## Modes
- **Evaluation**: on clean installs, Windows watches usage; turns itself On if the user is a good candidate, Off otherwise.
- **On**: enforces; cannot be bypassed per app (no allow-list).
- **Off**: historically could only be re-enabled by reinstalling/resetting Windows; newer Windows 11 builds allow turning it back on without reinstall - check the current build's behaviour.
Check: Windows Security -> App & browser control -> Smart App Control; registry `HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy` `VerifiedAndReputablePolicyState` (0 off, 1 on, 2 evaluation).

## Where it fits
- Unmanaged/consumer, small business devices without IT-managed allowlisting.
- **Managed enterprise devices** (Intune/ConfigMgr enrolled): SAC turns off on enterprise-managed devices; use App Control for Business with managed installer and optional Intelligent Security Graph instead, which offers allow rules and central management.

## Developer guidance
Sign your binaries with a trusted certificate (or Trusted Signing), so SAC/reputation checks pass; unsigned
installers are blocked when SAC is on.

## Events
Code integrity events (see the App Control event ID reference) show blocks.

## Checked
2026-10-28. Confirmed in the App Control and Smart App Control pages: `VerifiedAndReputablePolicyState` under `HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy` (0 off, 1 enforce, 2 evaluation), evaluation mode that turns itself off on enterprise-managed devices. Removed: the event log path and event number.
Method: documentation only; no commands were run.

## Verify
- [ ] On BYOD/small business devices: SAC state known and On where possible.
- [ ] On managed fleet: App Control for Business policy deployed instead.
