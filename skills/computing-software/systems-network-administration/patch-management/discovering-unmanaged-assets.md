---
id: computing-software.systems-network-administration.patch-management.discovering-unmanaged-assets
name: discovering-unmanaged-assets
category: computing-software
field: systems-network-administration
product: patch-management
tags: [asset-discovery, unmanaged-assets, software-inventory, nmap, shadow-it, patch-management]
level: practitioner
status: draft
description: "Find hosts your patch tooling does not know about by reconciling network scans, DHCP, switch tables, cloud APIs and EDR against the managed-agent list."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://nmap.org/book/man-host-discovery.html
  - https://www.cisecurity.org/controls/inventory-and-control-of-enterprise-assets
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discovering unmanaged assets

**Goal:** every device that can be patched is either managed by a patch tool or knowingly excepted. Unknown hosts never get patched.

## Collect from several independent sources
| Source | Command / place |
|---|---|
| Network sweep | `nmap -sn -PE -PS22,80,443,3389 10.0.0.0/16 -oG sweep.gnmap` |
| DHCP leases | Windows: `Get-DhcpServerv4Lease -ScopeId 10.0.10.0`; ISC/Kea lease files |
| Switch MAC/ARP tables | `show mac address-table`, `show ip arp` via config backup tooling |
| Cloud | `aws ec2 describe-instances`, Azure Resource Graph `Resources | where type =~ 'microsoft.compute/virtualmachines'`, `gcloud compute instances list` |
| Hypervisors | vCenter/Proxmox/Hyper-V VM lists |
| Directory | `Get-ADComputer -Filter * -Properties LastLogonTimestamp` |
| Security tools | EDR device list, vulnerability scanner asset list |

## Reconcile
1. Normalise to a key: MAC address plus hostname, or serial/instance ID for VMs and cloud.
2. Union all discovered sources.
3. Subtract the list of hosts reporting to your patch tools (WSUS/ConfigMgr/Intune, Satellite, Ansible inventory).
4. What remains is unmanaged. Classify: printers/IoT (vendor firmware process), appliances, rogue/shadow IT, stale records.

```bash
comm -23 <(sort discovered.txt) <(sort managed.txt) > unmanaged.txt
```

## Act
- Assign an owner for each unmanaged host within a fixed SLA; enrol, isolate or document an exception.
- Feed results to the CMDB.
- Run discovery at least weekly; continuous passive tools (runZero, Defender device discovery, network sensors) reduce gaps.

## Gotchas
- Ping sweeps miss hosts with ICMP blocked; include TCP probes and passive sources.
- Short-lived cloud instances: discover from cloud APIs or image pipelines, not scans.

## Verify
The unmanaged count trends to zero (or documented exceptions only) week on week.
