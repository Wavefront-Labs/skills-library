---
id: computing-software.systems-network-administration.virtualisation.vswitch-security-policy-forged-transmits-mac-learning
name: vswitch-security-policy-forged-transmits-mac-learning
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [forged-transmits, mac-learning, promiscuous-mode, vsphere-networking, distributed-switch, nested-esxi, vmware, vsphere]
level: practitioner
status: draft
description: "Set vSwitch security policy (promiscuous mode, MAC address changes, forged transmits) and vDS MAC learning correctly for nested hypervisors, NLB, appliances and IDS."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSwitch security policy and MAC learning

## The three settings (per switch, overridable per port group)
| Setting | Reject means | Default vSS | Default vDS |
|---|---|---|---|
| Promiscuous mode | VM sees only frames for its own MAC | Reject | Reject |
| MAC address changes | Drop inbound if guest changed its effective MAC | Accept | Reject |
| Forged transmits | Drop outbound frames with a source MAC not equal to vNIC MAC | Accept | Reject |

Hardening baseline: all three Reject, then open exceptions on dedicated port groups only.

## Who needs what
| Workload | Needs |
|---|---|
| Nested ESXi / nested Hyper-V / KVM labs | Forged transmits + MAC changes Accept, plus promiscuous **or** (better) MAC learning on vDS 6.7+ |
| Windows NLB unicast | MAC changes + forged transmits Accept |
| IDS / packet capture VM | Promiscuous Accept on its own port group (or use port mirroring) |
| Firewalls/routers with CARP/VRRP virtual MACs | Forged transmits + MAC changes Accept |
| Linux bonding mode balance-alb in guest | MAC changes Accept |

## MAC learning (vDS 6.7+, better than promiscuous)
Promiscuous floods every frame on the port group to every promiscuous VM: CPU and
throughput cost. MAC learning lets the vDS learn multiple MACs behind one vNIC.
```powershell
# PowerCLI 12+: MAC learning is on the port group's MacManagementPolicy
$pg   = Get-VDPortgroup "Nested-Trunk"
$spec = New-Object VMware.Vim.DVPortgroupConfigSpec
$spec.ConfigVersion = $pg.ExtensionData.Config.ConfigVersion
$spec.DefaultPortConfig = New-Object VMware.Vim.VMwareDVSPortSetting
$mac = New-Object VMware.Vim.DVSMacManagementPolicy
$mac.AllowPromiscuous = $false; $mac.ForgedTransmits = $true; $mac.MacChanges = $true
$mac.MacLearningPolicy = New-Object VMware.Vim.DVSMacLearningPolicy
$mac.MacLearningPolicy.Enabled = $true; $mac.MacLearningPolicy.Limit = 4096
$mac.MacLearningPolicy.LimitPolicy = "DROP"; $mac.MacLearningPolicy.AllowUnicastFlooding = $true
$spec.DefaultPortConfig.MacManagementPolicy = $mac
$pg.ExtensionData.ReconfigureDVPortgroup_Task($spec)
```
vSS has no MAC learning; on vSS use promiscuous plus forged transmits.

## Gotchas
- Port-group override beats switch setting; check both when troubleshooting.
- Nested ESXi without these: VMs inside the nested host get no network although the
  nested host itself pings fine (its vmk uses the outer vNIC MAC).
- Security scanners flag Accept on vSS defaults; set Reject at switch level.

## Verify
`esxcli network vswitch standard policy security get -v vSwitch0`; for vDS check the port
group policy tab. Test: nested VM gets DHCP/ping; NLB cluster converges.
