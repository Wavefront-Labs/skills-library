---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vm-bandwidth-management
name: hyper-v-vm-bandwidth-management
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-bandwidth-management, minimumbandwidth, hyper-v-switch, qos, hyper-v]
level: practitioner
status: docs-checked
description: "Limit and guarantee Hyper-V VM network bandwidth: switch MinimumBandwidthMode, absolute vs weight minimums, maximum caps, default flow, and verifying under contention."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/network-quality-of-service-bandwidth-limits
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmswitch
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmswitch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM bandwidth management on Hyper-V

## The switch mode decides
`New-VMSwitch -MinimumBandwidthMode Absolute | Weight | None | Default` chooses how minimum bandwidth is expressed when the switch is created. Weight (1 to 100) is recommended: it is more flexible and compatible with live migration and NIC teaming. Absolute is bits per second, with a minimum unit of 1% of link capacity (100 Mbps on 10 GbE) and rounding to the nearest percent. `None` disables minimum bandwidth on the switch; `Default` selects Weight on a switch that is not IOV-enabled and None on an IOV-enabled one.

## Per VM NIC
```powershell
# cap; value in bits per second
Set-VMNetworkAdapter -VMName backup01 -MaximumBandwidth 2000000000      # 2 Gbps

# guarantee in Weight mode (relative weight, 1-100)
Set-VMNetworkAdapter -VMName sql01 -MinimumBandwidthWeight 30

# guarantee in Absolute mode (bps)
Set-VMNetworkAdapter -VMName sql01 -MinimumBandwidthAbsolute 1000000000

# weight of the "default flow": traffic from adapters with no minimum allocated (default weight 1)
Set-VMSwitch -Name vSwitch1 -DefaultFlowMinimumBandwidthWeight 20
```

## Design rules
- Keep the sum of weights near or under 100; larger sums increase rounding error. For 20 VMs sharing a link, give each weight 1 rather than 10.
- Give critical workloads a relatively large weight even if they need little bandwidth (management and cluster heartbeat: 5 or more), and gap the weights (5, 3, 1 rather than 3, 2, 1).
- Account for unfiltered traffic with a catch-all flow.
- Do not enable Minimum Bandwidth and Data Center Bridging (DCB) for workloads that share the same networking stack or NIC.

## Gotchas
- Absolute minimums can break live migration if the destination cannot guarantee the same spare bandwidth; weights avoid that.
- `-MaximumBandwidth` and `-MinimumBandwidthAbsolute` are in bits per second, not bytes: 1000000000 is 1 Gbps.

## Verify
```powershell
Get-VMNetworkAdapter -VMName sql01 | Select VMName, @{n='MinW';e={$_.BandwidthSetting.MinimumBandwidthWeight}}, @{n='Max';e={$_.BandwidthSetting.MaximumBandwidth}}
```
Then check the settings with `Get-VMSwitch` and `Get-VMNetworkAdapter` before relying on them.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: MinimumBandwidthMode values and Default behaviour, weight range 1 to 100, 1% granularity of absolute minimums, the weight-versus-absolute live-migration reasoning, the Minimum Bandwidth and DCB restriction, bits-per-second units for MaximumBandwidth and MinimumBandwidthAbsolute, and the default-flow weight of 1. Removed because no documentation page confirmed them: the BandwidthReservationMode property, the egress-only and SR-IOV/RDMA bypass claims, the GUI path, and the iperf test.
Method: documentation only; no commands were run.
