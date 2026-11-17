---
id: computing-software.systems-network-administration.windows-server.iscsi-network-design
name: iscsi-network-design
category: computing-software
field: systems-network-administration
product: windows-server
tags: [iscsi, iscsi-network-design, mpio, jumbo-frames, iscsi-initiator]
level: practitioner
status: docs-checked
description: "Design iSCSI networks on Windows: dedicated subnets per path, no teaming, disabled DNS registration and NetBIOS, jumbo frames and MPIO binding."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-target-server
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/connect-iscsitarget
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/new-iscsitargetportal
  - https://learn.microsoft.com/en-us/powershell/module/mpio/enable-msdsmautomaticclaim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iSCSI network design

## Rules
- **Dedicated NICs and switches or VLANs** for iSCSI, separate from client traffic.
- **Two separate subnets** (one per fabric/switch), one NIC per subnet, for MPIO paths. Do not team iSCSI NICs
  (LBFO or SET); multipathing is MPIO's job.
- No default gateway on iSCSI NICs; they should not route.
- Disable DNS registration, NetBIOS over TCP/IP and Client for Microsoft Networks/File Sharing bindings on iSCSI NICs.
- Jumbo frames only if every hop (host, switch, target) supports them; test the path with a do-not-fragment ping at your configured packet size.

## Configure the NICs
```powershell
Set-NetIPInterface -InterfaceAlias iSCSI-A,iSCSI-B -InterfaceMetric 100
Set-DnsClient -InterfaceAlias iSCSI-A,iSCSI-B -RegisterThisConnectionsAddress $false
Disable-NetAdapterBinding -Name iSCSI-A,iSCSI-B -ComponentID <COMPONENT_ID>   # ids for Client for Microsoft Networks and File and Printer Sharing: list with Get-NetAdapterBinding
```
NetBIOS: adapter TCP/IPv4 > Advanced > WINS > Disable NetBIOS over TCP/IP.

## Bind sessions to specific paths
```powershell
New-IscsiTargetPortal -TargetPortalAddress 10.50.1.10 -InitiatorPortalAddress 10.50.1.21
New-IscsiTargetPortal -TargetPortalAddress 10.51.1.10 -InitiatorPortalAddress 10.51.1.21
Get-IscsiTarget | Connect-IscsiTarget -IsMultipathEnabled $true -IsPersistent $true -InitiatorPortalAddress 10.50.1.21 -TargetPortalAddress 10.50.1.10
Get-IscsiTarget | Connect-IscsiTarget -IsMultipathEnabled $true -IsPersistent $true -InitiatorPortalAddress 10.51.1.21 -TargetPortalAddress 10.51.1.10
```
`-InitiatorPortalAddress` pins each session to the chosen initiator NIC.

## Hyper-V hosts
Keep host iSCSI on physical NICs rather than a vSwitch unless guests need in-guest iSCSI; then give them dedicated vNICs.

## Verify
- [ ] `Get-IscsiSession | Select InitiatorPortalAddress,TargetNodeAddress` shows one session per path.
- [ ] The MPIO tooling you use (the `mpclaim` utility, or the MPIO properties dialog) shows two paths per disk; `mpclaim` is not covered in the current Microsoft Learn reference.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Connect-IscsiTarget -IsMultipathEnabled, -IsPersistent, -InitiatorPortalAddress, -TargetPortalAddress and New-IscsiTargetPortal confirmed in the iscsi module references.
- Set-NetIPInterface -InterfaceMetric, Set-DnsClient -RegisterThisConnectionsAddress and Disable-NetAdapterBinding -Name/-ComponentID exist in the Windows Server 2025 references.
- Removed unconfirmed details: the exact `ping -f -l 8972` size, the WMI SetTcpipNetbios call, the specific component ids and the claim that Windows may send both sessions from one NIC.

Method: documentation only; no commands were run.
