---
id: computing-software.networking-hardware-and-wireless.tailscale.vpn-on-demand-ios-macos
name: vpn-on-demand-ios-macos
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [vpn-on-demand, connection-rules, ios]
level: intro
status: docs-checked
description: "Auto-connect Tailscale on iOS and macOS according to interface rules."
sources: ["https://tailscale.com/kb/1291"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VPN On Demand

Goal: connect and disconnect Tailscale automatically on Apple devices.

VPN On Demand is an iOS and macOS feature that lets VPN providers automate connections. The Tailscale client also configures a broad On Demand policy while Tailscale is enabled, so the VPN stays active across restarts, auto-updates and crashes.

**Set up on iOS**

1. Log in, then tap your profile picture at top right to open settings.
2. Tap VPN On Demand. If hidden, an administrator may have hidden it, or the client is old.
3. Enable it and define rules.

**Connection rules** exist for Wi-Fi, Cellular and Ethernet interfaces. For Wi-Fi the options are:

- Always: connect whenever a Wi-Fi connection is active.
- Only On: connect when active, only if the current network is in the configured list.
- Except On: connect when active, but disconnect on the listed networks.
- Never: always disconnect when a Wi-Fi connection is active.
- Do Nothing: no automatic connect or disconnect.

Example from the docs: connect Tailscale when the phone leaves your home Wi-Fi and disconnect once you are back under it.

**Checklist**

1. Pick a rule per interface.
2. List trusted Wi-Fi networks.
3. Confirm the setting is not hidden by policy.

## Checked

2026-11-09. Confirmed against the Tailscale VPN On Demand page: availability, the automatic broad policy, iOS setup steps, interface rules and the Wi-Fi example. Added the two Wi-Fi options the page lists that the skill had omitted.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1291 (Using VPN On Demand for iOS and macOS), read in full.
