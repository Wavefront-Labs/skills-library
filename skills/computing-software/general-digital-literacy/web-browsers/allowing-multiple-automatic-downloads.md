---
id: computing-software.general-digital-literacy.web-browsers.allowing-multiple-automatic-downloads
name: allowing-multiple-automatic-downloads
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-downloads, multiple-downloads, automatic-downloads, site-permissions]
level: intro
status: gated
description: "Fix a site that only downloads the first of several files by changing Chrome's Automatic downloads permission, and where to look in Edge, without allowing it everywhere."
sources:
  - https://support.google.com/chrome/answer/95759
  - https://support.microsoft.com/en-us/microsoft-edge/view-and-delete-browser-history-in-microsoft-edge-00cf7943-a9e1-975a-a33d-ac10ce454ca4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allow multiple automatic downloads

## Symptom
A site's *Download all* or a sequence of downloads saves only the first file because the browser asks or blocks further automatic downloads.

## Chrome
Chrome's help describes the global default: More > Settings > Privacy and security > **Site Settings** > **Additional permissions** > **Automatic downloads**, then choose the option you want (the page explains you can let sites download related files together). Prefer a per-site exception over changing the default for every site.
- The per-site prompt in the address bar and the per-site entry in the site's settings panel (gated: unconfirmed, source is paywalled or blocked). Chrome's help page for downloads does not describe them.

## Edge
Edge keeps per-site permissions (location, cookies, pop-ups, media autoplay) under Settings and more > Settings > Privacy, search, and services > **Site permissions**. The exact name of its automatic-downloads entry (gated: unconfirmed, source is paywalled or blocked).

## Safari and Firefox
Per-site download permissions in Safari and Firefox (gated: unconfirmed, source is paywalled or blocked).

## Safer alternatives
- Ask the site for a single .zip of the files, or use the cloud drive's own download of a multi-selection, so one download covers all files.

## Security notes
- Keep the global default restrictive; allow a site only for a one-off job and reset it afterwards in Site settings.

## Verify
- [ ] All expected files appear in the Downloads list and the exception covers only that site.

## Checked
2026-10-27. Chrome Help (Download a file) and Microsoft's Edge history page (which lists the Site permissions location) were read. Confirmed the Chrome global Automatic downloads path and the Edge Site permissions location. The remaining items are marked gated. Method: documentation only; no commands were run.
