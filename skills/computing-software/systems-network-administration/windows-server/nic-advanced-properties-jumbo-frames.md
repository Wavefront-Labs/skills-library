---
id: computing-software.systems-network-administration.windows-server.nic-advanced-properties-jumbo-frames
name: nic-advanced-properties-jumbo-frames
category: computing-software
field: systems-network-administration
product: windows-server
tags: [netadapter, jumbo-frames, netadapteradvancedproperty, server-networking, mtu]
level: practitioner
status: docs-checked
description: "Set NIC advanced properties safely: jumbo frames end to end, speed/duplex, interrupt moderation, and verify MTU with ping -f -l before production."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapteradvancedproperty
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/keywords-that-can-be-edited
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/enumeration-keywords
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIC advanced properties and jumbo frames

## See what the driver offers
```powershell
Get-NetAdapterAdvancedProperty -Name 'SLOT 3 Port 1' | Format-Table DisplayName,DisplayValue,RegistryKeyword,ValidDisplayValues -Wrap
```
Use the **RegistryKeyword** (`*JumboPacket`, `*SpeedDuplex`, `*InterruptModeration`) in scripts; DisplayNames
differ per vendor.

## Jumbo frames
```powershell
Set-NetAdapterAdvancedProperty -Name 'SLOT 3 Port 1' -RegistryKeyword '*JumboPacket' -RegistryValue 9014
```
- `*JumboPacket` is the standardized keyword for the largest frame size the hardware supports (default 1514);
  its range and maximum are defined by the NIC vendor, so check the valid values (for example 9014 or 9000).
- Must be set on every hop: host NICs, vSwitch (automatic), physical switch ports and the storage/peer side. A
  single 1500 hop causes silent drops of large packets (SMB, iSCSI stall) rather than errors.
- Use only on dedicated storage, live migration or backup networks, not the client network.

## Verify path MTU
```cmd
ping -f -l 8972 10.10.20.11
```
`/f` sets Do not Fragment (IPv4 only) and `/l` sets the data size in bytes (default 32). 8972 = 9000 minus 28 bytes of
IP and ICMP headers. A failure to send the packet unfragmented means some hop on the path has a smaller MTU.

## Speed/duplex
`*SpeedDuplex` defaults to Auto Negotiation. Leave it unless the switch port is hard-set, and then match both ends.
Check `Get-NetAdapter | Select Name,LinkSpeed,FullDuplex`.

## Other properties
- `*InterruptModeration` (Enabled by default in the INF enumeration; algorithms are device-dependent). Change it only
  after testing.
- `*RSS` is Enabled by default.

Many advanced properties require restarting the adapter to take effect; `Set-NetAdapterAdvancedProperty` restarts it
unless you pass `-NoRestart`. Do it in a maintenance window or one team member at a time.

## Verify
- [ ] `ping -f -l` succeeds on all storage peers; no discards in adapter statistics after load.

## Checked

2026-10-27. Documentation release: Windows driver documentation on standardized INF keywords (enumeration and editable keywords), the Set-NetAdapterAdvancedProperty reference (Windows Server 2022 docset) and the ping command reference. Confirmed: *JumboPacket default 1514 and vendor-defined range, *SpeedDuplex, *InterruptModeration and *RSS defaults, -RegistryKeyword/-RegistryValue/-NoRestart, ping /f and /l. Removed the Energy Efficient Ethernet and receive/transmit buffer advice and the 'header included on most drivers' claim as unconfirmed.

Method: documentation only; no commands were run.
