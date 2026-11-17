---
id: computing-software.general-digital-literacy.basic-troubleshooting.connected-but-no-internet
name: connected-but-no-internet
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-connectivity, no-internet-access, dns, router-restart, ip-address]
level: intro
status: docs-checked
description: "Fix Windows Wi-Fi that shows connected but no internet: test another device, restart modem and router, spot a 169.254 address, run network commands, ping test, reset."
sources:
  - https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connected but no internet

Wi-Fi bars are full but pages will not load.

## 1. This device or the whole network?
Try another laptop or phone on the same Wi-Fi. If it connects and works, the cause is probably your device; if nothing works, suspect the router, modem or provider.

## 2. Whole network
- **Ping test (Windows):** open Command Prompt as administrator, run `ipconfig`, and find the **Default gateway** address for your Wi-Fi network. Run `ping <that address>`. Replies mean you reach the router, so the fault may be the modem or provider; check for an outage. No reply: try connecting the PC to the modem by Ethernet cable; if that works, the Wi-Fi router is the problem (install its latest firmware and see its documentation).
- **Restart modem and router:** unplug both power cables (remove a modem's backup battery if its lights stay on), wait at least 30 seconds, plug the modem in and wait for its lights to stop blinking, plug the router in and wait a few minutes.

## 3. Just this device (Windows)
- Make sure Wi-Fi is on and Airplane mode is off, and restart the PC.
- **Check the address:** `ipconfig`; an address that looks like `169.254.x.x` means Windows could not get an IP address from the router. Check that DHCP is enabled on the router (see its documentation).
- **Network commands** (Command Prompt as administrator), in this order: `netsh winsock reset`, `netsh int ip reset`, `ipconfig /release`, `ipconfig /renew`, `ipconfig /flushdns`. These reset the TCP/IP stack, renew the IP address and flush the DNS cache.
- Forget and rejoin the network, try the 2.4 GHz or 5 GHz network on a dual-band router, check Windows Update and restart.
- Uninstall the network adapter driver in Device Manager (Network adapters > Uninstall device > *Attempt to remove the driver for this device*) and restart; have a backup driver from the PC maker first, especially if the PC cannot get online.
- **Last resort:** Settings > Network & internet > Advanced network settings > **Network reset** (removes and reinstalls network adapters with default settings).

## Verify
- [ ] Pages load and `ping <default gateway>` replies.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix Wi-Fi connection issues in Windows" (Windows 11 steps). Confirmed: modem and router restart procedure, the five network commands and their purpose, the 169.254 address meaning and DHCP check, gateway ping test and Ethernet check, adapter driver uninstall, network reset path. Removed unconfirmed claims (neverssl captive portal, `ping 8.8.8.8` DNS test and DNS server suggestions, Mac DHCP lease, proxy and VPN steps, provider status page and light colours).
Method: documentation only; no commands were run.
