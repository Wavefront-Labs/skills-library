---
id: computing-software.digital-privacy-hygiene.privacy-configuration.controlling-windows-recall
name: controlling-windows-recall
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, windows-recall, copilot-plus-pc, windows, snapshots, ai-tools, group-policy]
level: practitioner
status: docs-checked
description: "Decide on and configure Windows Recall on Copilot+ PCs: keep snapshots off, filter apps and sites, remove the feature, and block it by policy."
sources:
  - "https://support.microsoft.com/windows"
  - "https://learn.microsoft.com/en-us/windows/client-management/manage-recall"
  - "https://learn.microsoft.com/en-us/windows/ai/recall/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling Windows Recall

**Goal:** Recall saves periodic screenshots ("snapshots") of what is on screen so you can search your history with
natural language. Decide whether that record should exist on this PC.

## Facts
- Copilot+ PCs only. Saving snapshots is **opt-in** and needs the user's consent; on unmanaged PCs the user decides
  for each account, and on managed devices Recall is removed by default unless IT allows it.
- Snapshots are stored and analysed locally, are not sent to Microsoft, and are always encrypted. Opening Recall and
  viewing snapshots needs Windows Hello with Enhanced Sign-in Security and at least one biometric option.
- Snapshots are taken periodically while the screen content changes. They capture whatever is visible, so other
  people's messages, documents and chats can be included.
- Not saved: DRM content, audio, continuous video, game video in Game Mode, and (with a supported browser) private
  browsing. Windows, apps and some remote desktop clients can exclude their windows from capture.
- **Sensitive information filtering** is on by default and skips snapshots where potentially sensitive information is
  detected. It is a filter, not a guarantee.
- Saving pauses once free storage falls under 25 GB. Websites are filtered only when in the foreground tab, so parts of
  a filtered site can still appear in snapshots.

## Configure (user)
Settings > Privacy & security > **Recall & snapshots**:
- Leave **Save snapshots** off unless you want the feature.
- Add apps and websites to the filter lists (a supported browser is needed for website filtering: Edge, Firefox,
  Opera, Chrome; other Chromium 124+ browsers filter private browsing only).
- Keep sensitive information filtering on.
- Use the page's options to pause, delete snapshots and manage storage.

## Remove or block
- Remove the component (admin PowerShell):
  `Disable-WindowsOptionalFeature -Online -FeatureName "Recall" -Remove`
- Group Policy, Computer Configuration > Administrative Templates > Windows Components > Windows AI:
  **Allow Recall to be enabled** = Disabled removes the Recall component (needs a restart); previously saved snapshots
  are deleted.
- **Turn off saving snapshots for Recall** = Enabled (also available under User Configuration; CSP setting
  `DisableAIDataAnalysis`) stops snapshots being saved; existing snapshots are deleted.
- Admins cannot turn saving on for users.

## For people you talk to
If correspondents use Recall, what you send them can end up in their snapshots. Ask high-risk contacts to add
messaging apps to their Recall filter list.

## Verify
- [ ] Recall off or removed, or the filter list covers every sensitive app and site; old snapshots deleted.

## Checked
Date: 2026-11-08.
Confirmed against the Learn pages "Manage Recall" (opt-in, local and encrypted storage, Windows Hello ESS, sensitive
information filtering default, supported browsers, 25 GB pause, policy names, paths and DisableAIDataAnalysis,
Disable-WindowsOptionalFeature command, DRM/audio/game exclusions) and "Recall overview". Removed: the Dism command,
the Optional features menu path, the registry key path, the Signal Desktop and disappearing-message claims, the malware
and PIN risk claim, and the user-level delete-by-time-range and storage-limit detail (not on the cited pages).
The support.microsoft.com/windows landing page was only a general entry point.
Method: documentation only; no commands were run.
