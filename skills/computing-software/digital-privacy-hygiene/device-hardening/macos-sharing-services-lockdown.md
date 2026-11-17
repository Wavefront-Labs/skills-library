---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-sharing-services-lockdown
name: macos-sharing-services-lockdown
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-sharing-services, macos, remote-login, screen-sharing, airdrop, file-sharing, local-hostname]
level: intro
status: draft
description: "Turn off unused macOS Sharing services (File/Screen Sharing, Remote Login, Remote Management, AirPlay Receiver), set AirDrop sensibly and change a revealing hostname."
sources:
  - "https://support.apple.com/guide/mac-help/welcome/mac"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://www.cisecurity.org/benchmark/apple_os"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS sharing services lockdown

**Goal:** a Mac on hotel or café Wi-Fi exposes no listening services and does not announce its owner's name.

## Sharing settings
System Settings > General > **Sharing**. Turn off everything you do not actively use:
- File Sharing, Media Sharing, Screen Sharing, Remote Management, **Remote Login** (SSH), Remote Application
  Scripting, Printer Sharing, Internet Sharing, Bluetooth Sharing, Content Caching.
- If you need one (e.g. SSH for yourself), restrict **Allow access for: Only these users**.
- **Local hostname** (Edit at the bottom): "Janes-MacBook-Pro.local" broadcasts your name on every network;
  rename to something generic.

## AirPlay and AirDrop
- System Settings > General > AirDrop & Handoff: **AirPlay Receiver** off unless you cast to this Mac (it listens on ports 5000/7000).
- AirDrop: Contacts Only or Receiving Off; "Everyone for 10 Minutes" only when needed. Unsolicited AirDrop
  images are a harassment vector.

## Firewall
System Settings > Network > Firewall on; Options > **Enable stealth mode**; avoid "Automatically allow downloaded
signed software to receive incoming connections" if you want prompts.

## Check what is listening
```bash
sudo lsof -iTCP -sTCP:LISTEN -n -P
sudo systemsetup -getremotelogin
```

## Gotchas
- Some apps (Plex, development servers) add their own listeners outside Sharing; the lsof check catches them.
- Screen Sharing turned on by a "support" caller is a scam indicator; turn it off and review users.

## Verify
- [ ] Sharing pane shows all services off (or deliberately limited); generic hostname.
- [ ] `lsof` shows no unexpected listeners; firewall on with stealth mode.
