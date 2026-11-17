---
id: computing-software.it-support-helpdesk.remote-support-tools.wake-on-lan-for-out-of-hours-work
name: wake-on-lan-for-out-of-hours-work
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, wake-on-lan, magic-packet, power-management, out-of-hours, rmm, configmgr]
level: practitioner
status: draft
description: "Make Wake-on-LAN actually work: BIOS and NIC settings, Fast Startup, subnet-directed broadcasts or relays, sending the packet, and proving the wake source."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/setup-upgrade-and-drivers/wake-on-lan-feature"
  - "https://learn.microsoft.com/en-us/mem/configmgr/core/clients/deploy/configure-wake-on-lan"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# wake-on-lan-for-out-of-hours-work

## Device prerequisites
1. Firmware: enable Wake on LAN (often "Power On by PCI-E" or "Wake on LAN" with "Deep
   Sleep" disabled). Vendor tools (Dell Command | Configure, HP BCU, Lenovo WMI) can set it
   at scale.
2. NIC (Device Manager > adapter): Power Management tab, tick "Allow this device to wake
   the computer" and "Only allow a magic packet". Advanced tab: Wake on Magic Packet =
   Enabled.
3. Windows: turn off Fast Startup (`powercfg /h off` or the Control Panel setting) if you
   need wake from full shutdown; hybrid shutdown commonly leaves the NIC unpowered.
4. Wired Ethernet only in practice; Wi-Fi wake from shutdown is rarely supported and docks
   need their own "wake on dock" firmware setting.

## Getting the packet there
- The magic packet is a UDP broadcast (ports 7 or 9) and does not cross routers by
  default. Options: a relay on the same subnet (most RMMs and ConfigMgr wake-up proxy pick
  a peer that is awake), or subnet-directed broadcast enabled on the router for that VLAN.
- Send one from a machine on the subnet:
```powershell
$mac = 'AA-BB-CC-DD-EE-FF' -split '[-:]' | ForEach-Object { [byte]('0x' + $_) }
$pkt = [byte[]](,0xFF * 6) + ($mac * 16)
$udp = New-Object Net.Sockets.UdpClient; $udp.EnableBroadcast = $true
$udp.Send($pkt, $pkt.Length, [Net.IPAddress]::Broadcast, 9) | Out-Null
```

## Diagnose
- `powercfg /devicequery wake_armed` lists devices allowed to wake the machine.
- `powercfg /lastwake` after a test tells you what woke it.
- Wireshark display filter `wol` on the target subnet proves the packet arrived.

## Gotchas
- BIOS updates often reset WoL to off.
- Laptops on battery usually ignore wake; leave them on AC.
- Woken machines go back to sleep in minutes; set your job to run immediately or keep it
  awake with a power request.

## Verify
Device powers on from shutdown within a minute of the packet, checks in to RMM/Intune,
and `powercfg /lastwake` names the NIC.
