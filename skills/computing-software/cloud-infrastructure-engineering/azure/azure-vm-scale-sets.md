---
id: computing-software.cloud-infrastructure-engineering.azure.azure-vm-scale-sets
name: azure-vm-scale-sets
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vmss, virtual-machine-scale-sets, flexible-orchestration, uniform-orchestration, autoscale, azure-monitor-autoscale, predictive-autoscale, spot-priority-mix, spot-vms, eviction-policy, application-health-extension, automatic-instance-repairs, upgrade-policy, rolling-upgrade, automatic-os-image-upgrade, azure-compute-gallery, availability-zones, fault-domains, scale-in-policy, instance-protection, terminate-notification, scheduled-events, cloud-init]
level: practitioner
status: draft
description: "Run Azure VM Scale Sets: Flexible vs Uniform, autoscale rules that don't flap, Spot priority mix, health extension with auto-repair, and rolling image upgrades from Compute Gallery."
sources: ["Microsoft Learn - Orchestration modes for Virtual Machine Scale Sets", "Microsoft Learn - Overview of autoscale in Azure / autoscale best practices", "Microsoft Learn - Spot Priority Mix for VMSS", "Microsoft Learn - Automatic instance repairs for VMSS", "Microsoft Learn - Upgrade policies and rolling upgrades for VMSS"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure VM Scale Sets — elastic VM fleets that heal and roll

**Goal:** a scale set that spreads across zones, scales on a metric without
oscillating, uses Spot where it can, replaces sick instances automatically, and rolls a
new image with no outage.

## 1. Choose orchestration mode
- **Flexible** (default for new scale sets and Microsoft's recommendation): instances
  are ordinary VMs (`Microsoft.Compute/virtualMachines`), can mix sizes, support
  zones + fault-domain spreading, and work with standard VM APIs and backups.
- **Uniform**: identical instances managed only via scale-set APIs; still used by older
  AKS node pools and some platform services. Choose it only when a dependency requires it.
- Mode is fixed at creation.

## 2. Image and configuration
- Build images with Azure Image Builder or Packer into an **Azure Compute Gallery**
  image definition with versions; reference the definition (not a version) so `latest`
  resolves on scale-out, or pin a version and roll deliberately.
- Keep `customData`/cloud-init idempotent and short; anything slow belongs in the image.
- Assign a **user-assigned managed identity** so new instances have it at boot.

## 3. Zones and spreading
- `zones: ["1","2","3"]` with `platformFaultDomainCount: 1` (max spreading) is the
  usual Flexible setup. Turn on zone balancing if you need strictly even counts — it can
  block scale-out when one zone is out of capacity, so weigh that.

## 4. Autoscale that doesn't flap
Autoscale is configured as an Azure Monitor autoscale setting attached to the scale set:
- Pair every **scale-out** rule with a **scale-in** rule, with a gap between thresholds
  (e.g. out at CPU > 70 %, in at < 40 %). Close thresholds cause flapping; autoscale's
  own flap detection will then refuse to scale in.
- Use `PT5M`-`PT10M` time windows, cool-down ≥ boot + warm-up time.
- Scale out aggressively (+20 % or +N), in conservatively (-1 or -10 %).
- Better metrics than CPU: App Gateway/LB request count per instance, Service Bus queue
  length, or a custom metric from Application Insights.
- **Predictive autoscale** (CPU only, needs ~7 days of history) can pre-scale for cyclic
  load; run in *forecast only* first.
- Profiles: a default profile plus recurring (business hours) or fixed-date profiles; the
  min/max of the active profile apply.

## 5. Spot
- **Spot Priority Mix** (Flexible only): e.g. `baseRegularPriorityCount: 2`,
  `regularPriorityPercentageAboveBase: 25` → 2 regular VMs, then 25 % regular / 75 % Spot.
- `evictionPolicy: Delete` for stateless fleets (Deallocate keeps disks and still bills them);
  `maxPrice: -1` to be evicted only for capacity, not price.
- Handle **Scheduled Events** (`Preempt`, ~30 s notice) from the metadata endpoint
  `169.254.169.254/metadata/scheduledevents` to drain.

## 6. Health and repair
- Add the **Application Health extension** (HTTP/HTTPS/TCP probe on the instance) or use
  a load-balancer probe; this is what rolling upgrades and auto-repair trust.
- Enable **automatic instance repairs** with a grace period ≥ boot time; action
  Replace (default), Restart or Reimage.
- **Terminate notification** (scheduled event, 5-15 min configurable) gives scale-in time to drain.
- **Instance protection** from scale-in for instances doing long work; scale-in policy
  `OldestVM` helps roll forward images, `NewestVM` keeps warm caches.

## 7. Upgrades
- Upgrade policy `Rolling` with `maxBatchInstancePercent` 20, `maxUnhealthyInstancePercent`
  20, `pauseTimeBetweenBatches` and `prioritizeUnhealthyInstances: true`. `Automatic` replaces
  everything at once — avoid in prod; `Manual` requires per-instance update calls.
- **Automatic OS image upgrade** for marketplace/gallery images rolls new versions
  using the same health signal.
- MaxSurge rolling upgrades (create new before deleting old) — check availability for your config.

## Gotchas
- Without a health signal, rolling upgrade and auto-repair either refuse to run or roll blind.
- Changing the model doesn't touch existing instances under `Manual` — they show "latest model: No" until upgraded.
- Spot capacity varies by size and zone; diversify sizes (Flexible allows mixed VM sizes via instance-mix — confirm GA status).
- Overprovisioning (Uniform) briefly creates extra VMs; turn off if instances register themselves externally.
- Autoscale settings live in a separate resource; deleting the scale set via IaC may leave orphaned autoscale settings.

## Verify
- [ ] Flexible mode, zones 1-3, image from Compute Gallery, managed identity attached.
- [ ] Health extension reports healthy; auto-repair enabled with tested replace of a killed app.
- [ ] Load test: scale-out before SLO breach, scale-in settles without flapping (autoscale run history clean).
- [ ] Simulated Spot eviction (`az vmss simulate-eviction`) drained without errors.
- [ ] A rolling upgrade to a new image version completes batch by batch with zero failed requests.
