---
id: computing-software.digital-privacy-hygiene.vpn-tools.verifying-tor-browser-downloads
name: verifying-tor-browser-downloads
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, tor-browser-verification, tor-browser, tor]
level: practitioner
status: docs-checked
description: "Download Tor Browser from the official site, verify its OpenPGP signature against the Tor Browser developers key, and handle errors."
sources:
  - "https://support.torproject.org/tor-browser/getting-started/verifying-tor-browser/"
  - "https://www.torproject.org/download/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Verifying Tor Browser downloads

**Goal:** the Tor Browser you install is the real one, especially when you got it from a mirror or a friend.

## Get it
- The Tor Project download page (torproject.org/download) lists Tor Browser for desktop and Android.
- Each file on the download page has a "signature" link: a `.asc` OpenPGP file with the same name as the package.

## Verify the signature
Install GnuPG first: Windows, Gpg4win; macOS, GPGTools; Linux usually has it preinstalled. Download the `.asc` file
next to the installer, then (file names here are examples; use yours):
```
gpg --auto-key-locate nodefault,wkd --locate-keys torbrowser@torproject.org
gpg --output ./tor.keyring --export 0xEF6E286DDA85EA2A4BA7DE684E2C6E8793298290
gpgv --keyring ./tor.keyring ~/Downloads/tor-browser-linux-x86_64-13.0.1.tar.xz.asc ~/Downloads/tor-browser-linux-x86_64-13.0.1.tar.xz
```
Expect `Good signature from "Tor Browser Developers (signing key) <torbrowser@torproject.org>"`. The key fingerprint
is `EF6E286DDA85EA2A4BA7DE684E2C6E8793298290`.

- If importing the key errors, stop and work out why; the Tor page offers a workaround importing the key from
  `openpgpkey.torproject.org` or `keys.openpgp.org`.
- `gpg --refresh-keys EF6E286DDA85EA2A4BA7DE684E2C6E8793298290` refreshes the key and fetches new subkeys.
- "No such file or directory" means a wrong file name or an earlier step failed.
- The signature date is when the package was signed; a date that varies between releases is normal.

## Gotchas
- A "Good signature" from a different key or fingerprint is not good.

## Checked
2026-11-01. Confirmed against the Tor Project support page "How to verify Tor Browser's signature" and the download
page: `.asc` signature files, Gpg4win/GPGTools/preinstalled GnuPG, the three commands, fingerprint, expected output,
refresh command, workaround sources, signature dating. Removed: GetTor, mirrors, Android store and iOS claims, the
`brew install` line, self-update claim, search-ad warning (not on the pages read).
Method: documentation only; no commands were run.
