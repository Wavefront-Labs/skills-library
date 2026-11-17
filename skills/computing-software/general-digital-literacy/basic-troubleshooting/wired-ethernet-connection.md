---
id: computing-software.general-digital-literacy.basic-troubleshooting.wired-ethernet-connection
name: wired-ethernet-connection
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-connectivity, ethernet, network-cable, usb-c-ethernet-adapter]
level: intro
status: draft
description: "Connect a computer by Ethernet cable for faster, stabler internet: adapters for thin laptops, cable categories, link lights, and fixing a cable that shows unplugged."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/connect-to-the-internet-using-ethernet-mchlp1157/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Wired Ethernet connection

## Why wire
Video calls, gaming, big uploads and work-from-home are steadier on a cable: no interference, lower latency, usually faster than Wi-Fi through walls.

## Hardware
- Laptops without a port: a **USB-C (or USB-A) to Ethernet adapter** (gigabit; 2.5G for fast fibre). Docks often include one.
- Cable: **Cat5e** or **Cat6** for gigabit; Cat5 (no "e") may cap at 100 Mb/s. Flat cables are fine for indoor runs; keep under 100 m.
- No router nearby: **powerline adapters** (through mains wiring) or mesh Wi-Fi nodes with Ethernet ports.

## Connect
- Plug into a **LAN** port on the router (not the WAN/internet port). It works automatically (DHCP).
- With both Wi-Fi and cable connected, Windows and macOS prefer the cable. Mac: System Settings › Network › ⋯ › *Set Service Order* if not.

## Troubleshoot "Network cable unplugged"
- Port lights on router and laptop: none = bad cable/port; try another cable and another router port.
- Settings › Network & internet › Ethernet: check *Connected*. Adapter not listed → Device Manager › Network adapters (install the adapter's driver, update Windows).
- Speed check: Windows Settings › Ethernet › *Link speed* (should say 1000/1000 Mbps); 100 Mbps = old cable or damaged pin.
- Office wall ports may be unpatched or need registration with IT.

## Verify
- [ ] Ethernet shows Connected at 1 Gbps; speed test is faster and steadier than Wi-Fi.
