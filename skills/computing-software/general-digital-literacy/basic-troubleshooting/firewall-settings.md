---
id: computing-software.general-digital-literacy.basic-troubleshooting.firewall-settings
name: firewall-settings
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-malware, firewall, windows-firewall, macos-firewall]
level: intro
status: docs-checked
description: "Check the Windows firewall and the macOS firewall are on, allow one blocked app instead of switching the firewall off, and restore Windows firewall defaults."
sources:
  - https://support.microsoft.com/en-us/windows/security/windows-security/firewall-and-network-protection-in-the-windows-security-app
  - https://support.apple.com/guide/mac-help/block-connections-to-your-mac-with-a-firewall-mh34041/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall settings

A firewall filters network traffic and blocks unauthorised access. Keep it on; turning it off could make your device more vulnerable.

## Windows firewall (Windows Security)
- Windows Security > **Firewall & network protection**. Windows shows which network type you are on; select **Domain**, **Private** or **Public** network. Under *Microsoft Defender Firewall* the setting should be **On**.
- **Private vs public:** the difference is whether other devices on the network may see, and maybe connect to, your device. A home network is typically private; a coffee-shop Wi-Fi is public and should have stricter controls.
- **Allow an app through firewall:** if the firewall blocks an app you need, add an exception for that app instead of turning the firewall off.
- **Incoming connections:** the checkbox *Blocks all incoming connections, including those in the list of allowed apps* ignores the allowed-apps list and blocks everything; it raises security but may stop some apps working.
- **Advanced settings** opens the classic firewall console for inbound and outbound rules; changing or deleting rules incorrectly can leave the system more vulnerable or break apps.
- **Restore firewalls to default** resets settings to how they were when you got the computer; any policies from your organisation are reapplied.
- If your device is managed by an organisation, policy may stop you changing the firewall; ask your administrator.

## macOS
- System Settings > **Network** > **Firewall**, turn **Firewall** on, and click **Options** for more settings (the Options button is disabled until the firewall is on).
- To control an app: in Options, add it to the list of applications and services with the plus button, then choose allow or block with its arrows. Blocking an app can affect it or software that depends on it.
- Some apps not in the list may still have access (system apps, services, and digitally signed apps opened by other apps); add them to the list to block them.
- When something tries to connect to an app not in the list, an alert asks whether to allow or deny the connection; until you answer, connection attempts are denied.

## Verify
- [ ] Windows Security shows the firewall on for the network you use, or macOS Firewall is on.

## Checked
Checked 2026-10-27 against Microsoft Support "Firewall and network protection in the Windows Security app" and the Apple Mac User Guide "Block connections to your Mac with a firewall". Confirmed: menu paths, network types, allow-an-app exception, block-all-incoming option, Advanced settings warning, Restore firewalls to default, macOS options and alert behaviour. Removed unconfirmed claims (Public as the default profile, how to switch a network between Public and Private, "tick Private only" prompt advice, macOS firewall off by default, stealth mode and automatic-allow options, exact prompt text).
Method: documentation only; no commands were run.
