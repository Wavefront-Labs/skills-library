---
id: computing-software.cybersecurity-defensive.endpoint-security.intune-security-baselines
name: intune-security-baselines
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [intune-security-baselines, security-baselines, windows-security-baseline, defender-baseline, edge-baseline, configuration-drift, mobile-device-management]
level: practitioner
status: draft
description: "Deploy Intune security baselines: choosing baselines, customising settings, conflict resolution with other profiles, version upgrades and per-setting compliance reporting."
sources: ["https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines", "https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines-configure", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intune security baselines

Microsoft-maintained groups of recommended settings: Security Baseline for Windows, Microsoft Defender
for Endpoint baseline, Microsoft Edge baseline, Windows 365 baseline, Microsoft 365 Apps baseline.

## Deploy
1. Endpoint security -> Security baselines -> choose baseline -> Create profile (latest version).
2. Review each setting; customise where business needs differ (e.g. BitLocker removable drives, SmartScreen behaviour), document deviations with reason.
3. Assign to a pilot group, then broad. Use filters to exclude special devices (kiosks, lab).

## Conflicts
- Baseline settings conflicting with another profile (settings catalog, GPO via co-management, another baseline) show as **Conflict** and neither applies reliably. One owner per setting: pick baseline or settings catalog, not both.
- Hybrid devices also receiving GPO: MDM wins over GPO only where `ControlPolicyConflict/MDMWinsOverGP` is set.

## Upgrades
New baseline versions are not applied automatically; create a new version profile (Intune lets you change an instance to a newer version and review added/removed/changed settings) and roll out by ring.

## Reporting
Per-profile device status and per-setting status (succeeded, error, conflict, not applicable).
Export and track: % devices compliant with baseline; errors per setting.

## Gotchas
- Baselines are a starting point, not a complete hardening (e.g. ASR rules, App Control are separate).
- Some settings require reboots; devices report pending.
- Removing a baseline does not necessarily revert settings (tattooing for some CSPs).

## Verify
- [ ] Baseline profile status > 95% succeeded; no unresolved conflicts.
- [ ] Deviations documented and approved.
