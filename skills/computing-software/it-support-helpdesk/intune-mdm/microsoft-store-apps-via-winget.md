---
id: computing-software.it-support-helpdesk.intune-mdm.microsoft-store-apps-via-winget
name: microsoft-store-apps-via-winget
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, store-app-winget, microsoft-store-app-new, winget, app-deployment, store-policies, intune]
level: practitioner
status: docs-checked
description: "Deploy Microsoft Store apps from Intune with the Microsoft Store app (new) type: search, System vs User install, auto-update, Store policies that interact, and known errors."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/store-apps-microsoft
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-troubleshoot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# microsoft-store-apps-via-winget

The **Microsoft Store app (new)** type lets admins browse, deploy and monitor Store apps in Intune. The Store supports UWP apps, .msix desktop apps and Win32 apps in .exe or .msi installers (Win32 Store apps are in preview). Devices need at least two cores, must support the Intune Management Extension, and need access to the Store and the destination content.

## Add an app
Apps > All Apps > Create > Microsoft Store app (new) > Search the Microsoft Store app. Search by name, publisher, type or store app ID. Intune searches the United States catalog by default. Paid apps, apps not available in the region, and apps with an ARM64 installer are not supported. Set **Install behavior** to System or User (greyed out means the app supports only one). Assign Required, Available for enrolled devices, or Uninstall.

## Install context
- Microsoft Entra registered devices must use System context. A User-context app assigned as Available shows "Requirements Not Met" in the Company Portal.
- A UWP app deployed in System context is provisioned and installs for each user who signs in; a user-context uninstall still shows installed because it remains provisioned. Microsoft recommends not mixing contexts.
- Assigning a UWP app in System context to a device that already has it can report error 0x87D1041C ("not detected after installation completed successfully") although the app installs.

## Updates
- Intune keeps Store apps up to date. UWP apps update from the Store whether or not assigned, unless Turn off Automatic Download and Install of updates is enabled.
- Win32 Store apps are updated by Intune only while assigned, and are unaffected by the Store update policy. A Required Win32 Store app with a version or context mismatch is reinstalled; an Available one is managed only after the user installs it from the Company Portal.

## Store policies that interact
| Policy | Effect |
|---|---|
| Turn off the Store application (Enabled) | Blocks users installing from the Store app, and manual Store updates. Does not stop Intune installing Store apps, and does not affect winget.exe |
| Allow apps from the Microsoft app store to auto update (AllowAppStoreAutoUpdate) | Keep Not configured or Disabled so UWP updates flow |
| Disable Store originated apps | Recommended Not configured or Enabled per Microsoft's table |
| DesktopAppInstaller EnableMicrosoftStoreSource / EnableAppInstaller | Not built in; need a custom profile. Recommended Not configured or Enabled |
| Only display the private store (RequirePrivateStoreOnly) | Blocks user Store access but lets winget reach the Store; Microsoft prefers Turn off the Store application |

## Troubleshooting
Check the app's install status in Intune and `IntuneManagementExtension.log` and `AppWorkload.log` in `%ProgramData%\Microsoft\IntuneManagementExtension\Logs` (the IME installs the app). Behind a firewall, see the Microsoft Store proxy configuration; third-party Win32 publishers host their own content, so confirm their endpoints.

## Checked
Date: 2026-11-08. Read in full: "Add Microsoft Store Apps to Microsoft Intune" (updated 2026-06-25) and "Troubleshoot Win32 App Issues"; the winget landing page was read for context only. Removed as unconfirmed: that the type is backed by the winget msstore source, the specific endpoint hostnames, the winget log folder, the manual `winget install` test as SYSTEM, LTSC and Server App Installer statements, Store ID format examples, the uninstall detection gotcha, and the Verify command.
Method: documentation only; no commands were run.
