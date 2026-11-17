---
id: computing-software.general-digital-literacy.web-browsers.installing-a-site-as-an-app
name: installing-a-site-as-an-app
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, bookmarks, install-web-app, progressive-web-app, desktop-shortcut]
level: intro
status: docs-checked
description: "Install websites as apps with Chrome and Edge so they open in their own window: install, shortcuts, start at login, update warnings and uninstall."
sources:
  - https://support.google.com/chrome/answer/9658361
  - https://support.google.com/chrome/answer/15085120
  - https://support.microsoft.com/en-us/edge/install-manage-or-uninstall-apps-in-microsoft-edge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install a site as an app

## Chrome (computer)
- **Install:** open the site > More > Cast, save, and share > **Install page as app...** (on some sites an **Install** button also shows at the right of the address bar), then follow the prompts.
- **Shortcut only:** More > Cast, save, and share > **Create shortcut...**, name it, Create.
- **Manage:** `chrome://apps`. Right-click an app to Create shortcut (choose where) or tick **Launch at startup** (Windows, Mac, Linux). Inside the app: More > App info > Settings.
- **Uninstall:** open the app > More > Uninstall [app name] > Remove; tick "Also delete data from Chrome" to remove its data.
- **Update warning:** when an app wants to change its name or icon, Chrome shows "App update available". Chrome says that if you suspect a malicious change, such as a name or icon that now resembles another app, uninstall it. You can Update, Ignore or Uninstall.

## Edge
- Go to the site. If it is a PWA, Edge offers to install it; otherwise Settings and more > More tools > Apps > **Install this site as an app**.
- Installed apps are listed at `edge://apps`: Open, Details (turn on Auto-start on device login, Pin to taskbar, Pin to Start, Create Desktop shortcut) and Uninstall (optionally delete app history and data).

## Notes
Web apps can offer extras such as offline use, notifications, file access and icon badges, though some may not work fully offline.

## Verify
- [ ] The app opens in its own window from the taskbar, Start or Dock.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Use web apps" and "Create shortcuts for websites in Chrome"; Microsoft Support "Install, manage, or uninstall apps in Microsoft Edge", read in October 2026. Confirmed: install, shortcut, manage, startup, uninstall and update-warning steps. Removed as unconfirmed: Safari Add to Dock, iPhone and Android Add to Home Screen, the "Open as window" tick box, and the claim that uninstalling needs more than deleting the desktop shortcut.
Method: documentation only; no commands were run.
