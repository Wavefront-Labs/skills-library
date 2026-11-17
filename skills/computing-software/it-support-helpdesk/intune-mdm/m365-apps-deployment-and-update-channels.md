---
id: computing-software.it-support-helpdesk.intune-mdm.m365-apps-deployment-and-update-channels
name: m365-apps-deployment-and-update-channels
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, m365-apps-deployment, microsoft-365-apps, office-deployment-tool, update-channels, monthly-enterprise-channel, click-to-run, intune]
level: practitioner
status: docs-checked
description: "Deploy Microsoft 365 Apps with Intune: configuration designer vs ODT XML, Current vs Monthly Enterprise vs Semi-Annual channels, Remove MSI, ESP caveat, and install failure codes."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-add-office365
  - https://learn.microsoft.com/en-us/microsoft-365-apps/updates/overview-update-channels
  - https://learn.microsoft.com/en-us/microsoft-365-apps/deploy/office-deployment-tool-configuration-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# m365-apps-deployment-and-update-channels

## Two ways to configure the Intune app
Apps > All Apps > Create > Microsoft 365 Apps, Windows 10 and later. Step 2 offers a **Configuration designer** or **Enter XML data**.
- Microsoft 365 Apps for business (`O365BusinessRetail`) can be configured only with XML; enterprise is `O365ProPlusRetail`.
- Configuration designer settings include architecture (64-bit installs on 64-bit devices only), update channel, Remove other versions, version to install, shared computer activation, auto-accept EULA and languages.
- Only one Microsoft 365 deployment is delivered to a device. Not supported on Windows Home, Team or Holographic. Installing the Store (Centennial) Office on a device already deployed through Intune can cause data loss.
- If any Microsoft 365 app is open during install, the install might fail and users could lose unsaved work.

Example XML (attributes per the ODT configuration options page):
```xml
<Configuration>
  <Add OfficeClientEdition="64" Channel="MonthlyEnterprise" MigrateArch="TRUE">
    <Product ID="O365ProPlusRetail">
      <Language ID="MatchOS" Fallback="en-us" />
      <ExcludeApp ID="Groove" /><ExcludeApp ID="Lync" />
    </Product>
  </Add>
  <Property Name="SharedComputerLicensing" Value="0" />
  <Property Name="FORCEAPPSHUTDOWN" Value="TRUE" />
  <Updates Enabled="TRUE" />
  <RemoveMSI />
  <Display Level="None" AcceptEULA="TRUE" />
</Configuration>
```
`MigrateArch` defaults to False; `FORCEAPPSHUTDOWN` defaults to FALSE and TRUE can cause data loss; `SharedComputerLicensing` defaults to 0 and 1 is for Remote Desktop Services shared computers. `Groove` excludes OneDrive and `Lync` excludes Skype for Business. ODT cannot be used to install OneDrive through Intune.

## Channels
Microsoft names three primary channels. Per the channels page:
| Channel | Feature updates |
|---|---|
| Current | As soon as ready, about monthly, no set schedule |
| Monthly Enterprise | Second Tuesday of the month, predictable |
| Semi-Annual Enterprise | January and July, second Tuesday |
Security updates for all three are on the second Tuesday when needed. The page carries a notice that changes begin July 2026: Semi-Annual Enterprise will receive feature and security updates monthly, on the same basis as Monthly Enterprise. Read the linked unification article before choosing Semi-Annual. ODT `Channel` values: `CurrentPreview`, `Current`, `MonthlyEnterprise`, `SemiAnnualPreview`, `SemiAnnual`. Monthly Enterprise has no dedicated preview channel.

## Where channel is set
The Office Group Policy setting Update Channel (Computer Configuration > Policies > Administrative Templates > Microsoft Office 2016 (Machine) > Updates) takes precedence over the ODT Channel. Microsoft also warns that settings-catalog settings that conflict with the app deployment, such as Update Channel and version, can cause unexpected behaviour including reinstallation. Pick one source.

## Failures
- Existing `.msi` Office blocks the install; use Remove other versions (RemoveMSI), which removes all Office MSI apps, not just the selected ones.
- Intune initiated the deployment if the folders Microsoft Office and Microsoft Office 15 appear in Program Files; watch `%ProgramFiles%\Microsoft Office\Updates\Download` grow to confirm the download.
- Custom ODT XML install status reflects only the install attempt, not whether the app is currently installed.
- Verbose logs: `reg add HKLM\SOFTWARE\Microsoft\ClickToRun\OverRide /v LogLevel /t REG_DWORD /d 3`, redeploy, wait 15 to 20 minutes, read `{Machine Name}-{TimeStamp}.log` in `%temp%` and `%windir%\temp`, then `reg delete HKLM\SOFTWARE\Microsoft\ClickToRun\OverRide /v LogLevel /f`.
- Codes: 1603 failed prerequisite (MSI present, or 64-bit over 32-bit), 17002 cancelled or out of disk space, 17004 unknown SKU, 1460 ODT download timeout, 997 installing, 0 success.
- With Autopilot and the ESP, Microsoft recommends deploying Microsoft 365 Apps as a Win32 app, because the app type is not managed by the IME and can run concurrently with a tracked Win32 install, failing the ESP.

## Checked
Date: 2026-11-08. Read in full: "Add Microsoft 365 Apps to Windows Devices Using Microsoft Intune" (updated 2026-04-23), "Overview of update channels for Microsoft 365 Apps" (channel table and notice) and "Configuration options for the Office Deployment Tool". Corrections: the channels page now announces the Semi-Annual unification from July 2026; Semi-Annual (Preview) schedule removed. Removed as unconfirmed: the Win32 setup.exe /configure approach, the settings catalog path and Cloud Update, the OfficeC2RClient.exe update command, error 0-1018, Visio and Project licensing advice, and the Word File > Account verify step.
Method: documentation only; no commands were run.
