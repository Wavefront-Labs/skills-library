---
id: computing-software.digital-privacy-hygiene.phishing-awareness.avoiding-malvertising-and-fake-download-ads
name: avoiding-malvertising-and-fake-download-ads
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, malvertising, search-ads, fake-installers, ublock-origin, authenticode, malicious-downloads]
level: practitioner
status: draft
description: "Avoid malicious search ads impersonating software downloads, banks and wallets: skip sponsored results, use official sources or package managers, and check installer signatures."
sources:
  - "https://www.ic3.gov/PSA/2022/PSA221221"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-authenticodesignature"
  - "https://github.com/gorhill/uBlock"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoiding malvertising and fake download ads

**Goal:** criminals buy search ads for "download 7-Zip", "OBS", "AnyDesk", "KeePass", your bank or a crypto wallet.
The ad shows the real domain but leads to a look-alike that serves infostealers.

## Habits
- **Skip sponsored results** for downloads and logins; scroll to the organic result, or better, use a bookmark.
- Get software from: the vendor's site you already know, the official project's GitHub releases, or a package manager:
  ```powershell
  winget install 7zip.7zip
  ```
  ```bash
  brew install --cask obs
  ```
- Check the domain carefully: `obsproject.com` vs `obs-project.net`, `7-zip.org` vs `7-zip.com`.
- Banking and wallets: type the address or use the app; never search for the login page.

## Block ads
- **uBlock Origin** (Firefox; uBlock Origin Lite on Chrome) or Brave's Shields remove search ads and malvertising
  networks. Encrypted DNS with blocklists (NextDNS, AdGuard DNS) adds another layer.

## Check the installer
```powershell
Get-AuthenticodeSignature .\obs-installer.exe | Format-List Status, SignerCertificate
```
`Status` should be `Valid` and the signer the expected company. On macOS: `codesign -dv --verbose=4 /Applications/App.app`
and `spctl -a -vv /Applications/App.app`. Unsigned installers for well-known apps, or ones wrapped in password-protected ZIPs or ISOs, are malicious.

## If you ran one
Assume an infostealer: disconnect, clean or reinstall the PC, and change passwords and revoke sessions from another
device (browser cookies were likely stolen).

## Report
Google: "About this ad" (⋮ next to the ad) > Report; Bing: ad feedback.

## Verify
- [ ] Ad blocker on every browser; software installed via package managers or known official sites only.
