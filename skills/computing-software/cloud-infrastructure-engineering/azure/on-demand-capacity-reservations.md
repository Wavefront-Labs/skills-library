---
id: computing-software.cloud-infrastructure-engineering.azure.on-demand-capacity-reservations
name: on-demand-capacity-reservations
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-availability, capacity-reservation-group, on-demand-capacity, reservation, capacity]
level: practitioner
status: docs-checked
description: "Reserve Azure VM capacity with capacity reservation groups: create, consume, resize, delete, how billing and discounts apply, and the unsupported deployment types."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview", "https://learn.microsoft.com/en-us/cli/azure/capacity/reservation", "https://learn.microsoft.com/en-us/cli/azure/capacity/reservation/group"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-demand capacity reservations

**Goal:** hold VM capacity in a region or zone for a critical workload (DR failover, launch events) without a term commitment.

## Model
- A capacity reservation group holds reservations. Each reservation has one VM size, one region, optionally one zone, and a quantity.
- A group has one reservation per VM size per zone (or per size if no zones are set). If a group has no zones, Azure picks the zone and VMs must then be deployed without specifying a zone.
- A reservation fails to create if Azure has no capacity or you lack quota. Reserved Instances give a billing discount only, not a capacity guarantee.
- A VM must specify the reservation group to consume the reservation.

## Create
```bash
az capacity reservation group create -g rg -n crg1 -l westeurope --zones 1 2 3
az capacity reservation create -g rg --capacity-reservation-group crg1 -n res-d4 \
  --sku Standard_D4s_v5 --capacity 5 --zone 1
```
- `--zone` on `az capacity reservation create` is a single value that must be one of the zones set on the group, can only be assigned at creation, and if omitted the reservation supports only non-zonal deployments. If given, VMs using it must be in the same zone.
- `--sku` accepts VM SKUs whose "CapacityReservationSupported" capability is true.
- The CLI reference also shows Future reservations (`--schedule-profile-start`, at least 7 days and at most 6 months ahead, with `--minimum-commitment-days`) and Block reservations (`--end`, 1 to 14 days or 3 to 26 weeks); these were not read beyond the parameter text.

## Consume
```bash
az vm create -g rg -n vm1 --image Ubuntu2204 --size Standard_D4s_v5 --zone 1 --capacity-reservation-group crg1
az vm update -g rg -n vm1 --capacity-reservation-group crg1
```

## Adjust and delete
- Quantity is changed through the reservation's `capacity` property. VM size and location cannot be changed.
- Lifecycle properties: `capacity`, `virtualMachinesAllocated`, `virtualMachinesAssociated`.
- Overallocation (more VMs than reserved) is not covered by the SLA.
- Delete a reservation only after all associated VMs are dissociated from it.

## Billing
Reservations are billed at the same rate as the underlying VM size, whether used or not. Used and unused reservations are both eligible for Savings Plan and Reserved Instance discounts. Prices are not recorded here.

## Limits
Quota is required. Only some VM series are supported. Unsupported deployment types include Spot, Dedicated Host, availability sets, proximity placement groups, update domains and Ultra Disk (check the overview page for the full list). Available to paid customers only.

## Inspect
```bash
az capacity reservation show -g rg -c crg1 -n res-d4 --instance-view
az capacity reservation group show -g rg -n crg1 --instance-view
```
`--instance-view` returns the instance view of the reservation or group (the CLI shows it as a flag; the output fields were not read).

## Checked
Date: 2026-11-07
Read in full: Learn "On-demand capacity reservation overview" (model, lifecycle properties, billing and discount eligibility, SLA note, limitations) and the `az capacity reservation` reference sections for create, show and the zone, SKU and schedule parameters. For `az capacity reservation group`, I read the create and show syntax and examples (`--zones`, `--instance-view`), not every command.
Fixed or removed: `--expand instanceView` (the real flag is `--instance-view`), "failure is immediate", the claim that attaching requires a deallocated VM, sharing with other subscriptions via a sharing profile, the `utilizationInfo.currentCapacity` Verify step, the "reservations and RI are separate" phrasing (replaced with the page's wording), the "cancel by deleting" shortcut (replaced with the dissociate-first rule), and the unconfirmed footer.
Not confirmed: `az vm create` and `az vm update` `--capacity-reservation-group` flags were checked only by the review tooling, not on a page I read; the full unsupported-deployment list and supported VM series were not transcribed.
Method: documentation only; no commands were run.
