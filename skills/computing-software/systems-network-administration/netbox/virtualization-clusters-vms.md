---
id: computing-software.systems-network-administration.netbox.virtualization-clusters-vms
name: virtualization-clusters-vms
category: computing-software
field: systems-network-administration
product: netbox
tags: [virtualization, clusters, virtual-machines]
level: practitioner
status: docs-checked
description: "Place VMs by site, cluster, host or standalone device."
sources: ["https://netboxlabs.com/docs/netbox/features/virtualization/", "https://netboxlabs.com/docs/netbox/integrations/rest-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtualization

Goal: model VMs next to physical infrastructure.

**Clusters.** A cluster is one or more physical host devices on which VMs can run. Each needs a user-defined type and an operational status, and may be assigned to a user-defined group. Designating host devices is optional.

**Virtual machine types.** Reusable classifications that can define create-time defaults for platform, vCPUs and memory, useful when many VMs share a sizing profile.

**Virtual machines.** They behave much like devices without physical attributes. A VM can have interfaces with IP addresses and VLANs, but those interfaces cannot be cabled because they are virtual. A VM can define compute, memory and storage resources.

**Placement.** Three options:

1. Assign to a site alone for logical grouping.
2. Assign to a cluster, optionally pinned to a specific host device.
3. Assign directly to a standalone device that belongs to no cluster.

**IP assignment.** For an IP on a VM interface use the generic relation type `virtualization.vminterface` through the REST API.

**Checklist**

1. Create cluster type and status first.
2. Pick one placement mode per VM.
3. Use VM types for repeatable sizing.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Virtualization feature page and the REST API overview (generic relations section), both read in full.
