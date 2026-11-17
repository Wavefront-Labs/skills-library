---
id: computing-software.general-digital-literacy.basic-troubleshooting.smartscreen-and-gatekeeper-warnings
name: smartscreen-and-gatekeeper-warnings
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [smartscreen, gatekeeper, app-warning, unidentified-developer, download-safety]
level: practitioner
status: draft
description: "Decide what to do about Windows SmartScreen and macOS Gatekeeper warnings when opening a downloaded app: verify the source, then allow it safely or delete it."
sources: ["https://support.microsoft.com/", "https://support.apple.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SmartScreen and Gatekeeper warnings

**Goal:** treat the warning as a prompt to verify, not an obstacle to click through.

## What they are
- **Windows SmartScreen** ("Windows protected your PC"): warns for files with no reputation or a bad one, or unsigned publishers.
- **macOS Gatekeeper** ("cannot be opened because it is from an unidentified developer" / "Apple could not verify it is free of malware"): checks signing and notarisation of apps downloaded from outside the App Store.

## Decide
1. Where did it come from? Only the vendor's official site or a store you trust. Search the exact name plus the word "official".
2. Is the publisher shown and what you expect? On Windows use More info to see the publisher name.
3. Check the download hash against the vendor's published value where provided (`Get-FileHash file.exe` on Windows; `shasum -a 256 file` on macOS).
4. Scan with your security software or upload the file to a multi-engine scanner.
5. If any doubt remains, delete it.

## If you trust it
- Windows: More info > **Run anyway**.
- macOS (current versions): try opening once, then System Settings > Privacy & Security > scroll to the blocked app > **Open Anyway** and confirm. Older versions allowed Control-click > Open.
- IT-managed devices: ask IT instead; policies may block overrides.

## Never
Do not disable SmartScreen or Gatekeeper permanently, and do not follow instructions in an email or web page to bypass them for a "required" update.

## Verify
App opens; Windows Security or Activity Monitor shows no unexpected behaviour; the file's signature (properties > Digital Signatures) names the real publisher.
