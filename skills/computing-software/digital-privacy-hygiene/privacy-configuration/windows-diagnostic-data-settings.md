---
id: computing-software.digital-privacy-hygiene.privacy-configuration.windows-diagnostic-data-settings
name: windows-diagnostic-data-settings
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, windows-diagnostic-data, telemetry, windows, privacy-settings, group-policy, advertising-id]
level: practitioner
status: docs-checked
description: "Minimise Windows diagnostic data: Required-only level, the Diagnostic Data Viewer, and the Allow Diagnostic Data Group Policy and MDM values, with edition limits."
sources:
  - "https://learn.microsoft.com/en-us/windows/privacy/configure-windows-diagnostic-data-in-your-organization"
  - "https://learn.microsoft.com/en-us/windows/privacy/diagnostic-data-viewer-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows diagnostic data settings

**Goal:** send Microsoft the minimum diagnostic data your edition allows, and know how to see what is sent.

## The levels (Microsoft Learn, "Configure Windows diagnostic data in your organization")
- **Diagnostic data off (Security)**: no Windows diagnostic data is sent. Available only on Windows Server, Enterprise
  and Education editions. If you rely on Windows Update, Microsoft's minimum recommended setting is Required, because
  no Windows Update information (such as update failures) is collected when it is off.
- **Required (Basic)**: the minimum data to keep the device secure, up to date and performing as expected (device
  attributes, quality metrics, compatibility and driver data, Microsoft Store performance). Crash metadata but no
  crash dumps or diagnostic logs. This is the default for Windows 10 version 1903 and later.
- **Optional (Full)**: adds app activity, browser activity in Microsoft browsers (including history and search terms),
  enhanced error reporting with memory state (may contain user content), and diagnostic logs.
- Enhanced exists only on Windows 10 1809 and earlier and Windows Server 2016/2019; not on Windows 11.

## Settings app
Settings > Privacy & security > Diagnostics & feedback. Choose Required only (do not send optional diagnostic
data) and review the other toggles on that page, such as tailored experiences. Learn notes that tailored experiences
use diagnostic data, and crash data is never used for it. Which toggles appear varies by Windows version, so read the
page itself rather than a fixed list.

## See what is sent: Diagnostic Data Viewer
- Install the Diagnostic Data Viewer app from the Microsoft Store (for PowerShell on Windows Server, use the
  Microsoft.DiagnosticDataViewer module, elevated session).
- Settings > Privacy & security > Diagnostics & feedback > under View diagnostic data, turn on the Diagnostic Data
  Viewer option. This stores diagnostic data until you turn it off and can use up to 1 GB of system-drive space by
  default (default history: 1 GB or 30 days, whichever comes first). Turn it off when done; that also clears the
  stored Windows data history.
- Open Diagnostic Data Viewer to see each event as JSON, search, filter by category, and Export data to CSV.
  An event shown may still be queued, not yet uploaded.
- The Feedback Hub is publicly viewable, so put no personal information in feedback.

## Policy (Group Policy or MDM)
Group Policy: Computer Configuration > Administrative Templates > Windows Components > Data Collection and Preview
Builds > **Allow diagnostic data** (called Allow telemetry on Windows 10 1809 and earlier and Windows Server 2019).
Values: 0 Diagnostic data off (Security), 1 Required (Basic), 2 Enhanced, 3 Optional (Full). When Computer and User
Configuration policies both exist, the more restrictive applies. On Windows 10 1803 and later, a user can still set a
more restrictive level in Settings unless the "Configure diagnostic data opt-in settings user interface" policy is set.
MDM: Policy CSP `System/AllowTelemetry`; `System/LimitDumpCollection` and `System/LimitDiagnosticLogCollection`
are Windows 11 and Windows Server 2022 only. Group Policy also has Limit dump collection and Limit diagnostic log
collection.

These settings cover only Windows components; third-party apps and other Microsoft apps (such as Microsoft 365 Apps)
have their own controls. Other Windows connections are covered by "Manage connections from Windows operating system
components to Microsoft services".

## Practical caution (not from the cited pages)
Avoid "debloat" scripts from random repositories; use the documented settings above.

## Verify
- [ ] Diagnostics & feedback shows optional diagnostic data off.
- [ ] Diagnostic Data Viewer turned off again after inspection.

## Checked
Checked 2026-11-08 against the full text of both Microsoft Learn pages. The generic support.microsoft.com Windows
landing page was dropped from sources (it holds no relevant content). Removed what the pages do not state: the
registry path, the claim that value 0 acts as Required on Home/Pro, the advertising ID, inking and typing, feedback
frequency and delete-diagnostic-data toggles, and the registry verification command.
Method: documentation only; no commands were run.
