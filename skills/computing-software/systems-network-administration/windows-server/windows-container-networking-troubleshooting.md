---
id: computing-software.systems-network-administration.windows-server.windows-container-networking-troubleshooting
name: windows-container-networking-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-containers, hnsdiag, host-networking-service, windows-container-networking, container-nat-network]
level: advanced
status: docs-checked
description: "Troubleshoot Windows container networking with the Host Networking Service: hnsdiag, Get-HnsNetwork, collectlogs, NAT port conflicts and stale endpoints."
sources:
  - https://github.com/microsoft/SDN/tree/master/Kubernetes/windows/debug
  - https://github.com/microsoft/SDN/tree/master/Kubernetes/windows
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/network-drivers-topologies
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows container networking troubleshooting
Windows containers get their networks from the Host Networking Service (HNS), which programs the virtual switch and
policy. Collect state before changing anything.

## Inspect
```cmd
hnsdiag list all -d
```
PowerShell, using the HNS helper modules in the microsoft/SDN repository (`Kubernetes/windows`, for example
`hns.v2.psm1`, which defines `Get-HnsNetwork`):
```powershell
Import-Module .\hns.v2.psm1
Get-HnsNetwork
```
Docker view: `docker network ls` and `docker network inspect nat`.

## Checks
- Containers on transparent or l2bridge networks from a VM host need MAC address spoofing enabled on the VM's network
  adapter; transparent is not supported on Azure VMs.
- NAT networks on Windows Server 2019 and later are not persisted across reboots; recreate them if they vanish.
- On overlay networks (Windows Server 2019 and later), test with TCP or UDP tools because ICMP is not supported through
  the VFP NAT rules.
- Check the `fixed-cidr` setting in the Docker daemon configuration file if the default NAT subnet overlaps another range.

## Logs
`collectlogs.ps1` in the microsoft/SDN repository (`Kubernetes/windows/debug`) collects the state needed to validate that
policies are plumbed: it runs `hnsdiag list all -d` when available and copies the Microsoft-Windows-Host-Network-Service
event logs. The same folder has packet-capture and HNS trace scripts.

## Verify
- [ ] A new container gets an address on the intended network and can reach its gateway.
- [ ] Published ports on a nat network answer from another host.

## Checked

2026-10-26 against the microsoft/SDN repository (Kubernetes/windows: hns.v2.psm1 defines Get-HnsNetwork, debug/collectlogs.ps1 runs `hnsdiag list all -d` and copies the Host-Network-Service logs; last commit 2025-08-21) and the Windows containers networking docs (MAC spoofing and Azure restriction, NAT persistence, overlay ICMP note, fixed-cidr; last commit 2026-10-20). Replaced the previous command list: `hnsdiag list networks/endpoints/loadbalancers`, `hnsdiag delete endpoints`, the HNS reset sequence with Remove-HnsNetwork and Restart-Service hns, the LoggingAndCleanupAide scripts and the specific error text could not be found in the documentation or repository and were removed.

Method: documentation only; no commands were run.
