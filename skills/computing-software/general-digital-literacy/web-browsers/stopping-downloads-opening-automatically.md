---
id: computing-software.general-digital-literacy.web-browsers.stopping-downloads-opening-automatically
name: stopping-downloads-opening-automatically
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, downloads, auto-open-downloads, open-files-automatically, download-settings]
level: intro
status: docs-checked
description: "Stop Chrome and Safari opening certain downloaded file types automatically, reset 'Always open files of this type', and make Chrome download PDFs instead of opening them."
sources:
  - https://support.google.com/chrome/answer/95759
  - https://support.apple.com/guide/safari/general-ibrw1072/mac
  - https://support.apple.com/guide/safari/download-items-from-the-web-sfri40598/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stop files opening automatically

Auto-opening downloads is convenient but risky: a malicious file can run without a pause.

## Chrome
If a file type such as a PDF or image opens by itself: after a download, select **Recent download history**, right-click a recently downloaded file of that type, and if **Always open files of this type** is checked, uncheck it.

## PDFs specifically (Chrome)
More > Settings > Privacy and security > Site Settings > Additional content settings > **PDF documents**, then choose **Download PDFs** or **Open PDFs in Chrome**.

## Safari (Mac)
Safari > Settings > General: the **Open "safe" files after downloading** option opens the listed file types (never software) automatically when a download completes; clear it to stop this. Safari also decompresses .zip files after downloading them.
If a download contains software, Safari shows an alert when you open it; do not open software you were not expecting or from a source you do not trust.

## Edge and Firefox
Not covered here; the relevant settings could not be confirmed.

## Verify
- [ ] Downloading a file saves it without opening it; the downloads list shows it.

## Checked
2026-10-27. Chrome Help (Download a file) and Apple's Safari User Guide (General settings; Download items) were read. Confirmed the Chrome uncheck steps, the PDF setting path, the Safari option name and Safari's zip decompression and software alert. Edge and Firefox are not covered. Method: documentation only; no commands were run.
