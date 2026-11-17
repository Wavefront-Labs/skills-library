---
id: computing-software.digital-privacy-hygiene.device-hardening.clipboard-access-prompts
name: clipboard-access-prompts
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, clipboard-access, app-permissions, paste-permission, clipboard-history]
level: practitioner
status: draft
description: "Control which apps can read the clipboard on iOS, Android and Windows, use paste prompts and history settings, and keep copied passwords from lingering."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://developer.android.com/develop/ui/views/touch-and-input/copy-paste"
  - "https://support.microsoft.com/windows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Clipboard access prompts and notifications

**Goal:** stop apps silently reading what you copy (passwords, addresses, 2FA codes).

## iOS / iPadOS
- iOS shows a banner "App pasted from Other App" when an app reads the clipboard.
- iOS 16+: apps ask **Allow Paste**. Per app: Settings > Apps > [app] > **Paste from Other Apps** = Ask / Deny /
  Allow. Set Ask or Deny for apps that have no reason to read it.
- Universal Clipboard shares the clipboard with your other Apple devices nearby; turn off Handoff if unwanted.

## Android
- Android 12+ shows a toast "[app] pasted from your clipboard".
- Android 13+ clears the clipboard automatically after about an hour and hides content flagged as sensitive (password
  managers mark copied passwords) in the preview.
- Gboard clipboard history: open the clipboard in Gboard and turn it off, or clear pinned items.

## Windows
Settings > System > **Clipboard**: turn off **Clipboard history** and **Sync across devices** (cloud clipboard
sends copied text to Microsoft). Win+V shows and clears history.

## Password managers
Set the clipboard clear timer (Bitwarden: Settings > Clear clipboard; KeePassXC: Settings > Security > Clear
clipboard after N seconds). Prefer autofill over copy/paste entirely.

## Gotchas
- Clipboard hijacking malware swaps copied crypto addresses; always check the first and last characters after pasting.
- Remote desktop and VM tools share the clipboard with the host; disable when connecting to untrusted machines.
