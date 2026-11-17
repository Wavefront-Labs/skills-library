---
id: computing-software.general-digital-literacy.web-browsers.guest-mode-and-public-computers
name: guest-mode-and-public-computers
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, profiles, guest-mode, public-computer, shared-computer, sign-out-everywhere, inprivate, incognito, library-computer]
level: intro
status: docs-checked
description: "Browse on shared or public computers with Chrome Guest mode or Incognito, avoid leaving accounts behind, and know what private modes do not hide."
sources:
  - https://support.google.com/chrome/answer/6130773
  - https://support.google.com/chrome/answer/95464
  - https://support.microsoft.com/en-us/microsoft-edge/browse-inprivate-in-microsoft-edge-cd2c9a48-0bc4-b98e-5e46-ac40c84e27e2
  - https://support.microsoft.com/en-us/microsoft-edge/keyboard-shortcuts-in-microsoft-edge-50d3edab-30d9-c7e4-21ce-37fe2713cfad
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guest mode and public computers

**Goal:** use a computer that is not yours without leaving your accounts behind.

## On a shared family or work computer
- **Chrome:** click **Profile** (top right) > **Open Guest profile**. Guest mode cannot see or change any other Chrome profile's info; when you close it, your browsing history, cookies and site data are deleted. Not available on Chromebooks; Ctrl+Shift+M (Mac Cmd+Shift+M) opens the profile menu where Guest is offered.
- **Edge:** Ctrl+Shift+M (Mac Command+Shift+M) is listed as "sign in as a different user or browse as a Guest".
- For regular users, give each person their own operating-system account or browser profile.

## On a library, hotel or internet-cafe computer
1. Chrome says to use Guest mode for a public computer, and to log in to sensitive sites only on trusted devices; avoid banking and other sensitive sign-ins on a public machine.
2. A private window (Chrome Incognito `Ctrl+Shift+N`; Edge InPrivate `Ctrl+Shift+N`; Mac Cmd+Shift+N) is the alternative: Chrome does not sign you in automatically and does not keep the sites you visited when all Incognito windows are closed; Edge deletes browsing history, cookies, site data, passwords and form data when you close all InPrivate windows.
3. Decline any "Save password?" or "Stay signed in" prompt, then **sign out** of every site before closing.
4. Close all Guest or private windows when you finish: a private session only ends when every private window is closed.

## What private modes do not hide
- Websites you visit and sign in to, your employer or school, whoever runs the network, and your internet provider may still see your activity (Chrome Guest and Incognito pages; Edge says school, workplace and provider may still access the data).
- Files you download stay on the computer until deleted, and bookmarks you save are kept (Chrome Incognito; Edge keeps favorites and downloaded files).
- Edge InPrivate does not make you safer from malicious sites or add ad blocking.

## Verify
- [ ] After closing the window, reopening the site shows you signed out.

## Checked
2026-10-27. Chrome Help (Browse Chrome as a guest; Browse in Incognito mode), Microsoft's Edge InPrivate page and Edge keyboard shortcuts page were read. Confirmed the Guest and private-window steps, the Ctrl+Shift+M and Ctrl+Shift+N shortcuts, what is deleted on close and what stays visible. Firefox private windows and account sign-out-everywhere paths are not covered because they could not be confirmed. Method: documentation only; no commands were run.
