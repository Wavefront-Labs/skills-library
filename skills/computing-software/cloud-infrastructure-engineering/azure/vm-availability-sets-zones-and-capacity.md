---
id: computing-software.cloud-infrastructure-engineering.azure.vm-availability-sets-zones-and-capacity
name: vm-availability-sets-zones-and-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-machines, availability-sets, availability-zones, fault-domains, update-domains, scheduled-events, high-availability]
level: practitioner
status: docs-checked
description: "Choose between Azure availability zones, availability sets and scale sets, create sets correctly, and react to platform maintenance with Scheduled Events."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/availability", "https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview", "https://learn.microsoft.com/en-us/azure/virtual-machines/windows/scheduled-events"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM availability — zones, sets and maintenance events

**Goal:** a VM tier that survives a rack, a host update and a datacentre loss, with the
placement option chosen on purpose.

## 1. The options
| Placement | Protects against | Notes from the docs |
|---|---|---|
| Availability zones | loss of a datacentre | three zones per supported region; each has distinct power, network and cooling |
| Availability set | correlated hardware failures and planned maintenance | two or more VMs meet the 99.95% SLA; no extra cost |
| Scale set (Flexible orchestration) | recommended by Microsoft for HA with the widest feature range | instances can span zones, one zone, or be regional |
- Availability sets give lower VM-to-VM latency than zones but are still exposed to datacentre-level failures; zones have the highest reliability.
- Regional resources have no visible zone, and a failure in any zone can affect a regional VM.
- Combine Azure Load Balancer with zones or scale sets for the most resilience.

## 2. Availability sets
Each set has up to 3 fault domains and 20 update domains, fixed at creation. With more VMs
than update domains (for example a sixth VM with five domains) VMs wrap around to the first
domain. During planned maintenance one update domain restarts at a time and gets 30 minutes
to recover before the next. Only VMs with managed disks can be created in a managed
(Aligned) set; disks are aligned with fault domains.
```bash
az vm availability-set create -n <AS_NAME> -g <RG> --platform-fault-domain-count 3 --platform-update-domain-count 5
az vm create -g <RG> -n <VM_NAME> --availability-set <AS_NAME> ...
```
Two VMs in one set can end up sharing a fault domain in some deployment sequences (the overview
page lists them); check after deployment.
Capacity reservations, proximity placement groups and maintenance configurations have their
own Learn pages; consult them rather than relying on this skill for their limits.

## 3. Scheduled Events
Inside the VM, query the Metadata Service on the static non-routable IP:
```bash
curl -H Metadata:true "http://169.254.169.254/metadata/scheduledevents?api-version=2020-07-01"
```
The `Metadata:true` header is required. Event types include `Reboot`, `Redeploy`, `Preempt`
(Spot eviction) and `Terminate` (scale sets). A scheduled event's approval timeout is 15 minutes.
Restarting a VM schedules a `Reboot` event and redeploying schedules `Redeploy`.

## Gotchas
- Design for N-1: update domains only help if the app tolerates losing one group at a time.
- Zone and set choices are made at VM creation; plan before deploying.

## Verify
- [ ] `az vm list -g <RG> --query "[].{n:name,z:zones,as:availabilitySet.id}" -o table` shows the intended spread.
- [ ] A Scheduled Events poller logs an event during a test restart.

## Checked
2026-10-28. Confirmed on the Learn pages "Availability options for Azure Virtual Machines", "Availability sets overview" and "Scheduled Events for Windows VMs": zones, 99.95% SLA, 3 fault and 20 update domains, immutability, update-domain behaviour and 30-minute recovery, Aligned sets, shared fault-domain note, endpoint, api-version, header, event types, 15-minute approval timeout. Removed (not confirmed in those pages): the 99.9/99.99% SLA rows, zone-mapping REST call, proximity placement group and capacity reservation sections and flags, maintenance configuration and `perform-maintenance`, Freeze/live-migration durations, Basic LB and Dedicated Host claims, verification commands for them.
Method: documentation only; no commands were run.
