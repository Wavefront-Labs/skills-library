---
id: computing-software.systems-network-administration.windows-server.nic-teaming-lbfo-vs-set
name: nic-teaming-lbfo-vs-set
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, netadapter, server-networking, nic-teaming, lbfo, new-netlbfoteam, switch-embedded-teaming, switch-independent, lacp, load-balancing-algorithm, hyper-v-virtual-switch]
level: practitioner
status: docs-checked
description: "Team NICs on Windows Server: LBFO modes and algorithms with New-NetLbfoTeam for non-Hyper-V hosts, why Hyper-V hosts must use SET, and switch-side settings."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/netlbfo/new-netlbfoteam
  - https://learn.microsoft.com/en-us/powershell/module/netlbfo/set-netlbfoteammember
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmswitch
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmswitchteam
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NIC teaming: LBFO vs SET

## Decision
- **Hyper-V hosts**: use **Switch Embedded Teaming (SET)** on the virtual switch. SET has been in Windows Server
  since 2016; on Azure Local it is the only supported teaming and LBFO is not supported. Check Microsoft's current
  guidance before binding a Hyper-V switch to an LBFO team on Windows Server.
- **Non-Hyper-V servers** (file servers, physical app servers): the NetLbfo cmdlets (`New-NetLbfoTeam`) are the
  teaming tool.

## LBFO
```powershell
New-NetLbfoTeam -Name 'Team-LAN' -TeamMembers 'NIC1','NIC2' `
  -TeamingMode SwitchIndependent -LoadBalancingAlgorithm Dynamic -Confirm:$false
Get-NetLbfoTeam ; Get-NetLbfoTeamMember
Add-NetLbfoTeamNic -Team 'Team-LAN' -VlanID 30     # extra tNIC on a VLAN
```
Modes (`-TeamingMode`: Static, SwitchIndependent, Lacp):
- **SwitchIndependent**: no switch configuration; members can connect to different switches.
- **LACP**: IEEE 802.1ax; the switch side must be configured to match.
- **Static**: needs configuration on both switch and host to identify the team links.
Algorithms (`-LoadBalancingAlgorithm`): Dynamic, TransportPorts, IPAddresses, MacAddresses, HyperVPort. **Dynamic**
hashes ports and IPs for outbound traffic and moves streams between members to balance utilisation; with
SwitchIndependent, inbound traffic goes to a particular member. TransportPorts, IPAddresses and MacAddresses send
all inbound traffic to the primary member in SwitchIndependent mode.
Standby adapter for active/passive: `Set-NetLbfoTeamMember -Name NIC2 -AdministrativeMode Standby`.

## SET (on Hyper-V hosts)
```powershell
New-VMSwitch -Name SETswitch -NetAdapterName 'NIC1','NIC2' -EnableEmbeddedTeaming $true -AllowManagementOS $true
Set-VMSwitchTeam -Name SETswitch -LoadBalancingAlgorithm HyperVPort
```
SET is switch-independent only, with Dynamic or HyperVPort load balancing (Microsoft recommends HyperVPort on NICs at
10 Gbps or faster), supports up to eight adapters per team, requires symmetric (identical) adapters, and supports
teaming of RDMA adapters. Dynamic VMMQ requires SET.

## Verify
- [ ] Pull one cable: `Get-NetLbfoTeamMember` shows the member's status change and traffic continues.
- [ ] Switch ports configured to match the mode (LACP or static need switch configuration; SwitchIndependent does not).

## Checked

2026-10-27. Documentation release: Windows Server 2022 docset NetLbfo cmdlet references (New-NetLbfoTeam, Set-NetLbfoTeamMember, Add-NetLbfoTeamNic), New-VMSwitch and Set-VMSwitchTeam references, and the Azure Local host network requirements page. Confirmed teaming modes, algorithm behaviour, Standby administrative mode, -EnableEmbeddedTeaming, SET load-balancing options, eight-adapter limit, symmetric adapter requirement and that LBFO is unsupported on Azure Local. Removed the claim that LBFO binding to a Hyper-V switch is deprecated and blocked by default on 2022+, the SMB Multichannel alternative, and the recommendation wording on default mode, none of which a fetched page states.

Method: documentation only; no commands were run.
