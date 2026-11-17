---
id: computing-software.it-support-helpdesk.intune-mdm.company-portal-app-and-troubleshooting-pane
name: company-portal-app-and-troubleshooting-pane
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, company-portal-app-support, company-portal-logs, troubleshooting-pane, company-portal, user-troubleshooting]
level: practitioner
status: docs-checked
description: "Support users in the Intune Company Portal: customization limits, self-service device actions, Android log upload, and the Troubleshooting + support pane tabs."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/company-portal-app"
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/help-desk-operators"
  - "https://learn.microsoft.com/en-us/mem/intune/user-help/send-logs-to-your-it-admin-by-email-android"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# company-portal-app-and-troubleshooting-pane

## Company Portal customization (Tenant administration > Customization)
- Edit the default policy or create up to 25 user-group-targeted policies; device-group
  targeting is not supported. Settings apply to the Company Portal apps, the website and
  the Intune app on Android.
- Branding limits: organization name max 40 characters; logos PNG/JPG/JPEG, max 750 KB,
  recommended height over 72 px; brand image max 1.3 MB, recommended width over 1125 px.
- Support information max lengths: contact name 40, phone 20, email 40, website name 40,
  website URL 150, additional information 120. Privacy statement URL max 79.
- Device enrollment prompts: Available with prompts (default), Available no prompts, or
  Unavailable (no way to enroll; apps requiring enrollment are hidden). The setting needs
  iOS/iPadOS Company Portal 4.4+ or Android 5.0.5421.0+; it does not apply to iOS/iPadOS
  Automated Device Enrollment devices but does apply to Android Knox Mobile Enrollment.
- App sources: Entra Enterprise Applications, Office Online Applications and Configuration
  Manager applications can be shown or hidden. Configuration Manager apps show only in the
  Windows Company Portal.
- The Remove and Reset buttons for corporate Windows and iOS/iPadOS devices can be hidden
  (default Customization policy only, not group-targeted ones); this does not apply a
  device restriction policy.

## Self-service actions (primary user only)
Retire (shown as Remove), Wipe (Reset / Factory Reset on iOS), Rename (changes only the
Company Portal listing), Sync (shown as Check Status), Remote Lock, Reset Passcode, Key
Recovery (macOS, web portal only). Limits from the page: Retire is always blocked on Entra
joined Windows; all remote actions are disabled for Device Enrollment Manager enrollments;
Wipe is unavailable on User Enrolled iOS/iPadOS; Automated Device Enrollment iOS/iPadOS
devices have Retire and Wipe disabled; Android Enterprise Device Owner scenarios (COPE,
COBO, COSU) do not offer Retire or Wipe.

## Collecting Android logs
- Company Portal: Menu > Help > **Send logs** (or tap HELP / SEND INFO on an error), then
  SEND LOGS, THEN EMAIL. An email opens with an incident ID in the subject; SEND LOGS ONLY
  skips the email. The send-logs option is unavailable in sovereign clouds, so send by
  email instead.
- Microsoft Intune app: Menu > Help > Get Support > UPLOAD LOGS > EMAIL.
- Save logs locally: Company Portal > Settings > SAVE LOGS (needs a file viewing app,
  inside the work profile on work-profile devices).
- Logs are also shared with Microsoft Support; quote the incident ID to the support person.
- Admins can download user-submitted logs for Android, AOSP and Windows Company Portal
  under Troubleshooting + support > Diagnostics (needs the Collect diagnostics permission).

## Troubleshooting + support pane
Intune admin center > **Troubleshooting + support > Troubleshoot**, find a user by display
name or email, filter by device if needed. Tabs: Summary (counts for policy, compliance,
app protection, applications, devices, roles and scopes), Devices (OS, compliance, last
check-in), Groups, Policy, Applications, App protection policy, Updates, Enrollment
restrictions, Diagnostics, ServiceNow incidents.
- Use it for "why does this user not get X": compare Policy and Applications assignment
  against Groups membership.
- Assign the built-in **Help desk operator** role to help desk staff instead of Intune
  administrator; certain enrollment issues are not captured and some errors have no
  remediation suggestion.

## Checked
Date: 2026-11-07. Read in full: Company Portal configuration page (customization, branding and support tables, enrollment options,
app sources, self-service actions table and footnotes, app logs), "Use the troubleshooting dashboard to help users" (all tabs) and
"Report a problem in Company Portal or Intune app for Android". Removed as unconfirmed: the symptom/fix table (empty app list,
"Couldn't identify device"), iOS "Send logs" and macOS "Save diagnostic report" menu paths, Windows "Settings > Diagnostic logs",
the "featured apps" customization, and the Verify step. Platform list and feature claims were trimmed to what the pages state.
Method: documentation only; no commands were run.
