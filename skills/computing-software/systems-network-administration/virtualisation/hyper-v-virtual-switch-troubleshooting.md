---
id: computing-software.systems-network-administration.virtualisation.hyper-v-virtual-switch-troubleshooting
name: hyper-v-virtual-switch-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmswitch-troubleshooting, hyper-v, virtual-switch, pktmon, networking]
level: advanced
status: docs-checked
description: "Troubleshoot Hyper-V virtual switch connectivity: VLAN and teaming checks, VMQ problems, extension issues, VmSwitch event logs and packet capture with pktmon."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-start
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-etl2pcap
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-filter-add
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/hpn/rsc-in-the-vswitch
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadaptervmq
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Virtual switch troubleshooting

**Goal:** find why a VM (or the host) has no or poor network connectivity through a Hyper-V switch.

## Check configuration in order
```powershell
Get-VMNetworkAdapter -VMName app01 | Select Name, SwitchName, Status, MacAddress, IPAddresses
Get-VMNetworkAdapterVlan -VMName app01                       # Access VLAN vs switch port config
Get-VMSwitch | Format-List *
Get-VMSwitchTeam
Get-NetAdapter | Select Name, Status, LinkSpeed, VlanID
Get-VMSwitchExtension -VMSwitchName vSwitch | Where Enabled
```
Typical findings: VM on the wrong switch, VLAN set on the VM but the physical port is access mode (or vice versa), a teamed NIC down, a third-party filtering extension dropping traffic, duplicate MAC.

## VMQ and offloads
If you suspect VMQ, test with it disabled on the physical adapter:
```powershell
Get-NetAdapterVmq
Set-NetAdapterVmq -Name 'pNIC1' -Enabled $false     # test; update driver/firmware for the real fix
```
Also check RSC in the vSwitch (`Get-VMSwitch -Name <switch> | Select-Object *RSC*`) and driver versions.

## Packet capture with pktmon
```powershell
pktmon filter add -i 10.0.10.25                 # a packet must match every condition of at least one filter
pktmon list                                     # networking stack layout and component IDs
pktmon start --capture --comp all --pkt-size 0  # --pkt-size 0 logs whole packets (default 128 bytes)
# reproduce
pktmon stop
pktmon etl2pcap PktMon.etl --out capture.pcapng   # open in Wireshark (dropped packets excluded unless --drop-only)
```
Seeing a packet at the vmNIC but not the pNIC points at the switch or an extension; at the pNIC but not on the wire points at the NIC/driver or upstream.

## Last resort
Recreate the switch (from console/iLO, not over the network it carries): `Remove-VMSwitch`, then `New-VMSwitch` with the same name so VMs reconnect.

## Checked

Checked 2026-10-26 against the Windows Server pktmon pages (`pktmon start`, `pktmon etl2pcap`, `pktmon filter add`, packet monitor overview), the RSC in the vSwitch page and the `Set-NetAdapterVmq` reference (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23). Confirmed: pktmon syntax and defaults (`--comp`, `--pkt-size` default 128, `--out`), filter matching rule, RSC inspection with `Select-Object *RSC*`, VMQ cmdlet parameters. Removed as undocumented: Event Viewer log names, the 1 GbE VMQ known-issue statement, and the property lists for `Get-VMSwitch` and `Get-VMSwitchTeam`.

Method: documentation only; no commands were run.
