---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-prestage-enrollment
name: jamf-prestage-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf, jamf-pro, jamf-prestage, automated-device-enrollment, apple-ade, apple-business-manager, setup-assistant, enrollment-customization, macos-management]
level: practitioner
status: draft
description: "Configure Jamf Pro PreStage enrollments with Apple Business Manager: device assignment, Setup Assistant skips, account settings, enrollment packages, and failed zero-touch fixes."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_PreStage_Enrollments.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Automated_Device_Enrollment_Integration.html"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-prestage-enrollment

Goal: a new Mac out of the box enrols itself, can't be un-managed, and
reaches the desktop ready to work.

## Prerequisites
- Apple Business Manager (ABM) with an **MDM server** for Jamf; ADE token
  (.p7m) uploaded in Jamf (Settings → Global → Automated Device Enrollment);
  renew yearly.
- Devices assigned to that MDM server in ABM (reseller adds them by order;
  or Apple Configurator for non-reseller Macs).
- Valid APNs certificate.

## PreStage settings that matter
- **Scope**: assign serials to the PreStage (or auto-assign new devices).
- **Require authentication** (SSO/LDAP) to tie the user to the record.
- **Make MDM profile non-removable**; supervision is automatic for ADE.
- **Setup Assistant** panes to skip (Siri, Screen Time, Apple Pay…) — skip
  Location Services only if time zone is set otherwise.
- **Account settings**: create a hidden local admin (management account /
  LAPS-managed), set the user account type (admin vs standard).
- **Enrollment packages**: signed, small (e.g. a Dockutil/Installomator
  bootstrap) — big packages delay Setup Assistant.
- **Enrollment Customization**: branding, SSO login, EULA pane.

## Troubleshooting
| Symptom | Check |
|---|---|
| No "Remote Management" screen at setup | serial not assigned in ABM to Jamf's MDM server, or token expired; device must be on network with access to `*.apple.com` |
| "Unable to connect to the configuration server" | Jamf URL unreachable, proxy/captive portal, APNs cert expired |
| Enrolled but no policies | Enrollment Complete policies scoped wrong; check policy logs |
| Mac was previously in another org's ABM | release from old ABM first |
Re-run ADE on an enrolled Mac: erase (Erase All Content and Settings), or
`sudo profiles renew -type enrollment` for testing.

## Gotchas
- Macs bought outside reseller channels need Apple Configurator to add to
  ABM, with a 30-day provisional period where users can remove management.
- Activation Lock: let Jamf manage the bypass code (ADE-supervised).

## Verify
A wiped test Mac shows Remote Management during setup, lands in Jamf with
the user assigned, MDM profile marked non-removable, and Enrollment
Complete policies show Completed.
