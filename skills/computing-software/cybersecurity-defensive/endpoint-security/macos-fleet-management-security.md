---
id: computing-software.cybersecurity-defensive.endpoint-security.macos-fleet-management-security
name: macos-fleet-management-security
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [mobile-device-management, macos-mdm, jamf, intune-macos, automated-device-enrollment, configuration-profiles, filevault-escrow, declarative-device-management]
level: practitioner
status: draft
description: "Secure a macOS fleet with an MDM (Jamf, Intune, Kandji): automated enrolment, security profiles, FileVault escrow, updates via DDM, and admin rights."
sources: ["Apple Platform Deployment guide (MDM, Automated Device Enrollment, Declarative Device Management)", "CIS Apple macOS Benchmark", "NIST macOS Security Compliance Project (mSCP)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS fleet management security

**Goal:** every Mac is enrolled from first boot, configured to a security baseline, kept updated
and recoverable, without users holding standing admin rights.

## Enrolment
- **Automated Device Enrollment (ADE)** via Apple Business Manager: devices bought through
  Apple or authorised resellers enrol at Setup Assistant; enrolment is non-removable (supervised).
- Account-driven enrolment for BYOD (user-approved, limited management).

## Baseline configuration (use mSCP or CIS to generate profiles)
- FileVault enabled with personal recovery key **escrowed to MDM**.
- Firewall on, stealth mode; Gatekeeper App Store and identified developers; SIP enforced (cannot be disabled by profile, only verified).
- Screen lock: password required immediately after sleep, max idle 15 minutes.
- Disable guest account, automatic login, remote Apple events; restrict sharing services.
- Privacy Preferences Policy Control (PPPC) profiles to grant EDR and management tools full disk access silently.
- System and kernel extension allow-lists for EDR/VPN.

## Updates
Declarative Device Management (DDM) software update enforcement (macOS 14+): set target OS
version and deadline; MDM reports status. Older: Nudge plus MDM commands.

## Admin rights
Standard user accounts; temporary elevation via tools (Privileges app, Jamf Connect, Intune
Endpoint Privilege Management for macOS) with logging. Local admin account with LAPS-style rotation (Jamf, macOSLAPS).

## Compliance and reporting
Compliance policies (Intune) or smart groups (Jamf) for FileVault, OS version, EDR running;
feed to Conditional Access.

## Gotchas
- Macs bought outside ABM need manual addition (Apple Configurator) to get ADE.
- Bootstrap token escrow needed for some MDM features (software updates, kernel extensions) on Apple silicon.
- Profiles installed manually by users can be removed by them; deploy via MDM.

## Verify
- [ ] Inventory report: 100% supervised, FileVault on with escrowed key, OS within N-1.
- [ ] Recovery key retrieval tested for a sample device.
