---
id: computing-software.systems-network-administration.patch-management.intune-security-baselines
name: intune-security-baselines
category: computing-software
field: systems-network-administration
product: patch-management
tags: [intune-security-baseline, intune, security-baseline, endpoint-security, config-baselines, patch-management]
level: practitioner
status: docs-checked
description: "Deploy and maintain Intune security baselines: profile versions, customisation, conflicts with GPO and settings catalog, version upgrades and per-setting compliance reports."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines
  - https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines-configure
  - https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines-monitor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intune security baselines

Intune ships preconfigured groups of settings: Security Baseline for Windows 10 and later, Microsoft Defender for Endpoint baseline, Microsoft 365 Apps for Enterprise baseline, Microsoft Edge baseline, Windows 365 baseline and others (HoloLens 2; a STIG audit baseline for GCC High tenants that audits only). Deploying baselines needs a Microsoft Intune Plan 1 subscription and an Intune RBAC role with the Security baselines permissions; the least privileged built-in role is Policy and Profile Manager. The Defender for Endpoint baseline is currently not recommended for VMs or VDI endpoints.

## Deploy
1. Intune admin center > Endpoint security > Security baselines > choose the baseline > Create policy.
2. On Configuration settings review every category; change values that conflict with your requirements (document each as a baseline deviation).
3. Assign to a pilot group; monitor for a week; then broad groups. A profile deploys as soon as it is created with assignments. Baselines go to user groups or device groups depending on the settings, so you may need more than one.
4. You can deploy several baselines, or several customised instances of one baseline, at once, but review them for different values of the same setting; those produce conflicts.

## Version upgrades
New baseline versions arrive periodically (e.g. Windows baseline version 24H2). Existing profiles do not upgrade automatically; once a newer version exists their settings become read-only (name, description and assignments stay editable) and only the latest version can be used for new profiles.
- Profiles pane > select the profile > **Update Version** (profiles created in May 2023 or later; older-format profiles use **Change Version**, which can export a CSV of differences with Review update).
- Choose "Accept baseline changes but keep my existing setting customizations" or "... discard existing setting customizations". Updating creates a new side-by-side instance; scope tags and assignments are not carried over, so assign the new one and remove the old one's assignments to avoid conflicts.
- Pilot the new version on a duplicate before switching all groups (Duplicate copies settings and scope tags but not assignments).
- Removing a baseline setting or assignment does not necessarily revert the device setting; each CSP handles removal differently.

## Conflicts
- Baselines often manage the same settings as device configuration profiles and other policy types, and different baselines can recommend different defaults for the same setting (Windows versus Defender). Review each setting's intent.
- When two profiles configure the same setting with different values the device reports Conflict. In the setting's details pane, Source Profiles lists the conflicting profiles; edit them so only one owns each setting.

## Monitor
- Profile dashboard: device and user check-in status, Device assignment status, and Per setting status (counts of Success, Error, Conflict per setting). Assignment status Pending means the device has not reported yet. Older-format profiles use Device status (Succeeded, Error, Conflict, Pending, Not applicable); data can take up to 24 hours to appear after first assignment.
- On a device: Settings > Accounts > Access work or school > select the account > Info > Advanced Diagnostic Report > Create report > Export; or Event Viewer > Applications and Services Logs > Microsoft > Windows > DeviceManagement-Enterprise-Diagnostics-Provider > Admin.

## Gotchas
- In almost all scenarios the baseline defaults are the most restrictive; confirm they do not conflict with other policy or features (Microsoft's example: firewall defaults may not merge connection security and local rules, so validate before assigning if you use delivery optimization). Pilot with app owners.
- Do not use preview baseline versions in production.
- Microsoft states the baselines are not strictly CIS or NIST compliant; there is no one-to-one mapping. Use them as a starting point and customise.

## Verify
Baseline profile shows (as an example internal target) nearly all devices Succeeded with zero unexplained Conflicts; deviation list matches customised settings.

## Checked
Date: 2026-11-08. Documentation: the three Microsoft Learn Intune security baseline articles (overview, manage profiles, monitor), as served after redirect to learn.microsoft.com/en-us/intune/device-security. Confirmed: baseline list, licensing and RBAC role, Create policy path, assignment behaviour, multiple instances allowed, read-only older versions, Update Version/Change Version options and side-by-side behaviour, Duplicate, removal behaviour, monitoring reports and statuses, MDM Advanced Diagnostic Report path, Event Viewer log path, preview and VDI cautions, CIS/NIST statement. Removed: the ControlPolicyConflict/MDMWinsOverGP claim, the one-profile-per-baseline rule (contradicted by the overview), the claim that specific named settings break legacy apps, the Info > Sync path, and the fixed 98% target (now an example).
Method: documentation only; no commands were run.
