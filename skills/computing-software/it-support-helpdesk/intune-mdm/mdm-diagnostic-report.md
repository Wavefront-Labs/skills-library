---
id: computing-software.it-support-helpdesk.intune-mdm.mdm-diagnostic-report
name: mdm-diagnostic-report
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mdm-diagnostic-report, mdmdiagnosticstool, mdm-diagnostics, intune-troubleshooting, windows-mdm]
level: practitioner
status: docs-checked
description: "Generate and read the Windows MDM diagnostic report: Settings Create report, the mdmdiagnosticstool zip and its files, Event Viewer MDM channels and remote log collection."
sources:
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm-collect-logs"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/collect-diagnostics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mdm-diagnostic-report

When Intune says a policy applied but the device behaves otherwise, the device's own MDM
logs settle it. Applies to Windows 11 and Windows 10.

## Quick report (the user can do it)
Settings > Accounts > Access work or school > select the work or school account > **Info**
> **Create report** (bottom of the page). A window shows the log path; select **Export**,
then look in the `MDMDiagnostics` folder under Public Documents.

## Command-line collection
The page gives this form:
```
mdmdiagnosticstool.exe -area "DeviceEnrollment;DeviceProvisioning;Autopilot" -zip "%PUBLIC%\Documents\MDMDiagReport.zip"
```
The report is also written to the `MDMDiagnostics` folder under Public Documents. The zip holds
logs for the areas you named. For the three areas above it contains:
- `DiagnosticLogCSP_Collector_Autopilot_*`: Autopilot ETLs.
- `DiagnosticLogCSP_Collector_DeviceProvisioning_*`: provisioning ETLs
  (Microsoft-Windows-Provisioning-Diagnostics-Provider).
- `MDMDiagHtmlReport.html`: snapshot of MDM configuration and policies, including
  management URL, MDM server device ID, certificates and policies.
- `MdmDiagLogMetadata.json`: the command-line arguments used.
- `MDMDiagReport.xml`: more detail, such as enrollment variables, provisioning packages
  and multivariant conditions.
- `MdmDiagReport_RegistryDump.reg`: dumps of common MDM registry locations.
- `MdmLogCollectorFootPrint.txt`: the tool's own log.
- `*.evtx`: event logs; `microsoft-windows-devicemanagement-enterprise-diagnostics-provider-admin.evtx`
  is the main one for MDM events.

## Event Viewer directly
- Path: Applications and Services Logs > Microsoft > Windows >
  DeviceManagement-Enterprise-Diagnostic-Provider. The **Admin** channel logs by default;
  for more detail use View > **Show Analytic and Debug logs**, right-click **Debug** and
  **Enable Log**.
- To save: right-click the node > **Save all events as**, pick a location, then choose
  English under "Display information for these languages".
- When viewing logs from another machine, use a PC or VM on the same OS build as the
  source. Open the file with Event Viewer > Open Saved Log, then filter Event sources by
  DeviceManagement-EnterpriseDiagnostics-Provider.

## Remote collection through MDM
If the MDM server supports it, the DiagnosticLog CSP can enable and export the channels
`Microsoft-Windows-DeviceManagement-Enterprise-Diagnostics-Provider%2FAdmin` and `%2FDebug`
(for example `./Vendor/MSFT/DiagnosticLog/EtwLog/Channels/<channel>/State` set to
`true`, and `.../Export`). Device state can be snapshotted with
`./Vendor/MSFT/DiagnosticLog/DeviceStateData/MdmConfiguration` and data `SNAP`; files are
retrieved via the CSP's FileDownload node.

## Practical use
- Intune's **Collect diagnostics** remote action covers the same ground without the user
  (see collect-diagnostics-remote-action).
- The reports contain device and user identifiers; treat them as internal data.
- Sync the device before creating the report so it is a current snapshot.

## Checked
Date: 2026-11-07. Read in full: Windows "Collect MDM logs" (Settings Create report, command, zip structure, Event Viewer,
remote collection, view logs, device state data) and the Intune Collect diagnostics page (for the cross-reference). Removed as
unconfirmed or contradicted: the `-cab` and `-out` forms (page uses `-zip`), the `TPM` area, `HKLM\SOFTWARE\Microsoft\MdmDiagnostics\Area`,
`MDMDiagReport.html` in `%PUBLIC%` described as the quick-report file name, the PolicyManager registry-reading section, example error
-2016281112, `MDMWinsOverGP`, the Enterprise/Education edition claim, and the Verify step. Page lists "diagnose-mdm-failures-in-windows-10"
as an old URL that redirects to this same article, so it was dropped from sources.
Method: documentation only; no commands were run.
