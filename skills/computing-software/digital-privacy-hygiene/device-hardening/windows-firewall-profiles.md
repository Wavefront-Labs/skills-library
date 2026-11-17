---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-firewall-profiles
name: windows-firewall-profiles
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, windows-firewall, windows-security, public-wifi-and-travel-network-security]
level: practitioner
status: docs-checked
description: "Check the Domain, Private and Public Windows Firewall profiles, block all incoming connections on untrusted networks, and review allowed apps."
sources:
  - "https://support.microsoft.com/windows/turn-microsoft-defender-firewall-on-or-off-ec0844f7-aebd-0583-67fe-601ecf5d774f"
  - "https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows Firewall profiles

**Goal:** the PC accepts no unsolicited inbound connections on untrusted networks.

## Profiles
Windows Security shows which type of network you are connected to: **Domain network**, **Private network** or
**Public network**. Each has its own firewall setting; keep the firewall on for all three.
Use Public for any network you don't control; reserve Private for your own home network.

## Block everything on hostile networks
Windows Security > Firewall & network protection > choose the profile > under Incoming connections tick **Blocks all
incoming connections, including those in the list of allowed apps**. This ignores the allowed apps list; it increases
security but might stop some apps working.

## Review allowed apps
Firewall & network protection > **Allow an app through firewall**: if the firewall blocks an app you need you can add an
exception; read Microsoft's note on the risks of allowing apps through the firewall first. Remove entries you no longer need.

## Gotchas
- Third-party security suites may replace the firewall; confirm something is enforcing.
- Answer allow prompts for new apps deliberately.

## Checked
2026-10-28. Confirmed on Microsoft Support (Firewall and network protection in Windows Security) and Microsoft Learn
(Windows Firewall overview): the three profile names, the Blocks all incoming connections option and its effect, Allow an
app through firewall. Removed (not on the fetched pages): the PowerShell and netsh commands, the Wi-Fi network profile type
settings path, per-profile rule advice.
Method: documentation only; no commands were run.
