---
id: computing-software.general-digital-literacy.web-browsers.failed-and-interrupted-downloads
name: failed-and-interrupted-downloads
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, downloads, failed-download, interrupted-download, resume-download, network-error]
level: intro
status: docs-checked
description: "Fix failed, stuck or interrupted downloads in Chrome: read the error message, resume, free space, fix permissions, and recognise security blocks."
sources:
  - https://support.google.com/chrome/answer/2898334
  - https://support.google.com/chrome/answer/6261569
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failed and interrupted downloads

**Goal:** the file finishes downloading, or you know exactly why it cannot.

## First steps (Chrome)
- Make sure the internet connection is stable; Chrome automatically resumes interrupted downloads.
- To resume by hand: select Download in progress, point to the paused file name, select **Resume**.
- Try again later, or contact the website owner.

## Read the error message
| Message | Chrome's explanation and fix |
|---|---|
| "Network failed" (installing from the Chrome Web Store: `NETWORK_FAILED`) | Unwanted software could be blocking it: remove it, retry; reinstall Chrome if it still fails |
| "Download blocked" | Your computer's security settings blocked the file. On Windows the Attachment Manager may have removed it: check Windows internet security settings |
| "No file" / "File missing" | The file does not exist on the site or moved: contact the site owner or find it elsewhere |
| "Virus scan failed" / "Virus detected" | Your virus scanner may have blocked it: check the scanner's details |
| "Disk full" | Not enough space: delete files, empty the Trash |
| "Insufficient permissions" / "System busy" | Chrome could not save the file: cancel and retry; right-click the link and choose **Save link as**; save somewhere you can access, such as Desktop or Documents |
| "Needs authorization" | You lack permission: contact the site or server owner |
| "Forbidden" / "Failed - Forbidden" | You may need to sign in on the site that hosts the file |

## Security blocks
Chrome blocks files it finds dangerous (malware, or uncommon or unfamiliar files) or marks "Unverified" if downloaded while Safe Browsing is off. Take warnings seriously; attackers may ask you to turn off or ignore them. Chrome removes a warning from history after one hour if you take no action.

## Verify
- [ ] The file finishes and opens without error.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Fix file download errors" and "Google Chrome blocks some downloads", read in October 2026. Confirmed: every row in the table, Resume path, automatic resume, block reasons. Removed as unconfirmed: Edge, Firefox and Safari wording, the Ctrl+J shortcut, partial-file extensions, large-file tips, curl and checksum commands.
Method: documentation only; no commands were run.
