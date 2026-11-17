---
id: computing-software.general-digital-literacy.web-browsers.clearing-browsing-data
name: clearing-browsing-data
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-privacy, clear-browsing-data, clear-cache, clear-cookies, site-data, delete-history, time-range, clear-on-exit, clear-site-data]
level: intro
status: docs-checked
description: "Clear history, cookies and cached files in Chrome, Edge and Safari, for one site or a time range, and choose what to keep, such as saved passwords."
sources:
  - https://support.google.com/chrome/answer/2392709
  - https://support.google.com/chrome/answer/95647
  - https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09
  - https://support.microsoft.com/en-us/microsoft-edge/view-and-delete-browser-history-in-microsoft-edge-00cf7943-a9e1-975a-a33d-ac10ce454ca4
  - https://support.apple.com/guide/safari/manage-cookies-sfri11471/mac
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Clearing browsing data selectively

**Goal:** fix a broken site or remove traces, without logging yourself out of everything.

## Everything in a time range
Chrome: More > **Delete browsing data**; Edge: Settings > Privacy, search, and services > Clear browsing data > **Choose what to clear**. In both, `Ctrl+Shift+Delete` (Mac Cmd+Shift+Delete in Chrome) opens it. Pick a time range (such as Last hour or All time) first.

| Item | Clearing it... |
|---|---|
| Browsing history | removes the list of visited pages (and, in Chrome, their address-bar predictions and New Tab shortcuts) |
| Cookies and other site data | **signs you out** of most sites |
| Cached images and files | removes saved parts of pages; sites reload them on the next visit |
| Download history | removes the list only; downloaded files stay on the computer |
| Autofill form data | removes saved form entries |
| Site settings / permissions | removes permissions you gave sites |

Chrome's help says passwords and passkeys are not deleted by this dialog; they are managed in the Google Password Manager. Edge lists Passwords as an item you can tick, so leave it unticked unless you mean it.

## Just one site (better for fixing a broken site)
- Chrome: Settings > Privacy and security > Third-party cookies > **See all site data and permissions**, search the site name, then Delete.
- Edge: Settings > Privacy, search, and services > Cookies > **See all cookies and site data**; you can delete the cookies of a single site there.
- Safari: Safari > Settings > Privacy > **Manage Website Data**, select one or more sites, then Remove (or Remove All). Apple notes this may sign you out and may change or remove data in other apps.

## Clear automatically
- Chrome: Settings > Privacy and security > Site settings > Additional content settings > On-device site data > **Delete data sites have saved on your device when you close all windows**.
- Edge: Clear browsing data > **Choose what to clear every time you close the browser**, then turn on Cookies and other site data (this signs you out of most sites each time).

## Gotchas
- Clearing history while signed in and synced removes it on your other devices and from your Google Account (Chrome); Edge clears synced items across devices if sync is on.
- It removes local data only; it does not hide activity from your network or the sites.
- Safari's History > Clear History removes history, recent searches and the downloads list (not the files); cookies are cleared separately under Manage Website Data.

## Verify
- [ ] The problem site loads properly after clearing its data; other sites keep you signed in.

## Checked
2026-10-27. Chrome Help (Delete browsing data in Chrome; Delete, allow, and manage cookies), Microsoft's Edge cookies and history pages and Apple's Safari User Guide (cache and cookies; clear history) were read. Confirmed the menu paths, items and their effects above. Firefox is not covered because its support site could not be read. Method: documentation only; no commands were run.
