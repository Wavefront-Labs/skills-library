---
id: computing-software.general-digital-literacy.basic-troubleshooting.forget-and-rejoin-wifi
name: forget-and-rejoin-wifi
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, wifi, connectivity, forget-network, wifi-password-changed, cant-connect-wifi, network-reset, airplane-mode, 2-4ghz-vs-5ghz]
level: intro
status: docs-checked
description: "Fix Windows 11 Wi-Fi that will not connect after a password change or router swap: airplane mode, forget and rejoin, restart the router, try the other band, then network reset."
sources:
  - https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
  - https://support.apple.com/guide/mac-help/share-your-wi-fi-password-with-another-device-mchlp1179/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forget and rejoin a Wi-Fi network

**Goal:** reconnect when a Windows device refuses a network it used to join.

## When to use
Router replaced or password changed, "can't connect" messages, or one device failing on a network others can use.

## Steps (Microsoft's order for Windows 11)
1. **Check Wi-Fi is on:** select the Network, Sound or Battery icons on the taskbar, make sure Wi-Fi is on, and choose a network you recognise.
2. **Airplane mode off:** Settings > Network & internet > **Airplane mode**; make sure it is off.
3. **Forget and reconnect:** Settings > Network & internet > **Wi-Fi** > **Manage known networks** > select the network > **Forget**. Reconnect by selecting it and entering the password.
4. **Restart modem and router:** unplug the router's power cable and the modem's (if a modem has a backup battery and lights stay on, remove the battery), wait at least 30 seconds, put the battery back, plug the modem in and wait for its lights to stop blinking, then plug in the router and wait a few minutes. Everyone on the network is disconnected meanwhile. A combined modem/router needs only one device restarted.
5. **Try the other band:** many routers broadcast 2.4 GHz and 5 GHz as separate networks; if both are listed, try the other one.
6. **Test another device** on the same network; if it connects, the problem is on your device.
7. **Check for updates and restart the PC** (Settings > Windows Update > Check for updates).
8. **Last resort, network reset:** Settings > Network & internet > **Advanced network settings** > **Network reset** > **Reset now** > Yes. It removes your network adapters and their settings; after the restart they are reinstalled with defaults. Afterwards you might need to reinstall VPN client software or Hyper-V virtual switches, and each known network may be set to the Public profile.

## Other devices
Mac, iPhone and Android menus are not covered by this page; use the maker's support pages for those. On a Mac that is connected to the network, you can share the password with a nearby Mac, iPhone or iPad whose owner is signed in to their Apple Account and is in your Contacts: choose the network on the other device, then click **Share** in the Wi-Fi Password notification on your Mac.

## Verify
- [ ] The device connects and a web page loads.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix Wi-Fi connection issues in Windows" (Windows 11 steps; the Windows 10 network reset path is Status > Network reset) and the Apple Mac User Guide "Share a Wi-Fi password on Mac". Confirmed: steps 1 to 8 with the menu paths, the router restart procedure, the network reset behaviour and side effects, and the Mac password-sharing conditions. Removed unconfirmed claims (Wi-Fi flyout right-click Forget, Mac, iPhone and Android forget and reset menus, "reinstalls adapters, forgets all networks" wording, WPA3-only advice, airplane mode toggling as a fix).
Method: documentation only; no commands were run.
