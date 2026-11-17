---
id: computing-software.it-support-helpdesk.desktop-support.office-activation-and-shared-computer-activation
name: office-activation-and-shared-computer-activation
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, office-activation, shared-computer-activation, ospp-vbs, microsoft-365-apps, activation-limit]
level: practitioner
status: docs-checked
description: "Fix Microsoft 365 Apps activation: reset activation state (scripts or manual), clear stale licences with ospp.vbs, and set up shared computer activation for RDS and VDI."
sources:
  - "https://learn.microsoft.com/en-us/microsoft-365/troubleshoot/activation/reset-office-365-proplus-activation-state"
  - "https://learn.microsoft.com/en-us/microsoft-365-apps/licensing-activation/overview-shared-computer-activation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# office-activation-and-shared-computer-activation

Goal: Office stops nagging without the user losing work, and pooled machines activate per user.

## Reset activation state
Reasons to reset: tenant migration, repurposing a device, changing licence mode. Close all Office apps first.
Methods on the reset page (also covers Project and Visio; Windows only):
- Enterprise (command-line) Microsoft Support and Recovery Assistant: scriptable, for many or remote devices.
- Microsoft 365 activation troubleshooter in Get Help (same Windows 10 or later device).
- Scripts: `OLicenseCleanup.vbs` and `signoutofwamaccounts.ps1` (run elevated; the second runs automatically if saved
  beside the first); `WPJCleanUp.cmd` only if the device is Workplace Joined.
- Manual (back up the registry first):
  - Delete licence tokens in `%localappdata%\Microsoft\Office\Licenses` (vNext, version 1909 or later) and
    `%localappdata%\Microsoft\Office\16.0\Licensing` (shared computer activation).
  - Legacy licences: from `...\Office16` run `cscript ospp.vbs /dstatus`, then
    `cscript ospp.vbs /unpkey:<last 5 characters of the key>` for each one; delete
    `HKCU\Software\Microsoft\Office\16.0\Common\Licensing`.
  - Delete `HKCU\Software\Microsoft\Office\16.0\Common\Identity` (for shared computer activation, the same key under
    `HKEY_USERS\<SID>`; `whoami /user` gives the SID).
  - Remove Office entries in Control Panel > Credential Manager > Windows Credentials.
  - On Microsoft Entra joined or hybrid joined devices WAM accounts cannot be cleared by hand: run the script.
    `dsregcmd /status` shows AzureAdJoined, EnterpriseJoined and DomainJoined (YES/NO/NO = Entra joined,
    YES/NO/YES = hybrid joined).
  - Clearing a Workplace Joined account (Settings > Accounts > Access work or school > Disconnect) removes SSO for
    the session and unenrols the device from management.

## Shared computer activation (RDS, AVD, shared PCs)
- Required where several users sign in to the same computer with their own accounts. Does not count against the
  normal device limit (for example 5 PCs). Not available for Office for Mac.
- Plans: any plan including Microsoft 365 Apps for enterprise, plans with desktop Project or Visio, Education plans
  with Apps for enterprise, and Microsoft 365 Business Premium (the only business plan). Each user needs a licence.
- Enable at install with the Office Customization Tool "Shared Computer" option or
  `<Property Name="SharedComputerLicensing" Value="1" />` in the ODT configuration. After install: Group Policy "Use
  shared computer activation" (not supported for Apps for business), or a REG_SZ `SharedComputerLicensing` = 1 under
  `HKLM\SOFTWARE\Microsoft\Office\ClickToRun\Configuration`, or Support and Recovery Assistant. Reboot required.
  Users who already activated must have activation reset.
- Each user gets a licence token per computer, stored in the user profile; it is valid for 30 days and renews while
  the user is signed in and using Office; reliable internet access to the Office Licensing Service is needed.
- Unlicensed users or a closed Activate dialog give reduced functionality mode (view and print only).
- Token roaming (version 1704 and later) for non-persistent VDI: set `SCLCacheOverride` = 1 and
  `SCLCacheOverrideDirectory` to a per-user folder (registry string values, ODT properties, or the Group Policy
  "Specify the location to save the licensing token"). A network share can add latency. Default location is
  `%localappdata%\Microsoft\Office\16.0\Licensing`. Single sign-on is recommended to reduce prompts.

## Verify
The user shows as activated after restarting Office, and on shared computer activation machines the token exists in the
user's Licensing folder.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the reset-activation and shared computer activation articles. The cited unlicensed-product page returned
404 and was dropped. Removed as not stated on the pages: File > Account checks, 5 tablets and 5 phones, E1/F3 licence
claims, vNextDiag, and Credential Manager entry names.
