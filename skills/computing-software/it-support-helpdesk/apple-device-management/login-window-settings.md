---
id: computing-software.it-support-helpdesk.apple-device-management.login-window-settings
name: login-window-settings
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, login-window, login-window-settings, macos, loginwindow]
level: practitioner
status: docs-checked
description: "Control the macOS login window with the com.apple.loginwindow payload: user list, banner text, shutdown buttons, auto-login and FileVault options, with verified key names."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.loginwindow.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# login-window-settings

Goal: control the login experience on managed Macs.
- Payload `com.apple.loginwindow` (macOS 10.7 and later, device channel only, not allowed with User Enrolment). Multiple instances are allowed.
- User list: `SHOWFULLNAME` (true shows the name and password dialog, false shows a list of users), `HideLocalUsers` (true shows only network and system users), `HideAdminUsers`, `HideMobileAccounts`, `IncludeNetworkUser`, `SHOWOTHERUSERS_MANAGED` (shows "Other..."). All default false.
- Text and hints: `LoginwindowText` (text shown in the login window), `RetriesUntilHint` (0, the default, shows no hint), `AdminHostInfo` (toggles computer information in the menu bar time area), `showInputMenu` (from 10.8).
- Buttons and menu items: `ShutDownDisabled`, `RestartDisabled`, `SleepDisabled`, `ShutDownDisabledWhileLoggedIn`, `RestartDisabledWhileLoggedIn`, `PowerOffDisabledWhileLoggedIn`, `LogOutDisabledWhileLoggedIn` (10.13), `DisableScreenLockImmediate` (10.13).
- FileVault and auto login: `DisableFDEAutoLogin` (from 10.9) disables the automatic login option when using FileVault. `AutologinUsername` and `AutologinPassword` (macOS 14 and later) set up auto login for an existing user; the password must match that user's current password.
- Other: `DisableConsoleAccess` makes the system disregard the `>console` user name; `AllowList` and `DenyList` take user or group GUIDs, apply only to network and mobile accounts, and the deny list wins; `AdminMayDisableMCX` lets a local administrator bypass managed preferences for their session.
Gotcha: `HideLocalUsers` hides local accounts, including a local break-glass admin, from the list, so record that account's short name and consider `SHOWFULLNAME` (name and password dialog) or `SHOWOTHERUSERS_MANAGED` ("Other...").
Verify: the configured `LoginwindowText` appears in the login window on a test Mac.

## Checked

Date: 2026-11-07. Read in full: apple/device-management `com.apple.loginwindow.yaml` lines 1 to 219 (all keys through `ForceCaptivePortalConnectionFromLockScreen`; the last two macOS 27 keys were left out). Removed: the Jamf Connect pairing, remote-support-tool testing advice, "lock screen message for lost devices" (a different payload), and the claim that defaults can change after major upgrades.
Method: documentation only; no commands were run.
