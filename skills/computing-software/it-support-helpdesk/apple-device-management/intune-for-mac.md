---
id: computing-software.it-support-helpdesk.apple-device-management.intune-for-mac
name: intune-for-mac
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, mdm-alternatives, intune-for-mac, intune-mac, company-portal]
level: practitioner
status: draft
description: "Manage Macs with Microsoft Intune using ADE, the Company Portal, shell script policies and the Microsoft Intune management agent."
sources:
  - "https://docs.kandji.io/"
  - "https://learn.microsoft.com/en-us/mem/intune/"
  - "https://github.com/micromdm/nanomdm"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# intune-for-mac

Goal: decide when Intune is enough for Macs.
- Enrolment profile in Intune > Devices > Apple > Enrollment; Setup Assistant can require Company Portal sign-in.
- Apps via VPP, LOB pkg or DMG; scripts run through the Intune management agent (shell scripts, custom attributes).
- Settings catalog covers many macOS payloads; custom profiles accept `.mobileconfig`.
- Update policies use DDM for macOS (confirm release).
- Missing vs Jamf: extension-attribute-style smart groups and rich Self Service.
- See the intune-mdm skills for enrolment details.
Gotcha: the Intune agent runs scripts only after first check-in and at fixed intervals (about every 8 hours), so time-critical setup needs another tool.
Verify:
- Mac shows compliant in Intune.
- Script policy reports Success in the device blade.
