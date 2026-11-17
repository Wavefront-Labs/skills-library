---
id: computing-software.it-support-helpdesk.desktop-support.macos-wireless-and-network-diagnostics
name: macos-wireless-and-network-diagnostics
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, wireless-diagnostics, macos, wifi, networkquality, wdutil, scutil]
level: practitioner
status: draft
description: "Diagnose Wi-Fi and network problems on a Mac: Option-click details, Wireless Diagnostics report, wdutil, networkQuality, DNS via scutil, and resetting network settings."
sources:
  - "https://support.apple.com/en-us/102559"
  - "https://support.apple.com/guide/mac-help/use-wireless-diagnostics-mchlf4d3c0fe/mac"
  - "https://support.apple.com/en-us/101942"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-wireless-and-network-diagnostics

## Quick read
Hold `Option` and click the Wi-Fi icon: shows IP, router, RSSI (signal, closer to 0 is
better; below about -70 dBm is weak), noise, channel and band, PHY mode, Tx rate.

## Commands
```bash
networksetup -listallhardwareports     # which enX is Wi-Fi
ipconfig getifaddr en0                  # current IP on en0
sudo wdutil info                        # Wi-Fi details (airport CLI is gone in recent macOS)
networkQuality -v                       # throughput, responsiveness under load
scutil --dns | head -40                 # DNS resolvers in order, incl. VPN-scoped
route -n get default                    # which interface carries default traffic
ping -c 20 <router-ip>                  # local link quality
```

## Wireless Diagnostics
Option-click Wi-Fi > Open Wireless Diagnostics. Run it while the problem happens; it
writes a report bundle (in `/var/tmp`) to attach to the ticket. Window > Scan shows nearby
networks and channel congestion; Window > Performance graphs signal and noise live.

## Common fixes
- Forget the network (System Settings > Wi-Fi > ... > Forget) and rejoin; stale
  802.1X credentials are a common cause on corporate SSIDs.
- Private Wi-Fi Address (per-network) breaks MAC-based captive portals or reservations;
  turn it off for that network if policy needs fixed MACs.
- Remove duplicate service order entries: Network settings > ... > Set Service Order, put
  Wi-Fi or Ethernet first as needed.
- Last resort reset: remove the Wi-Fi service and re-add it, or delete
  `/Library/Preferences/SystemConfiguration/preferences.plist` and network plists after a
  backup, then restart.

## Gotchas
- VPN/ZTNA clients install their own DNS resolvers; check `scutil --dns` before blaming
  Wi-Fi.
- MDM Wi-Fi profiles reinstall settings you delete; change them in the MDM.

## Verify
Signal and noise look healthy, ping to router has no loss, `networkQuality` reports
expected throughput, and internal names resolve.
