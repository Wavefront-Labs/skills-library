---
id: computing-software.general-digital-literacy.web-browsers.browser-managed-by-your-organisation-notice
name: browser-managed-by-your-organisation-notice
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [managed-browser, browser-policies, chrome-management, enterprise-policy]
level: practitioner
status: draft
description: "Understand and check the Your browser is managed by your organisation message in Chrome, Edge and Firefox, and what policies can see or change."
sources: ["https://support.google.com/chrome/", "https://support.mozilla.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser managed by your organisation

**Goal:** know whether policies are controlling your browser, and whether that is expected.

## Check
- Chrome: open `chrome://management` (or Menu: the entry "Managed by your organization"); `chrome://policy` lists each active policy and its source.
- Edge: `edge://management` and `edge://policy`.
- Firefox: `about:policies` (shows active policies or "not active").

## What it means
Policies are set by a company or school (device management, group policy, or a registry/plist entry). They can force an extension, set the home page and search engine, block settings, require sign-in, and, on managed profiles, let the admin report browsing metadata or installed extensions as the policy allows. Read `chrome://management` for what is reported.

## When it is unexpected
On a personal device, a "managed" notice with unfamiliar policies (forced search engine, forced extension, blocked settings) can indicate unwanted software. Steps: list policies, identify the source, check installed programs and extensions, scan with a reputable anti-malware tool, then remove the leftover policy entries (see the browser-hijacker removal skill). Do not delete policies on a work or school device; ask IT.

## If you are the admin
Policies come from Group Policy / Intune on Windows, configuration profiles on macOS, JSON files on Linux. Reload after changes (`chrome://policy` > Reload policies).

## Verify
After removal, `chrome://management` shows the browser is not managed and settings are editable again.
