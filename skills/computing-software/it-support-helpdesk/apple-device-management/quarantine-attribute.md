---
id: computing-software.it-support-helpdesk.apple-device-management.quarantine-attribute
name: quarantine-attribute
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, gatekeeper, quarantine-attribute, quarantine, xattr]
level: practitioner
status: draft
description: "Inspect and handle the com.apple.quarantine extended attribute on downloaded files and deployed packages."
sources:
  - "https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web"
  - "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# quarantine-attribute

Goal: handle first-launch prompts.
- View: `xattr -l file`; delete flag: `xattr -d com.apple.quarantine file`.
- Files installed by MDM or the installer command generally lack quarantine.
- Browsers and AirDrop add it; Gatekeeper evaluates at first launch.
- For scripts, `xattr -dr com.apple.quarantine /path` is a last resort.
- Log decisions for audit.
Practice: Prefer fixing the source by distributing through MDM, and record any manual attribute removal in the ticket so auditors can trace why a file bypassed the prompt. Check `xattr -l` output before and after deployment when testing a new package.
Gotcha: stripping quarantine on untrusted downloads bypasses user warnings; restrict to files you trust.
Verify:
- `xattr -l` lists no quarantine on a deployed app.
- App launches silently.
