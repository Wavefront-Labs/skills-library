---
id: computing-software.general-digital-literacy.web-browsers.reviewing-extension-permissions
name: reviewing-extension-permissions
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-extensions, extension-permissions, site-access, extension-audit]
level: intro
status: docs-checked
description: "Review what each Chrome extension can read and change, limit site access to the current site, specific sites or on selection, and check Safety Check for harmful extensions."
sources:
  - https://support.google.com/chrome/answer/2664769
  - https://support.google.com/chrome/answer/10468685
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Review extension permissions and site access

**Goal:** each extension sees only the sites it needs.

## Chrome
- **Quick switch:** Extensions button > More next to the extension > "This can read and change site data" > choose:
  - **When you select the extension:** it can access the current site only when you select it, for that tab or window.
  - **On [current site]:** it automatically reads and changes data on that site.
  - **On all sites:** it automatically reads and changes data on all sites.
- **Detail page:** More > Extensions > Manage extensions > Details. Under "Allow this extension to read and change all your data on websites you visit" pick when you select / On specific sites / On all sites. Under Permissions, next to "Allowed sites" use Add; to remove a site use More > Remove. If Add is missing, switch to On specific sites.
- Chrome notes these choices affect only sites matching the extension's host permissions; extensions that change lower-level network access (VPNs, proxy settings) are not affected.
- **Safety Check** (Settings > Privacy and security > Go to Safety Check) warns of potentially harmful extensions.
- **Unsupported extensions:** Chrome and the Web Store require extensions to meet current requirements, so Chrome may disable ones that do not. You can find an alternative (Details > More > Find Alternatives), remove it, or temporarily re-enable it for a limited period only.

## Routine
Every few months remove extensions you do not use and narrow the site access of rarely used ones.

## Verify
- [ ] Every extension has the narrowest site access that still works.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Install and manage extensions" and "Manage Chrome safety and security", read in October 2026. Confirmed: the quick-switch options, Details paths, host-permission note, Safety Check extension warning and unsupported-extension handling. Removed as unconfirmed: the permission meaning table, Edge detail paths, Firefox and Safari steps, and the claim that Chrome disables updated extensions until you approve new permissions.
Method: documentation only; no commands were run.
