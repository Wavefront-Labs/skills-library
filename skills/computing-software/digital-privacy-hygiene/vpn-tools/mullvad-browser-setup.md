---
id: computing-software.digital-privacy-hygiene.vpn-tools.mullvad-browser-setup
name: mullvad-browser-setup
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, mullvad-browser-setup, privacy-browser, browser-fingerprinting]
level: practitioner
status: docs-checked
description: "Use Mullvad Browser for anti-fingerprinting browsing without Tor: what it is, pairing with a VPN, keeping defaults, permanent private mode."
sources:
  - "https://mullvad.net/en/browser"
  - "https://www.privacyguides.org/en/desktop-browsers/#mullvad-browser"
  - "https://blog.torproject.org/releasing-mullvad-browser/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mullvad Browser setup

**Goal:** Tor Browser-style fingerprint resistance on a normal connection (with or without a VPN), where the Tor
network is not wanted.

## What it is
- Developed by the Tor Project; Mullvad's page says it is Tor Browser without the Tor Network, usable with or
  without a VPN. It is free and open source whether or not you use Mullvad VPN.
- Strategy is to hide in the crowd: all users are meant to look the same, so the fingerprint is shared with many
  other Mullvad Browser users (Privacy Guides).
- It uses uBlock Origin to block third-party trackers and deliberately nothing more, since extra blocking attempts
  can reveal your identity (Mullvad). Privacy Guides says pre-installed extensions are configured by the security
  levels (Standard, Safer, Safest).
- Letterboxing limits tracking by browser window size (Mullvad).
- Tor Project's launch post: it does not anonymise through the Tor network; Tor Browser remains the option that
  does.

## Use it well
- Keep the defaults. Privacy Guides discourages adding extensions beyond those pre-installed; any change makes you
  less like the other users (the window-size and settings point is an inference from the shared-fingerprint design).
- It runs in permanent private browsing mode: history, cookies and site data are cleared every time the browser is
  closed; bookmarks, browser settings and extension settings are kept. Expect to log in again each session.
- For the strongest anti-fingerprinting protection Privacy Guides recommends using it with a VPN so you share an
  IP pool as well; Mullvad says a trustworthy VPN or none.
- Windows, macOS and Linux are listed by Privacy Guides; Linux installs include Flathub.

## Gotchas
- Logging into personal accounts in it links that session to you (inference).

## Checked
Method: docs-checked 2026-11-09 against mullvad.net/en/browser, the Privacy Guides desktop browsers page (Mullvad Browser section) and the Tor Project blog post releasing Mullvad Browser, all downloaded and searched. Dropped as unconfirmed: the `brew install --cask` command, NoScript bundled, first-party isolation, Standard as the default level, the "when to use what" table and the coveryourtracks.eff.org note.
