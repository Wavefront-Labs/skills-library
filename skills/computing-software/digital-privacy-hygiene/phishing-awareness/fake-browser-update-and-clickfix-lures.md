---
id: computing-software.digital-privacy-hygiene.phishing-awareness.fake-browser-update-and-clickfix-lures
name: fake-browser-update-and-clickfix-lures
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, fake-browser-update, clickfix, fake-captcha, malicious-downloads, malicious-attachments, run-dialog, powershell-paste, infostealer, socgholish]
level: intro
status: draft
description: "Recognise fake 'update your browser' pages and ClickFix fake CAPTCHAs that tell you to press Win+R and paste a command; the rule: never paste commands from a website."
sources:
  - "https://www.proofpoint.com/us/blog/threat-insight/security-brief-clickfix-social-engineering-technique-floods-threat-landscape"
  - "https://www.microsoft.com/en-us/security/blog/2025/08/21/think-before-you-clickfix-analyzing-the-clickfix-social-engineering-technique/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fake browser updates and ClickFix lures

**Goal:** two of the most effective malware delivery tricks rely on you doing the
installation yourself. Learn their look.

## Fake browser updates
A compromised website overlays "Your Chrome is out of date - Update" and downloads a file
(`Update.js`, `ChromeSetup.zip`, `.msix`, `.exe`). Real browsers update **themselves** from
their own menu (Chrome: Settings > About Chrome; Firefox: Help > About Firefox; Edge:
Settings > About). No website ever needs to update your browser.

## ClickFix / fake CAPTCHA
A page shows "Verify you are human" or "Fix this error" and instructs:
1. Press **Win + R** (or open Terminal on macOS),
2. Press **Ctrl + V** (the page silently copied a command to your clipboard),
3. Press **Enter**.
The pasted command is PowerShell/mshta/curl that installs an infostealer or remote access
tool. Variants target macOS ("paste this in Terminal to install") and fake Teams/Zoom
"fix your microphone" pages.

## Rules
- **Never paste a command from a website, email or chat into Run, PowerShell or Terminal**
  unless you wrote or fully understand it.
- Real CAPTCHAs only involve clicking or picking images in the page.
- Download software only from the vendor's site or official store.

## If you already ran it
Disconnect from the internet and treat it as an infostealer infection (see
`computing-software.digital-privacy-hygiene.password-hygiene.responding-to-infostealer-credential-theft`).

## Verify
- [ ] Household knows the "never paste commands" rule.
