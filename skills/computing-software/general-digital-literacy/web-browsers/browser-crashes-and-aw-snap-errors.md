---
id: computing-software.general-digital-literacy.web-browsers.browser-crashes-and-aw-snap-errors
name: browser-crashes-and-aw-snap-errors
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, browser-crash, aw-snap, edge-repair]
level: intro
status: docs-checked
description: "Fix Chrome Aw Snap page crashes and loading errors, and Edge that crashes or will not open: free memory, extensions, update, repair, reset or reinstall."
sources:
  - https://support.google.com/chrome/answer/95669
  - https://support.google.com/chrome/answer/6098869
  - https://support.google.com/chrome/answer/1385029
  - https://support.microsoft.com/en-us/edge/what-to-do-if-microsoft-edge-isn-t-working
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Browser crashes and Aw Snap errors

## One page: "Aw, Snap!" in Chrome
Chrome's help lists "Aw, Snap!" as Chrome having problems loading the page. If other sites open normally but one site crashes, the site may be the cause: report it to the site owner. Chrome's full list of error codes is at `chrome://network-errors/`.

## Steps for Chrome (in the order Chrome's help gives them)
1. Check the address for mistakes and reload the page. See whether one site or many are affected.
2. Check the internet connection (Wi-Fi or ethernet, modem and router).
3. Update Chrome (More > Help > About Google Chrome > Relaunch), then restart it.
4. Open the page in an Incognito window. If it works there, an extension or stored data is the cause.
5. Turn off all extensions (More > Extensions > Manage extensions); re-enable them one at a time.
6. Delete browsing data (cookies, cache). This signs you out of sites, so note what you need first.
7. Check that a firewall or antivirus is not blocking Chrome.
8. Free memory: close unused tabs; More > More tools > Task Manager, sort by Memory, select a task, End process (unsaved work in that task is lost).
9. Reset Chrome settings to default (see the resetting-browser-settings skill).
10. Reinstall Chrome. Signed-in Chrome keeps your saved info in your Google Account.

## Microsoft Edge that crashes, closes or will not open
Microsoft's help suggests, in this spirit:
- Close other tabs and apps, pause downloads, uninstall extensions you do not need, then reload.
- Update: Settings and more > Settings > About Microsoft Edge.
- Scan for malware with Windows Security; restart the computer; keep third-party security software up to date.
- Clear history and cached images and files, from Settings and more > History > Open history page > Delete browsing data.
- Repair Edge: close Edge for all users, Start > Settings > Apps > Installed apps > Microsoft Edge > Modify > Repair (needs internet). Microsoft says browser data and settings should not be affected. If Modify is missing, an organisation manages Edge; ask the administrator.

## Verify
- [ ] The same pages load and stay open without a crash after a restart.

## Checked
Date: 2026-10-27. Documentation: Chrome Help ("Get help with common error messages in Chrome", "Fix connection and loading errors in Chrome", "Speed up Google Chrome") and Microsoft Support ("What to do if Microsoft Edge isn't working"), read in October 2026. Confirmed: the Aw Snap description, the step order, the Task Manager path, Edge update, history-clearing and Repair paths and the repair note. Removed as unconfirmed: STATUS_ACCESS_VIOLATION style code meanings, the hardware-acceleration step, command-line start flags, the disk-space figure, and the Firefox and Safari steps.
Method: documentation only; no commands were run.
