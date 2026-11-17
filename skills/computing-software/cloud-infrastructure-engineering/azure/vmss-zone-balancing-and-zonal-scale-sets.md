---
id: computing-software.cloud-infrastructure-engineering.azure.vmss-zone-balancing-and-zonal-scale-sets
name: vmss-zone-balancing-and-zonal-scale-sets
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vmss, availability-zones, zone-balance, fault-domains, resilience]
level: practitioner
status: docs-checked
description: "Deploy zone-spanning scale sets: zones list, strict vs best-effort zone balance, fault domain settings and what happens during a zone outage."
sources: ["https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-use-availability-zones", "https://learn.microsoft.com/azure/reliability/reliability-virtual-machine-scale-sets", "https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-manage-fault-domains", "https://learn.microsoft.com/cli/azure/vmss"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMSS zone balancing

**Goal:** a scale set that keeps serving when a zone fails, without stalling scale-out when one zone is short on capacity.

## Create zone-spanning
```bash
az vmss create -g <rg> -n vmss-web --image Ubuntu2204 --orchestration-mode Flexible \
  --zones 1 2 3 --platform-fault-domain-count 1 --instance-count 6 --lb-sku Standard
```
- **Zone-spanning** (`--zones 1 2 3`) spreads instances across the zones you choose; scale sets do not replicate data
  across zones or fail over automatically, so a zonal resource needs separate deployments plus your own routing and failover.
- Fault domains: zonal and zone-spanning scale sets use max spreading (`platformFaultDomainCount = 1`) by default.
  Fixed spreading with five fault domains is an option in some modes; regional (non-zonal) sets default to 5 in some
  modes and 1 in others, and 2 or 3 apply to regional sets only (see the fault-domain page's table for your
  orchestration mode). If the platform can't allocate the requested fault domain count, the request fails.

## Zone balance
- Default: best-effort even spread across the selected zones.
- Strict: set `zoneBalance` to true. If a SKU isn't available in one of the selected zones, the scale set may not be
  able to scale out to meet capacity.
```bash
az vmss update -g <rg> -n vmss-web --zone-balance true
```
The CLI flag `--zone-balance` takes `true` or `false`.

## Zone outage behaviour
- If a zone fails the scale set might experience downtime for instances there; you may add capacity during the outage and
  the scale set adds instances in the unaffected zones. After the zone returns you may need to scale back down to the
  original capacity.
- Capacity planning: size so the remaining zones can carry the load if one fails.

## Gotchas
- You can convert an existing non-zonal (regional) scale set to use availability zones; see the "Convert existing scale
  sets" section of the reliability page for the conditions.
- Check VM SKU availability in every selected zone; a SKU missing from a zone limits scale-out.
- Disk colocation with the VM is guaranteed for Ultra and Premium v2 disks, best effort for Premium v1 and not
  guaranteed for Standard SSD/HDD.

## Verify
- [ ] `az vmss list-instances --query "[].zones[0]"` shows the intended distribution across zones.

## Checked
2026-10-27. Confirmed against Learn "Create a scale set that uses availability zones", "Reliability in Virtual Machine
Scale Sets", "Manage fault domains in scale sets" and the az vmss CLI reference (`--zone-balance`, `--zones`,
`--platform-fault-domain-count`). Fixed: strict balance does not have a documented "differ by at most 1" rule; the
fault-domain guidance was oversimplified. Removed: "best-effort default means other zones when needed" detail, scale-in
ordering claim, public IP/Application Gateway notes, `az vm list-skus --zone` and Chaos Studio advice, and cross-zone
traffic cost note (not in fetched pages).
Method: documentation only; no commands were run.
