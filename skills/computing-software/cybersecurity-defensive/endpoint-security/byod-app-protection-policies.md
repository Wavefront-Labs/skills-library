---
id: computing-software.cybersecurity-defensive.endpoint-security.byod-app-protection-policies
name: byod-app-protection-policies
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [mobile-device-management, mobile-application-management, mam, app-protection-policies, byod, intune-mam, data-transfer-restrictions, selective-wipe]
level: practitioner
status: draft
description: "Protect corporate data on personal phones without enrolling them: Intune app protection (MAM) policies, data transfer controls, Conditional Access and selective wipe."
sources: ["Microsoft Learn - App protection policies overview (Intune)", "Microsoft Learn - Data protection framework using app protection policies (levels 1-3)", "CompTIA Security+ SY0-701 objective 4.1 (BYOD, deployment models)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App protection for BYOD (MAM)

**Goal:** employees can use work email and files on personal devices, while corporate data
stays inside managed apps and can be wiped without touching personal data.

## Model
Mobile Application Management without enrolment (MAM-WE): policies apply to the work identity
inside managed apps (Outlook, Teams, OneDrive, Edge, Office). The device itself is not managed.

## Policy settings (Microsoft data protection framework, level 2 "enhanced" is a common target)
- **Data transfer**: send/receive data only with policy-managed apps; restrict cut/copy/paste to managed apps (allow paste in); block "Save as" to local/personal storage; open links in Edge (managed browser).
- **Access requirements**: app PIN or biometric, PIN after 30 minutes of inactivity; block jailbroken/rooted devices; minimum app and OS versions.
- **Conditional launch**: offline grace period (e.g. 720 minutes then block, 90 days then wipe data), maximum PIN attempts then reset/wipe, Play Integrity / device threat level from Mobile Threat Defense.
- Encrypt org data (Android) and backups blocked to personal cloud.

## Conditional Access
Grant control "Require app protection policy" for mobile platforms on Exchange Online,
SharePoint, Teams; block legacy authentication and native mail apps that cannot enforce policy.

## Selective wipe
Intune > Apps > App selective wipe for a user/device removes corporate data from managed apps
only. Also triggered by leaving the company (account disabled) or conditional launch failures.

## Gotchas
- Users with native mail apps or third-party clients bypass MAM: CA must require the policy.
- Screenshot blocking on Android is per app setting; iOS cannot block screenshots.
- Personal and work accounts in the same app (Outlook): policy applies to the work account only; test sharing between accounts.

## Verify
- [ ] Test: copy text from Outlook (work) to WhatsApp is blocked; save attachment to personal storage blocked.
- [ ] Selective wipe removes work data and leaves personal data.
